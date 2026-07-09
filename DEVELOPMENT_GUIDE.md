# Grasshopper Component Development Guide
## 使用 compas-actions.ghpython_components 開發自定義組件

---

## 📋 目錄

1. [專案概述](#專案概述)
2. [環境設置](#環境設置)
3. [組件結構](#組件結構)
4. [開發流程](#開發流程)
5. [實戰範例：YOLO UDP Receiver](#實戰範例yolo-udp-receiver)
6. [常見問題](#常見問題)
7. [進階技巧](#進階技巧)

---

## 專案概述

### 什麼是 compas-actions.ghpython_components？

這是一個將 Python 代碼轉換為 Grasshopper `.ghuser` 組件的工具。它讓你可以：

- ✅ 用文本編輯器編寫 Grasshopper 組件
- ✅ 使用版本控制（Git）管理組件代碼
- ✅ 支持 CPython (Python 3.9) for Rhino 8
- ✅ 自動生成 `.ghuser` 文件

### 系統架構

```
components/              # 組件源代碼目錄
├── MyComponent/         # 每個組件一個資料夾
│   ├── code.py          # Python 代碼
│   ├── metadata.json    # 組件配置
│   └── icon.png         # 24x24 圖標
│
dist/                    # 生成的 .ghuser 文件
└── MyComponent.ghuser
```

---

## 環境設置

### 1. 前置需求

- macOS (Apple Silicon)
- Rhino 8
- Miniconda/Anaconda
- 已配置的 `gh_timber` conda 環境

### 2. 確認環境

```bash
# 檢查 conda 環境
conda env list

# 應該看到 gh_timber 環境
# gh_timber   /opt/homebrew/Caskroom/miniconda/base/envs/gh_timber
```

### 3. 快速啟動

**方法 1: 使用 Alias（推薦）**

在你的 `~/.zshrc` 中已經設置了：

```bash
alias gh_comp='cd /Users/laihongyi/Downloads/compas-actions.ghpython_components && /opt/homebrew/Caskroom/miniconda/base/envs/gh_timber/bin/python componentize_cpy.py components dist --version "0.1.0"'
```

直接使用：
```bash
gh_comp
```

**方法 2: 手動執行**

```bash
cd /Users/laihongyi/Downloads/compas-actions.ghpython_components
conda activate gh_timber
python componentize_cpy.py components dist --version "0.1.0"
```

---

## 組件結構

### 1. 資料夾結構

每個組件需要三個文件：

```
components/MyComponent/
├── code.py          # Python 代碼（必需）
├── metadata.json    # 配置文件（必需）
└── icon.png         # 圖標（必需，24x24）
```

### 2. code.py 結構

對於 CPython (Rhino 8)，使用 `executingcomponent` 格式：

```python
"""
Component Description

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        output1: Description of output1
        output2: Description of output2
"""

from ghpythonlib.componentbase import executingcomponent as component
import Rhino.Geometry as rg

class MyComponent(component):
    def RunScript(self, param1, param2):
        ghenv.Component.Message = 'v{{version}}'

        # Your code here
        output1 = None
        output2 = None

        return (output1, output2)
```

**重要說明：**
- `{{version}}` 會被替換為命令行指定的版本號
- `RunScript` 的參數要與 `metadata.json` 的 `inputParameters` 對應
- 返回值要與 `metadata.json` 的 `outputParameters` 對應

### 3. metadata.json 結構

```json
{
    "name": "Component Name",
    "nickname": "Nick",
    "category": "Category Tab",
    "subcategory": "Panel Name",
    "description": "What this component does",
    "exposure": 2,
    "instanceGuid": "unique-guid-here",
    "ghpython": {
        "marshalGuids": true,
        "iconDisplay": 2,
        "inputParameters": [
            {
                "name": "param1",
                "nickname": "p1",
                "description": "Parameter description",
                "optional": true,
                "scriptParamAccess": "item",
                "typeHintID": "float"
            }
        ],
        "outputParameters": [
            {
                "name": "output1",
                "nickname": "out1",
                "description": "Output description",
                "optional": false
            }
        ]
    }
}
```

**重要屬性說明：**

- `category`: 組件在 Grasshopper 中的分類頁籤
- `subcategory`: 組件在頁籤中的面板
- `exposure`: 組件在面板中的位置
  - `2`: Primary (第一區)
  - `4`: Secondary (第二區)
- `scriptParamAccess`: 參數訪問模式
  - `"item"`: 單個值
  - `"list"`: 列表
  - `"tree"`: 數據樹
- `typeHintID`: 類型提示
  - `"float"`, `"int"`, `"str"`, `"bool"`
  - `"point"`, `"vector"`, `"plane"`
  - `"curve"`, `"surface"`, `"brep"`, `"mesh"`

### 4. icon.png

- 尺寸：24x24 像素
- 格式：PNG
- 可以從現有組件複製開始

---

## 開發流程

### 完整開發週期

```bash
# 1. 創建組件資料夾
mkdir -p components/MyComponent

# 2. 複製圖標模板（或創建自己的）
cp components/Test_GhTimber/icon.png components/MyComponent/icon.png

# 3. 創建 metadata.json
# （使用文本編輯器編寫）

# 4. 創建 code.py
# （使用文本編輯器編寫）

# 5. 生成 .ghuser 文件
gh_comp

# 6. 檢查生成結果
ls -lh dist/

# 7. 安裝到 Grasshopper
# 在 Grasshopper: File > Special Folders > User Object Folder
# 複製 dist/MyComponent.ghuser 到該資料夾

# 8. 重啟 Grasshopper 測試

# 9. 修改代碼後重複步驟 5-8
```

### 快速迭代技巧

1. **使用監聽模式**（可選）

   你可以創建一個 watch script 來自動檢測變化：

   ```bash
   # watch.sh
   while true; do
       fswatch -1 components/
       gh_comp
       echo "Components rebuilt at $(date)"
   done
   ```

2. **版本號管理**

   開發時使用固定版本號：
   ```bash
   gh_comp  # 使用預設 0.1.0
   ```

   發布時指定版本：
   ```bash
   python componentize_cpy.py components dist --version "1.0.0"
   ```

---

## 實戰範例：YOLO UDP Receiver

### 背景

我們要創建一個組件來接收 YOLOv8 姿態偵測的 UDP 數據，並在 Grasshopper 中顯示關鍵點位置。

### 系統架構

```
[攝影機] → [YOLOv8] → [UDP:9999] → [Grasshopper Component] → [Point3d]
          opencv2gh_yolov8.py      YOLO_UDP_Receiver.ghuser
```

### 步驟 1: 創建組件結構

```bash
mkdir -p components/YOLO_UDP_Receiver
cp components/Test_GhTimber/icon.png components/YOLO_UDP_Receiver/icon.png
```

### 步驟 2: 編寫 metadata.json

創建 `components/YOLO_UDP_Receiver/metadata.json`：

```json
{
    "name": "YOLO UDP Receiver",
    "nickname": "YOLO_UDP",
    "category": "YOLO",
    "subcategory": "Network",
    "description": "Receives YOLOv8 pose detection data via UDP and outputs keypoint positions",
    "exposure": 2,
    "instanceGuid": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "ghpython": {
        "marshalGuids": true,
        "iconDisplay": 2,
        "inputParameters": [
            {
                "name": "port",
                "nickname": "port",
                "description": "UDP port number (default: 9999)",
                "optional": true,
                "scriptParamAccess": "item",
                "typeHintID": "int"
            },
            {
                "name": "target_joint",
                "nickname": "joint",
                "description": "Target joint name",
                "optional": true,
                "scriptParamAccess": "item",
                "typeHintID": "str"
            }
        ],
        "outputParameters": [
            {
                "name": "point",
                "nickname": "pt",
                "description": "Target joint position as Point3d"
            },
            {
                "name": "x",
                "nickname": "x",
                "description": "X coordinate"
            },
            {
                "name": "y",
                "nickname": "y",
                "description": "Y coordinate"
            },
            {
                "name": "all_points",
                "nickname": "all_pts",
                "description": "All detected keypoints"
            },
            {
                "name": "joint_names",
                "nickname": "names",
                "description": "List of joint names"
            },
            {
                "name": "message",
                "nickname": "msg",
                "description": "Status message"
            }
        ]
    }
}
```

### 步驟 3: 編寫 code.py

創建 `components/YOLO_UDP_Receiver/code.py`：

```python
"""
YOLO UDP Receiver - Grasshopper Component
Receives YOLOv8 pose detection data via UDP

    Args:
        port: UDP port number (default: 9999)
        target_joint: Target joint name

    Returns:
        point: Target joint position as Point3d
        x, y, z: Coordinates
        all_points: All keypoints
        joint_names: Joint names list
        message: Status message
"""

from ghpythonlib.componentbase import executingcomponent as component

import clr
clr.AddReference("System")
clr.AddReference("RhinoCommon")

from System.Net import IPEndPoint, IPAddress
from System.Net.Sockets import Socket, AddressFamily, SocketType, ProtocolType
from System.Net.Sockets import SocketOptionLevel, SocketOptionName
from System.Text import Encoding
import Rhino.Geometry as rg
import System


class YOLOUDPReceiver(component):
    # Class variables to maintain state
    _udp_socket = None
    _keypoints = {}

    @staticmethod
    def parse_json(text):
        """Simple JSON parser"""
        result = {}
        text = text.strip('{}').replace('"', '').replace(' ', '')
        for pair in text.split(','):
            if ':' not in pair:
                continue
            k, v = pair.split(':', 1)
            try:
                result[k] = float(v) if '.' in v else int(v)
            except:
                result[k] = v
        return result

    def RunScript(self, port, target_joint):
        ghenv.Component.Message = 'v{{version}}'

        # Initialize outputs
        point = rg.Point3d(0.0, 0.0, 0.0)
        x = y = z = 0.0
        all_points = []
        joint_names = []
        message = "Initializing..."

        try:
            # Setup
            port_num = int(port) if port else 9999
            target = str(target_joint).strip() if target_joint else "left_wrist"

            # Create socket if needed
            if YOLOUDPReceiver._udp_socket is None:
                YOLOUDPReceiver._udp_socket = Socket(
                    AddressFamily.InterNetwork,
                    SocketType.Dgram,
                    ProtocolType.Udp
                )
                YOLOUDPReceiver._udp_socket.Blocking = False
                YOLOUDPReceiver._udp_socket.SetSocketOption(
                    SocketOptionLevel.Socket,
                    SocketOptionName.ReuseAddress,
                    True
                )
                YOLOUDPReceiver._udp_socket.Bind(
                    IPEndPoint(IPAddress.Parse("127.0.0.1"), port_num)
                )

            # Receive data
            buffer = System.Array.CreateInstance(System.Byte, 8192)
            for _ in range(50):
                try:
                    n = YOLOUDPReceiver._udp_socket.Receive(buffer)
                    if n > 0:
                        text = Encoding.UTF8.GetString(buffer, 0, n)
                        data = self.parse_json(text)

                        if 'keypoint' in data.get('type', ''):
                            name = data.get('name', '')
                            if name:
                                YOLOUDPReceiver._keypoints[name] = {
                                    'x': float(data.get('x', 0)),
                                    'y': float(data.get('y', 0)),
                                    'confidence': float(data.get('confidence', 1.0))
                                }
                except:
                    break

            # Process target joint
            if target in YOLOUDPReceiver._keypoints:
                kp = YOLOUDPReceiver._keypoints[target]
                x = float(kp['x']) * 100.0
                y = float(kp['y']) * 100.0
                z = 0.0
                point = rg.Point3d(x, y, z)
                message = "OK: {}".format(target)
            else:
                message = "No data for '{}'".format(target)

            # Process all joints
            for name in sorted(YOLOUDPReceiver._keypoints.keys()):
                kp = YOLOUDPReceiver._keypoints[name]
                pt = rg.Point3d(float(kp['x']) * 100.0, float(kp['y']) * 100.0, 0.0)
                all_points.append(pt)
                joint_names.append(name)

        except Exception as e:
            message = "ERROR: {}".format(str(e))

        return (point, x, y, z, all_points, joint_names, message)
```

### 步驟 4: 生成組件

```bash
gh_comp
```

輸出：
```
GHPython componentizer
======================
[x] Source: .../components (2 components)
[x] Target: .../dist
Processing component bundles:
  [x] YOLO_UDP_Receiver => .../dist/YOLO_UDP_Receiver.ghuser
  [x] Test_GhTimber => .../dist/Test_GhTimber.ghuser
```

### 步驟 5: 安裝到 Grasshopper

1. 打開 Grasshopper
2. `File > Special Folders > User Object Folder`
3. 複製 `dist/YOLO_UDP_Receiver.ghuser` 到該資料夾
4. 重啟 Grasshopper

### 步驟 6: 使用組件

1. 在 Grasshopper 中找到組件（在 `YOLO > Network` 分類下）
2. 拖放到畫布上
3. 連接輸入：
   - `port`: 9999（或其他端口）
   - `joint`: "left_wrist"（或其他關鍵點名稱）
4. 在外部運行 `opencv2gh_yolov8.py` 來發送數據
5. 查看輸出的 Point3d

### 可用的關鍵點名稱

YOLO Pose 提供 17 個關鍵點：

```python
- "nose"           # 鼻子
- "left_eye"       # 左眼
- "right_eye"      # 右眼
- "left_ear"       # 左耳
- "right_ear"      # 右耳
- "left_shoulder"  # 左肩
- "right_shoulder" # 右肩
- "left_elbow"     # 左肘
- "right_elbow"    # 右肘
- "left_wrist"     # 左手腕
- "right_wrist"    # 右手腕
- "left_hip"       # 左髖
- "right_hip"      # 右髖
- "left_knee"      # 左膝
- "right_knee"     # 右膝
- "left_ankle"     # 左腳踝
- "right_ankle"    # 右腳踝
```

---

## 常見問題

### Q1: 組件化後找不到組件？

**A:** 檢查以下幾點：

1. 確認 `.ghuser` 文件已複製到正確位置
   ```bash
   ls ~/Library/Application\ Support/McNeel/Rhinoceros/8.0/Plug-ins/Grasshopper\ \(b45a29b1-4343-4035-989e-044e8580d9cf\)/UserObjects/
   ```

2. 確認已重啟 Grasshopper

3. 檢查組件的 `category` 和 `subcategory` 設置

### Q2: 組件報錯 "module not found"？

**A:** 這通常是因為組件試圖 import 不存在的模塊。

**解決方案：**

1. 確保所有 import 都是 Rhino/Grasshopper 內建的
2. 如需外部套件，需要額外配置 Python 路徑

### Q3: 如何在組件之間共享代碼？

**A:** 創建一個 Python 模塊並在 `code.py` 中 import：

```python
# 在專案根目錄創建 mylib.py
# components/MyComponent/code.py
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import mylib
```

### Q4: 如何調試組件？

**A:** 使用輸出參數顯示調試信息：

```python
def RunScript(self, input1):
    debug = []

    debug.append("Input: {}".format(input1))
    debug.append("Type: {}".format(type(input1)))

    # ... your code ...

    debug_output = "\n".join(debug)
    return (result, debug_output)
```

在 `metadata.json` 中添加 debug 輸出參數。

### Q5: 組件更新後沒有變化？

**A:** `.ghuser` 組件有一個重要限制：

> 一旦組件被放置到文件中，它就變成了普通的 GHPython 組件，不會自動更新。

**解決方案：**

1. 刪除舊組件
2. 從組件面板拖入新組件
3. 重新連接

### Q6: 如何生成唯一的 GUID？

**A:** 使用 Python：

```bash
python3 -c "import uuid; print(uuid.uuid4())"
```

或線上工具：https://www.uuidgenerator.net/

---

## 進階技巧

### 1. 保持組件狀態

使用類變數保存狀態（如 socket 連接）：

```python
class MyComponent(component):
    _socket = None  # 類變數，在所有實例間共享

    def RunScript(self, input1):
        if MyComponent._socket is None:
            MyComponent._socket = create_socket()
        # ...
```

### 2. 多版本支持

使用版本號模板：

```python
def RunScript(self, input1):
    ghenv.Component.Message = 'v{{version}}'
    # ...
```

生成時指定版本：
```bash
python componentize_cpy.py components dist --version "1.2.3"
```

### 3. 條件輸出

根據輸入動態決定輸出：

```python
def RunScript(self, mode, data):
    if mode == "A":
        return (result_a, None)
    else:
        return (None, result_b)
```

### 4. 錯誤處理最佳實踐

```python
def RunScript(self, input1):
    try:
        result = process(input1)
        message = "OK"
        error = None
    except Exception as e:
        result = None
        message = "Error"
        error = str(e)

    return (result, message, error)
```

### 5. 性能優化

對於大數據處理：

```python
def RunScript(self, data_list):
    # 使用列表推導式而非循環
    results = [process(x) for x in data_list]

    # 避免重複計算
    if not hasattr(self, '_cache'):
        self._cache = expensive_computation()

    return results
```

---

## 附錄

### 完整的專案結構

```
compas-actions.ghpython_components/
├── components/              # 源代碼
│   ├── Test_GhTimber/
│   │   ├── code.py
│   │   ├── metadata.json
│   │   └── icon.png
│   └── YOLO_UDP_Receiver/
│       ├── code.py
│       ├── metadata.json
│       └── icon.png
│
├── dist/                    # 生成的組件
│   ├── Test_GhTimber.ghuser
│   └── YOLO_UDP_Receiver.ghuser
│
├── originalcode/            # 原始代碼參考
│   ├── opencv2gh_yolov8.py
│   └── gh_udp_receiver_final.py
│
├── componentize_cpy.py      # 組件化腳本
├── environment.yml          # Conda 環境
├── python.runtimeconfig.json
├── SETUP_FIXES.md          # 環境設置
├── QUICKSTART.md           # 快速開始
├── README.md               # 專案說明
└── DEVELOPMENT_GUIDE.md    # 本文檔
```

### 參考資源

- [Grasshopper Python Guide](https://developer.rhino3d.com/guides/rhinopython/)
- [RhinoCommon API](https://developer.rhino3d.com/api/RhinoCommon/)
- [compas-actions GitHub](https://github.com/compas-dev/compas-actions)
- [GH_IO Documentation](https://developer.rhino3d.com/api/grasshopper/html/R_Project_GH_IO.htm)

---

## 進階技巧：熱重載機制

### 什麼是熱重載？

熱重載（Hot Reload）讓你在開發過程中修改代碼後，無需重啟 Grasshopper 或重新生成 .ghuser 文件，就能立即看到效果。

### 實作方式

#### 1. 分離邏輯到外部套件

**傳統方式（無熱重載）**：
```python
# components/MyComponent/code.py
class MyComponent(component):
    def RunScript(self, x, y):
        # 所有邏輯都寫在這裡（155+ 行）
        result = x + y
        return result
```

修改邏輯 → 需要 `gh_comp` → 需要重啟 GH → 才能看到效果 ❌

**熱重載方式**：
```python
# components/MyComponent/code.py
import my_logic_package
import importlib

# 強制重載套件
importlib.reload(my_logic_package)

class MyComponent(component):
    def RunScript(self, x, y):
        # 調用外部套件
        result = my_logic_package.calculate(x, y)
        return result
```

修改邏輯 → 在 GH 中重新計算 → 立即看到效果 ✅

#### 2. YOLO UDP Receiver 實例

**套件結構**：
```
gh_yolo_udp/
├── __init__.py
└── gh_yolo_udp.py    # 核心邏輯（196 行）
```

**組件代碼**（簡化到 31 行）：
```python
# components/YOLO_UDP_Receiver/code.py
from ghpythonlib.componentbase import executingcomponent as component
import gh_yolo_udp
import gh_yolo_udp.gh_yolo_udp
import importlib

# 強制重載（重要！）
importlib.reload(gh_yolo_udp.gh_yolo_udp)  # 先重載子模組
importlib.reload(gh_yolo_udp)              # 再重載主模組

class YOLOUDPReceiver(component):
    def RunScript(self, enable, port, target_joint):
        self.Message = 'v{{version}}'

        # 所有邏輯都在外部套件中
        result = gh_yolo_udp.get_pose_data(enable, port, target_joint)

        return (
            result["point"],
            result["x"],
            result["y"],
            result["z"],
            result["all_points"],
            result["joint_names"],
            result["message"],
            result["debug"]
        )
```

**外部套件**（可以熱重載）：
```python
# gh_yolo_udp/gh_yolo_udp.py
def get_pose_data(enable, port, target_joint):
    """核心邏輯函數 - 可以隨時修改"""

    # 所有複雜邏輯都在這裡
    # Socket 處理、JSON 解析、座標轉換等

    # 修改這裡的代碼後，只需在 GH 中重新計算組件即可！
    scale_factor = 100.0  # 修改縮放係數
    x = kp['x'] * scale_factor

    return {
        "point": point,
        "x": x,
        "y": y,
        ...
    }
```

#### 3. 開發流程對比

**無熱重載**：
```bash
1. 修改 components/MyComponent/code.py
2. 執行 gh_comp（重新生成 .ghuser）
3. 複製到 UserObjects 資料夾
4. 重啟 Grasshopper
5. 測試
```
⏱️ **每次修改需要 2-5 分鐘**

**有熱重載**：
```bash
1. 修改 my_logic_package/logic.py
2. 在 Grasshopper 中按 F5（或重新計算組件）
3. 測試
```
⏱️ **每次修改需要 1-2 秒**

#### 4. 熱重載最佳實踐

**DO ✅**：
- 將複雜邏輯分離到外部套件
- 在組件 code.py 中使用 `importlib.reload()`
- 先重載子模組，再重載主模組
- 使用模組級變數保持狀態（如 socket）

**DON'T ❌**：
- 不要把所有代碼寫在 code.py 中
- 不要忘記 reload 子模組
- 不要在重載時依賴舊的類實例

#### 5. 重載順序很重要

```python
# ❌ 錯誤順序
importlib.reload(my_package)
importlib.reload(my_package.submodule)  # 太晚了！

# ✅ 正確順序
importlib.reload(my_package.submodule)  # 先重載子模組
importlib.reload(my_package)            # 再重載主模組
```

#### 6. 狀態管理

使用模組級變數保持狀態：
```python
# gh_yolo_udp/gh_yolo_udp.py
_udp_socket = None  # 模組級變數
_keypoints = {}

def get_pose_data(enable, port, target_joint):
    global _udp_socket, _keypoints

    # 重載時這些變數會重置為 None/{}
    # 所以需要檢查並重新初始化
    if _udp_socket is None and enable:
        _udp_socket = create_socket()
```

#### 7. 除錯技巧

在除錯訊息中顯示套件路徑：
```python
debug_lines.append("Loaded from: " + __file__)
# 輸出: Loaded from: /path/to/gh_yolo_udp/gh_yolo_udp.py
```

這樣你可以確認是否載入了正確版本的代碼。

### 優勢總結

| 特性 | 傳統方式 | 熱重載方式 |
|------|---------|-----------|
| 修改後重新測試時間 | 2-5 分鐘 | 1-2 秒 |
| 需要重啟 GH | ✅ 需要 | ❌ 不需要 |
| 需要重新生成 .ghuser | ✅ 需要 | ❌ 不需要 |
| code.py 複雜度 | 高（155+ 行）| 低（31 行）|
| 可測試性 | 困難 | 容易 |
| 開發效率 | ⭐⭐ | ⭐⭐⭐⭐⭐ |

### 何時使用熱重載？

**適合**：
- ✅ 開發階段，需要頻繁調整邏輯
- ✅ 複雜組件（100+ 行代碼）
- ✅ 需要除錯和測試的組件
- ✅ 團隊協作開發

**不適合**：
- ❌ 簡單組件（< 50 行）
- ❌ 已經穩定的生產組件
- ❌ 不需要頻繁修改的組件

---

## 更新日誌

- **2025-12-30**: 新增熱重載機制說明與 gh_yolo_udp 範例
- **2025-12-21**: 初始版本，包含 YOLO UDP Receiver 範例
- 添加完整的開發流程說明
- 添加常見問題解答

---

**作者**: Claude Code
**最後更新**: 2025-12-30
**專案版本**: 0.1.0
