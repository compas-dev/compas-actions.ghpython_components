# Test GhTimber - 測試與範例組件

## 概述

Test GhTimber 是一個簡單的測試組件，用於：
- 演示 compas-actions.ghpython_components 的基本組件結構
- 測試 gh_timber 模組的導入和熱重載機制
- 驗證 Grasshopper 組件化流程是否正常工作

## 功能

計算木材體積：`result = x × y × z`

## 使用方法

### 輸入參數

| 參數 | 類型 | 預設值 | 說明 |
|------|------|--------|------|
| x | float | 0 | 長度 |
| y | float | 0 | 寬度 |
| z | float | 0 | 高度 |

### 輸出參數

| 參數 | 類型 | 說明 |
|------|------|------|
| result | float | 體積（x × y × z）|

### 範例

```
輸入：
  x = 100.0
  y = 50.0
  z = 20.0

輸出：
  result = 100000.0
```

## 技術特點

### 1. executingcomponent 基類

```python
from ghpythonlib.componentbase import executingcomponent as component

class Timber(component):
    def RunScript(self, x, y, z):
        # 組件邏輯
        return result
```

### 2. 外部模組導入

```python
import gh_timber
import importlib
importlib.reload(gh_timber)  # 支援熱重載
```

### 3. 版本號模板

```python
ghenv.Component.Message = 'v{{version}}'  # 自動替換為實際版本
```

## 開發用途

### 測試組件化流程

```bash
# 1. 修改 components/Test_GhTimber/code.py
# 2. 執行構建
gh_comp

# 3. 檢查生成的文件
ls -la dist/Test_GhTimber.ghuser
```

### 測試 gh_timber 模組

```python
# gh_timber/__init__.py
def timber_volume(x, y, z):
    return x * y * z
```

修改 `gh_timber/__init__.py` 後，在 Grasshopper 中重新計算組件即可看到效果。

## 作為模板使用

創建新組件時，可以複製此組件作為模板：

```bash
# 1. 複製目錄
cp -r components/Test_GhTimber components/My_New_Component

# 2. 修改 metadata.json
#    - name, nickname, description
#    - category, subcategory
#    - instanceGuid（生成新的 UUID）
#    - inputParameters, outputParameters

# 3. 修改 code.py
#    - 類名
#    - RunScript 參數和邏輯

# 4. 替換 icon.png（24x24）

# 5. 構建
gh_comp
```

## 文件結構

```
components/Test_GhTimber/
├── code.py          # 組件邏輯（32 行）
├── metadata.json    # 組件配置
├── icon.png         # 24x24 圖標
└── README.md        # 本文檔
```

## 相關資源

- **gh_timber 模組**：`gh_timber/__init__.py`
- **開發指南**：`DEVELOPMENT_GUIDE.md`
- **組件目錄**：`COMPONENT_CATALOG.md`

---

**組件類別**：GhTimber > Utilities
**GUID**：`cdd47086-f912-4b77-825b-6b79c3aaecc1`
**版本**：v0.1.0
**狀態**：📝 範例組件
