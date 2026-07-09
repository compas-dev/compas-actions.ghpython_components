# 組件版本管理系統設計

## 研究成果：Ladybug Tools 的更新機制

根據研究 Ladybug Tools 的實作，他們提供了三個關鍵組件：

### 1. LB Versioner
- **功能**：更新整個 Ladybug Tools 插件到最新版本
- **機制**：
  - 使用 `ladybug-rhino` CLI 工具
  - 執行 `change-installed-version` 命令
  - 更新後需要重啟 Rhino

### 2. LB Sync Grasshopper File ⭐ (最相關)
- **功能**：同步當前 GH 文件中的所有組件到工具欄版本
- **機制**：
  - 掃描整個 Grasshopper 文件
  - 比對組件 GUID
  - 自動替換相同 GUID 的舊組件
  - 如果 input/output 有變化，標記為紅色需手動處理

### 3. LB Update File
- **功能**：更新舊文件但不更新安裝
- **限制**：只更新到當前安裝的版本

## 我們的需求分析

根據你的需求，我們需要：

1. ✅ **版本檢測**：檢查畫布上的組件是否為最新版本
2. ✅ **更新提醒**：告訴使用者哪些組件需要更新
3. ✅ **一鍵更新**：按鈕自動更新所有舊組件
4. ⚠️ **智能處理**：偵測 input/output 變化，提示手動處理

## 設計方案

### 架構概覽

```
ComponentUpdater (組件更新器)
    ↓
1. 掃描畫布上的所有組件
2. 讀取 UserObjects 資料夾中的最新 .ghuser
3. 比對版本號（透過 Component.Message）
4. 列出需要更新的組件清單
5. 按鈕觸發 → 自動替換組件
6. 保留連線（如果 input/output 相容）
```

### 核心技術

#### 1. 版本號嵌入

在每個組件的 `code.py` 中：
```python
def RunScript(self, ...):
    ghenv.Component.Message = 'v0.1.0'  # 版本號
    # ...
```

#### 2. 組件識別

使用唯一的 `instanceGuid` 識別每個組件類型：
```json
{
  "instanceGuid": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
}
```

#### 3. 版本比對

```python
# 畫布上的組件
canvas_version = component.Message  # "v0.1.0"

# UserObjects 中的組件
latest_version = read_from_ghuser()  # "v0.2.0"

if canvas_version < latest_version:
    needs_update = True
```

#### 4. 組件替換

使用 Grasshopper SDK：
```python
# 1. 記錄舊組件的連線
old_sources = [(param, param.Sources) for param in old_comp.Params.Input]
old_recipients = [(param, param.Recipients) for param in old_comp.Params.Output]

# 2. 創建新組件
new_comp = create_component_from_ghuser()
new_comp.Attributes.Pivot = old_comp.Attributes.Pivot  # 保持位置

# 3. 重新連線（如果參數相容）
reconnect_wires(old_sources, old_recipients, new_comp)

# 4. 刪除舊組件
document.RemoveObject(old_comp)
document.AddObject(new_comp)
```

### 實作細節

#### 組件資訊檔案 (manifest.json)

在專案根目錄創建 `manifest.json`：

```json
{
  "name": "Your Plugin Name",
  "version": "0.2.0",
  "components": [
    {
      "name": "YOLO_UDP_Receiver",
      "guid": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "version": "0.2.0",
      "ghuser_path": "YOLO_UDP_Receiver.ghuser",
      "inputs": [
        {"name": "port", "type": "int"},
        {"name": "target_joint", "type": "str"}
      ],
      "outputs": [
        {"name": "point", "type": "Point3d"},
        {"name": "x", "type": "float"},
        {"name": "y", "type": "float"}
      ]
    },
    {
      "name": "Swarm_Dynamics",
      "guid": "b5c6d7e8-f9a0-1234-bcde-567890abcdef",
      "version": "0.1.0",
      "ghuser_path": "Swarm_Dynamics.ghuser",
      "inputs": [...],
      "outputs": [...]
    }
  ]
}
```

#### ComponentUpdater 組件

創建一個新的組件 `Component_Updater`：

**輸入**：
- `check`: Boolean - 檢查版本
- `update`: Boolean - 執行更新
- `manifest_path`: String - manifest.json 路徑（可選）

