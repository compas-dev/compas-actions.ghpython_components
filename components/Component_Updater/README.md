# Component Updater - 組件版本管理工具

## 概述

Component Updater 是一個用於檢查和管理 Grasshopper 畫布上組件版本的工具。靈感來自 Ladybug Tools 的 "Sync Grasshopper File" 組件。

## 功能特色

### ✅ 當前實作（MVP v0.1.0）

- **版本檢測**：掃描畫布上的所有組件，比對版本號
- **相容性檢查**：偵測 input/output 參數變化
- **詳細報告**：列出需要更新的組件及其狀態
- **manifest.json 支援**：使用 JSON 文件管理組件資訊

### 🚧 規劃中功能

- **自動更新**：一鍵替換畫布上的舊組件
- **連線保留**：更新時自動恢復參數連線
- **批次更新**：更新多個 .gh 文件
- **版本回退**：降級到舊版本

## 使用方法

### 步驟 1: 安裝組件

1. 複製 `dist/Component_Updater.ghuser` 到 Grasshopper UserObjects 資料夾
2. 重啟 Grasshopper
3. 在 `Utilities > Version` 分類下找到組件

### 步驟 2: 準備 manifest.json

確保專案根目錄有 `manifest.json` 文件（已自動生成）：

```json
{
  "name": "GH Timber Components",
  "version": "0.1.0",
  "components": [
    {
      "name": "YOLO_UDP_Receiver",
      "guid": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "version": "0.1.0",
      "inputs": [...],
      "outputs": [...]
    }
  ]
}
```

### 步驟 3: 檢查版本

1. 在 Grasshopper 中放置 Component Updater 組件
2. 連接一個 Boolean Toggle 到 `check` 輸入
3. 設定 `check = True`
4. 查看 `report` 輸出

**輸出範例**：

```
==================================================
組件版本檢查報告
==================================================

插件名稱: GH Timber Components
插件版本: 0.1.0

發現 2 個組件需要更新：

✅ YOLO_UDP_Receiver
   當前版本: v0.1.0
   最新版本: v0.2.0
   狀態: 可自動更新

⚠️ Swarm_Dynamics
   當前版本: v0.1.0
   最新版本: v0.2.0
   狀態: 需手動更新（參數已變更）
   - 新增輸入: Gravity
   - 移除輸出: Labels
```

## 輸入參數

| 參數 | 類型 | 說明 |
|------|------|------|
| **check** | Boolean | 設為 True 檢查版本 |
| **update** | Boolean | 設為 True 更新組件（開發中）|
| **manifest_path** | String | manifest.json 路徑（可選，自動偵測）|

## 輸出參數

| 輸出 | 類型 | 說明 |
|------|------|------|
| **report** | String | 詳細的版本檢查報告 |
| **outdated** | List | 需要更新的組件清單 |
| **updated** | List | 已更新的組件清單（開發中）|
| **errors** | List | 錯誤訊息 |

## 工作原理

### 1. 版本號嵌入

每個組件在 `code.py` 中設定版本號：

```python
def RunScript(self, ...):
    ghenv.Component.Message = 'v{{version}}'  # 會被替換為實際版本號
    # ...
```

### 2. 組件識別

使用 `instanceGuid` 識別組件類型：

```json
{
  "guid": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
}
```

### 3. 版本比對

```python
current_version = component.Message  # "v0.1.0"
latest_version = manifest['version']  # "0.2.0"

if parse_version(current_version) < parse_version(latest_version):
    needs_update = True
```

### 4. 相容性檢查

比對 input/output 參數名稱：

```python
current_inputs = {"port", "target_joint"}
manifest_inputs = {"port", "target_joint", "timeout"}  # 新增了 timeout

compatible = (current_inputs == manifest_inputs)  # False
```

## manifest.json 結構

### 完整範例

```json
{
  "name": "Your Plugin Name",
  "version": "0.2.0",
  "author": "Your Name",
  "description": "Plugin description",
  "components": [
    {
      "name": "Component_Name",
      "nickname": "Nick",
      "guid": "unique-guid-here",
      "version": "0.2.0",
      "category": "Category",
      "subcategory": "Subcategory",
      "ghuser_filename": "Component_Name.ghuser",
      "inputs": [
        {"name": "param1", "type": "float", "optional": true},
        {"name": "param2", "type": "int", "optional": false}
      ],
      "outputs": [
        {"name": "result", "type": "float"}
      ]
    }
  ]
}
```

### 更新 manifest.json

每次修改組件後，更新對應的版本號：

```json
{
  "name": "YOLO_UDP_Receiver",
  "version": "0.2.0",  // 更新這裡
  "inputs": [
    {"name": "port", "type": "int"},
    {"name": "target_joint", "type": "str"},
    {"name": "timeout", "type": "float"}  // 新增參數
  ]
}
```

## 版本號規範

