"""
Component Updater - Version Management Tool
檢查並更新 Grasshopper 畫布上的組件版本

    Args:
        check: Check for component updates
        update: Update outdated components (CAUTION: will modify canvas)
        manifest_path: Path to manifest.json (optional)

    Returns:
        report: Version check report
        outdated: List of outdated components
        updated: List of updated components
        errors: Error messages
"""

from ghpythonlib.componentbase import executingcomponent as component
import Rhino.Geometry as rg
import json
import os
import re


class ComponentUpdater(component):

    @staticmethod
    def parse_version(version_str):
        """Parse version string like 'v0.1.0' to tuple (0, 1, 0)"""
        if not version_str:
            return (0, 0, 0)

        # Remove 'v' prefix if exists
        version_str = version_str.strip().lower().replace('v', '')

        # Extract numbers
        match = re.match(r'(\d+)\.(\d+)\.(\d+)', version_str)
        if match:
            return tuple(map(int, match.groups()))

        return (0, 0, 0)

    @staticmethod
    def load_manifest(manifest_path=None):
        """Load manifest.json"""
        if manifest_path and os.path.exists(manifest_path):
            with open(manifest_path, 'r', encoding='utf-8') as f:
                return json.load(f)

        # Auto-detect manifest.json in common locations
        search_paths = [
            os.path.join(os.path.dirname(__file__), 'manifest.json'),
            os.path.join(os.path.dirname(__file__), '..', '..', 'manifest.json'),
            os.path.join(os.path.expanduser('~'), 'Downloads', 'compas-actions.ghpython_components', 'manifest.json')
        ]

        for path in search_paths:
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f)

        return None

    @staticmethod
    def check_canvas_versions(document, manifest):
        """Check versions of components on canvas"""
        if not manifest or 'components' not in manifest:
            return []

        outdated = []
        component_map = {c['guid']: c for c in manifest['components']}

        # Scan all objects in document
        for obj in document.Objects:
            # Check if it's a GHPython component
            if not hasattr(obj, 'ComponentGuid'):
                continue

            guid_str = str(obj.ComponentGuid)

            # Check if this component is in our manifest
            if guid_str in component_map:
                comp_info = component_map[guid_str]

                # Get current version from component message
                current_version = ""
                if hasattr(obj, 'Message'):
                    current_version = obj.Message if obj.Message else ""

                latest_version = "v{}".format(comp_info['version'])

                # Parse and compare versions
                current_tuple = ComponentUpdater.parse_version(current_version)
                latest_tuple = ComponentUpdater.parse_version(latest_version)

                if current_tuple < latest_tuple:
                    outdated.append({
                        'object': obj,
                        'object_id': str(obj.InstanceGuid),
                        'name': comp_info['name'],
                        'nickname': comp_info.get('nickname', ''),
                        'current_version': current_version if current_version else 'unknown',
                        'latest_version': latest_version,
                        'guid': guid_str,
                        'inputs': comp_info.get('inputs', []),
                        'outputs': comp_info.get('outputs', [])
                    })

        return outdated

    @staticmethod
    def check_compatibility(old_comp, manifest_comp):
        """Check if component inputs/outputs are compatible"""
        # Get current parameter names
        current_inputs = set()
        if hasattr(old_comp, 'Params') and hasattr(old_comp.Params, 'Input'):
            current_inputs = {str(p.Name) for p in old_comp.Params.Input}

        current_outputs = set()
        if hasattr(old_comp, 'Params') and hasattr(old_comp.Params, 'Output'):
            current_outputs = {str(p.Name) for p in old_comp.Params.Output}

        # Get manifest parameter names
        manifest_inputs = {p['name'] for p in manifest_comp.get('inputs', [])}
        manifest_outputs = {p['name'] for p in manifest_comp.get('outputs', [])}

        # Check compatibility
        inputs_compatible = current_inputs == manifest_inputs
        outputs_compatible = current_outputs == manifest_outputs

        changes = []
        if not inputs_compatible:
            added = manifest_inputs - current_inputs
            removed = current_inputs - manifest_inputs
            if added:
                changes.append("新增輸入: {}".format(", ".join(added)))
            if removed:
                changes.append("移除輸入: {}".format(", ".join(removed)))

        if not outputs_compatible:
            added = manifest_outputs - current_outputs
            removed = current_outputs - manifest_outputs
            if added:
                changes.append("新增輸出: {}".format(", ".join(added)))
            if removed:
                changes.append("移除輸出: {}".format(", ".join(removed)))

        return inputs_compatible and outputs_compatible, changes

    def RunScript(self, check, update, manifest_path):
        ghenv.Component.Message = 'v{{version}}'

        # Initialize outputs
        report_lines = []
        outdated = []
        updated = []
        errors = []

        # Convert inputs
        check = check if check is not None else False
        update = update if update is not None else False

        try:
            # Load manifest
            manifest = self.load_manifest(manifest_path)

            if not manifest:
                errors.append("找不到 manifest.json 文件")
                report_lines.append("❌ 錯誤：找不到 manifest.json")
                report = "\n".join(report_lines)
                return (report, outdated, updated, errors)

            report_lines.append("=" * 50)
            report_lines.append("組件版本檢查報告")
            report_lines.append("=" * 50)
            report_lines.append("")
            report_lines.append("插件名稱: {}".format(manifest.get('name', 'Unknown')))
            report_lines.append("插件版本: {}".format(manifest.get('version', 'Unknown')))
            report_lines.append("")

            if check:
                # Get current document
                doc = ghenv.Component.OnPingDocument()

                if not doc:
                    errors.append("無法獲取當前文件")
                    report_lines.append("❌ 錯誤：無法獲取當前文件")
                else:
                    # Check versions
                    outdated_list = self.check_canvas_versions(doc, manifest)

                    if not outdated_list:
                        report_lines.append("✅ 所有組件都是最新版本！")
                    else:
                        report_lines.append("發現 {} 個組件需要更新：".format(len(outdated_list)))
                        report_lines.append("")

                        for item in outdated_list:
                            # Check compatibility
                            compatible, changes = self.check_compatibility(
                                item['object'],
                                {'inputs': item['inputs'], 'outputs': item['outputs']}
                            )

                            status = "✅" if compatible else "⚠️"
                            report_lines.append("{} {}".format(status, item['name']))
                            report_lines.append("   當前版本: {}".format(item['current_version']))
                            report_lines.append("   最新版本: {}".format(item['latest_version']))

                            if not compatible:
                                report_lines.append("   狀態: 需手動更新（參數已變更）")
                                for change in changes:
                                    report_lines.append("   - {}".format(change))
                            else:
                                report_lines.append("   狀態: 可自動更新")

                            report_lines.append("")

                            # Add to outdated list
                            outdated.append("{}: {} → {}".format(
                                item['name'],
                                item['current_version'],
                                item['latest_version']
                            ))

            if update and outdated:
                report_lines.append("")
                report_lines.append("=" * 50)
                report_lines.append("⚠️ 更新功能開發中")
                report_lines.append("=" * 50)
                report_lines.append("")
                report_lines.append("自動更新功能需要以下步驟：")
                report_lines.append("1. 從 UserObjects 資料夾載入 .ghuser 文件")
                report_lines.append("2. 記錄舊組件的連線和位置")
                report_lines.append("3. 創建新組件並恢復連線")
                report_lines.append("4. 移除舊組件")
                report_lines.append("")
                report_lines.append("目前請手動更新：")
                report_lines.append("1. 從工具欄拖入新組件")
                report_lines.append("2. 重新連接參數")
                report_lines.append("3. 刪除舊組件")

                errors.append("自動更新功能尚未實作")

        except Exception as e:
            errors.append("執行錯誤: {}".format(str(e)))
            report_lines.append("")
            report_lines.append("❌ 錯誤: {}".format(str(e)))

        report = "\n".join(report_lines)
        return (report, outdated, updated, errors)