**輸出**：
- `report`: String - 版本檢查報告
- `outdated`: List - 需要更新的組件清單
- `updated`: List - 已更新的組件清單
- `errors`: List - 錯誤訊息

**核心邏輯**：

```python
def check_versions():
    """檢查畫布上所有組件的版本"""
    outdated_components = []

    # 1. 讀取 manifest
    manifest = load_manifest()

    # 2. 掃描畫布
    doc = ghenv.Component.OnPingDocument()
    for obj in doc.Objects:
        if is_ghpython_component(obj):
            # 取得組件 GUID
            guid = obj.ComponentGuid

            # 在 manifest 中查找
            component_info = manifest.find_by_guid(guid)
            if component_info:
                # 比對版本
                current_version = obj.Message  # "v0.1.0"
                latest_version = component_info['version']

                if parse_version(current_version) < parse_version(latest_version):
                    outdated_components.append({
                        'object': obj,
                        'name': component_info['name'],
                        'current': current_version,
                        'latest': latest_version,
                        'guid': guid
                    })

    return outdated_components

def update_components(outdated_list):
    """更新畫布上的組件"""
    updated = []
    errors = []

    doc = ghenv.Component.OnPingDocument()

    for item in outdated_list:
        try:
            old_comp = item['object']
            ghuser_path = get_ghuser_path(item['guid'])

            # 檢查 input/output 相容性
            compatible = check_compatibility(old_comp, item['guid'])

            if compatible:
                # 自動替換
                new_comp = replace_component(doc, old_comp, ghuser_path)
                updated.append(item['name'])
            else:
                # 標記為需手動處理
                mark_for_manual_update(old_comp)
                errors.append(f"{item['name']}: input/output 不相容，需手動更新")

        except Exception as e:
            errors.append(f"{item['name']}: {str(e)}")

    return updated, errors
```

## 實作步驟

### Phase 1: 基礎架構（立即可做）

1. **標準化版本號**
   - 在所有組件的 `code.py` 加入版本號
   - 使用 `{{version}}` 模板自動替換

2. **創建 manifest.json**
   - 記錄所有組件的資訊
   - 每次 `gh_comp` 後自動更新

3. **版本比對腳本**
   - 簡單的 Python 腳本
   - 讀取 manifest 和畫布上的組件
   - 列出需要更新的清單

### Phase 2: 組件更新器（需要 Grasshopper SDK）

4. **ComponentUpdater 組件**
   - 實作版本檢查邏輯
   - 實作自動替換邏輯
   - 處理連線保留

5. **相容性檢測**
   - 比對 input/output 名稱和類型
   - 標記不相容的組件

### Phase 3: 進階功能（未來擴充）

6. **批次更新**
   - 一次更新多個 .gh 文件

7. **版本回退**
   - 支援降級到舊版本

8. **更新日誌**
   - 顯示每個版本的變更內容

## 技術挑戰與解決方案

### 挑戰 1: 如何讀取 .ghuser 文件？

**.ghuser 本質上是序列化的 GH_Archive**

**解決方案**：
```python
import clr
clr.AddReference("Grasshopper")
from Grasshopper.Kernel import GH_Archive

def load_ghuser(path):
    archive = GH_Archive()
    if archive.Deserialize_Binary(path):
        # 讀取組件資訊
        root = archive.GetRootNode
        # ... 解析
    return component_info
```

### 挑戰 2: 如何替換組件並保留連線？

**解決方案**：
```python
def replace_component(doc, old_comp, new_comp_path):
    # 1. 記錄位置
    pivot = old_comp.Attributes.Pivot

    # 2. 記錄連線
    input_wires = {}
    for i, param in enumerate(old_comp.Params.Input):
        input_wires[param.Name] = list(param.Sources)

    output_wires = {}
    for i, param in enumerate(old_comp.Params.Output):
        output_wires[param.Name] = list(param.Recipients)

    # 3. 載入新組件
    new_comp = load_from_ghuser(new_comp_path)
    new_comp.Attributes.Pivot = pivot

    # 4. 重新連線
    for param in new_comp.Params.Input:
        if param.Name in input_wires:
            for source in input_wires[param.Name]:
                param.AddSource(source)

    for param in new_comp.Params.Output:
        if param.Name in output_wires:
            for recipient in output_wires[param.Name]:
                recipient.AddSource(param)

    # 5. 替換
    doc.RemoveObject(old_comp, False)
    doc.AddObject(new_comp, False)

    return new_comp
```