使用 [Semantic Versioning](https://semver.org/)：

```
版本格式：MAJOR.MINOR.PATCH

MAJOR: 重大更新，不向下相容（input/output 變化）
MINOR: 新增功能，向下相容
PATCH: Bug 修復，向下相容

範例：
v1.0.0 → v1.1.0  (新增功能，相容)
v1.1.0 → v1.1.1  (Bug 修復，相容)
v1.1.1 → v2.0.0  (重大更新，不相容)
```

## 更新工作流程

### 場景 1: 無參數變化（可自動更新）

```
1. 修改組件代碼 (bug 修復、性能優化)
2. 更新版本號: v0.1.0 → v0.1.1
3. 更新 manifest.json
4. 執行 gh_comp 生成新 .ghuser
5. 安裝到 UserObjects
6. 在 GH 中使用 Component Updater 檢查
7. update = True (未來功能)
```

### 場景 2: 有參數變化（需手動更新）

```
1. 修改組件代碼 (新增/移除參數)
2. 更新版本號: v0.1.0 → v0.2.0  (MINOR 版本)
3. 更新 manifest.json (記錄新參數)
4. 執行 gh_comp
5. 安裝到 UserObjects
6. 在 GH 中使用 Component Updater 檢查
7. 查看報告，找出標記為 ⚠️ 的組件
8. 手動替換：
   - 從工具欄拖入新組件
   - 重新連接參數
   - 刪除舊組件
```

## 最佳實踐

### 1. 版本管理

```bash
# 每次修改組件後
1. 更新 components/XXX/code.py
2. 決定版本號（MAJOR/MINOR/PATCH）
3. 更新 manifest.json
4. gh_comp
5. git commit -m "更新：XXX 組件 v0.1.0 → v0.2.0"
```

### 2. 文檔更新

每次版本更新時，記錄變更：

```markdown
## 版本歷史

### v0.2.0 (2025-12-30)
- 新增 timeout 參數
- 修復 UDP 連線問題
- 優化性能

### v0.1.0 (2025-12-21)
- 初始版本
```

### 3. 測試流程

```
1. 創建測試 .gh 文件
2. 放置舊版本組件
3. 連接參數
4. 更新組件版本
5. 使用 Component Updater 檢查
6. 確認報告正確
7. 手動測試更新流程
```

## 限制與已知問題

### 當前限制（v0.1.0）

1. ❌ **無法自動更新**：只能檢查版本，無法自動替換組件
2. ❌ **需手動安裝**：需要手動複製 .ghuser 到 UserObjects
3. ⚠️ **manifest 路徑**：需要手動指定或放在特定位置

### 未來改進

- [ ] 實作自動更新功能
- [ ] 支援連線保留
- [ ] 批次更新多個文件
- [ ] 從 GitHub 自動下載最新版本
- [ ] 視覺化版本比對
- [ ] 更新預覽（顯示將要發生的變化）

## 技術細節

### Grasshopper API 限制

1. **無法程式化替換組件**：
   - Grasshopper SDK 不允許直接替換組件
   - 需要手動刪除舊組件並添加新組件

2. **連線資訊**：
   - 可以讀取 `param.Sources` 和 `param.Recipients`
   - 但無法程式化創建新組件實例

3. **解決方案**：
   - Phase 1: 只提供檢查功能（當前）
   - Phase 2: 研究 Grasshopper Kernel 深層 API
   - Phase 3: 可能需要 C# 插件支援

## 參考資源

### Ladybug Tools 實作

- [LB Versioner](https://docs.ladybug.tools/ladybug-primer/components/5_version/versioner)
- [Sync Grasshopper File](https://docs.ladybug.tools/ladybug-primer/components/5_version/sync_grasshopper_file)
- [Source Code](https://github.com/ladybug-tools/ladybug-grasshopper/blob/master/ladybug_grasshopper/src/LB%20Versioner.py)

### 相關文檔

- VERSION_MANAGEMENT.md - 完整設計文檔
- manifest.json - 組件版本資訊
- DEVELOPMENT_GUIDE.md - 組件開發指南

## 常見問題

### Q: 為什麼不能自動更新？

**A**: 當前版本（v0.1.0）是 MVP，只實作了版本檢查功能。自動更新需要：

1. 從 .ghuser 文件創建組件實例
2. 操作 Grasshopper Document
3. 處理參數連線

這些需要更深入的 Grasshopper SDK 研究。

### Q: manifest.json 放在哪裡？

**A**: 組件會自動搜尋以下位置：

1. 組件所在目錄
2. 專案根目錄
3. ~/Downloads/compas-actions.ghpython_components/

或者手動指定 `manifest_path`。

### Q: 如何處理不相容的更新？

**A**: 報告會標記為 ⚠️ 並列出變更：

```
⚠️ Component_Name
   當前版本: v0.1.0
   最新版本: v0.2.0
   狀態: 需手動更新（參數已變更）
   - 新增輸入: new_param
   - 移除輸出: old_output
```

需要手動替換組件。

### Q: 可以檢查其他人的組件嗎？

**A**: 可以！只要：

1. 有對應的 manifest.json
2. 組件使用 `Component.Message` 顯示版本號
3. 組件有唯一的 `ComponentGuid`

## 版本歷史

- **v0.1.0** (2025-12-30)
  - 初始 MVP 版本
  - 版本檢查功能
  - 相容性檢測
  - manifest.json 支援

---

**組件類別**：Utilities > Version
**作者**：Claude Code
**靈感來源**：Ladybug Tools Sync Grasshopper File
**最後更新**：2025-12-30