### 挑戰 3: 如何偵測 input/output 變化？

**解決方案**：
```python
def check_compatibility(old_comp, new_manifest):
    # 比對參數名稱
    old_inputs = {p.Name for p in old_comp.Params.Input}
    new_inputs = {p['name'] for p in new_manifest['inputs']}

    old_outputs = {p.Name for p in old_comp.Params.Output}
    new_outputs = {p['name'] for p in new_manifest['outputs']}

    # 檢查是否相容
    inputs_compatible = old_inputs == new_inputs
    outputs_compatible = old_outputs == new_outputs

    return inputs_compatible and outputs_compatible
```

## 使用者工作流程

### 場景 1: 檢查版本

```
1. 打開 Grasshopper 文件
2. 放置 ComponentUpdater 組件
3. 設定 check = True
4. 查看 report 輸出：

   版本檢查報告
   ====================
   ✅ Test_GhTimber: v0.1.0 (最新)
   ⚠️ YOLO_UDP_Receiver: v0.1.0 → v0.2.0 可更新
   ⚠️ Swarm_Dynamics: v0.1.0 → v0.1.5 可更新

   總共 2 個組件需要更新
```

### 場景 2: 自動更新（無 input/output 變化）

```
1. check = True (先檢查)
2. 確認可更新
3. update = True
4. 查看結果：

   更新完成！
   ====================
   ✅ YOLO_UDP_Receiver: v0.1.0 → v0.2.0
   ✅ Swarm_Dynamics: v0.1.0 → v0.1.5

   已更新 2 個組件
```

### 場景 3: 手動更新（有 input/output 變化）

```
1. check = True
2. update = True
3. 查看結果：

   更新報告
   ====================
   ✅ YOLO_UDP_Receiver: v0.1.0 → v0.2.0
   🔴 Swarm_Dynamics: 不相容，需手動更新
      - 新增輸入參數: Gravity
      - 移除輸出參數: Labels

   1 個組件已自動更新
   1 個組件需手動處理（已標記為紅色）
```

## 最小可行版本 (MVP)

如果要快速實現，可以先做：

### 簡化版本檢查器

**不需要 Grasshopper SDK，只需要**：

1. **manifest.json**：記錄所有組件版本
2. **Python 腳本**：讀取 .gh 文件（XML格式）
3. **報告生成**：列出需要更新的組件

**實作**：
```python
# check_versions.py
import xml.etree.ElementTree as ET
import json

def parse_gh_file(gh_path):
    """解析 .gh 文件，提取組件資訊"""
    tree = ET.parse(gh_path)
    root = tree.getroot()

    components = []
    # 查找所有 GHPython 組件
    for obj in root.findall(".//Object"):
        guid = obj.get('InstanceGuid')
        message = obj.find('.//Message').text if obj.find('.//Message') is not None else ''

        components.append({
            'guid': guid,
            'version': message
        })

    return components

def check_outdated(gh_path, manifest_path):
    """檢查需要更新的組件"""
    components = parse_gh_file(gh_path)
    manifest = json.load(open(manifest_path))

    outdated = []
    for comp in components:
        manifest_comp = next((c for c in manifest['components'] if c['guid'] == comp['guid']), None)
        if manifest_comp and comp['version'] < manifest_comp['version']:
            outdated.append({
                'name': manifest_comp['name'],
                'current': comp['version'],
                'latest': manifest_comp['version']
            })

    return outdated

# 使用
outdated = check_outdated('myfile.gh', 'manifest.json')
for comp in outdated:
    print(f"{comp['name']}: {comp['current']} → {comp['latest']}")
```

## 參考資源

- [Ladybug Versioner](https://docs.ladybug.tools/ladybug-primer/components/5_version/versioner)
- [Sync Grasshopper File](https://docs.ladybug.tools/ladybug-primer/components/5_version/sync_grasshopper_file)
- [Ladybug Versioner Source Code](https://github.com/ladybug-tools/ladybug-grasshopper/blob/master/ladybug_grasshopper/src/LB%20Versioner.py)

---

**作者**: Claude Code
**日期**: 2025-12-30
**版本**: 1.0
