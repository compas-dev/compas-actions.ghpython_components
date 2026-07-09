# YOLO UDP Receiver - YOLOv8 姿態偵測數據接收器

## 概述

YOLO UDP Receiver 是一個 Grasshopper 組件，用於接收 YOLOv8 姿態偵測系統通過 UDP 發送的人體關鍵點數據，並在 Grasshopper 中輸出為 Point3d 格式。

## 系統架構

```
┌─────────────────┐     UDP      ┌─────────────────────┐     Point3d    ┌─────────────┐
│  攝影機/視頻    │ ──────────▶ │  YOLOv8 + Python    │ ──────────────▶│  Grasshopper │
│                 │              │  opencv2gh_yolov8.py │    Port 9999   │  YOLO_UDP   │
└─────────────────┘              └─────────────────────┘                └─────────────┘
```

## 功能特色

- **17 個人體關鍵點支援**（COCO 格式）
- **即時數據接收**（非阻塞 Socket）
- **Enable/Disable 控制**（優雅開關 Socket）
- **熱重載支援**（修改邏輯無需重啟 GH）
- **簡單 JSON 解析**（無外部依賴）

## 安裝

### 1. 安裝 Grasshopper 組件

```bash
# 方法 A：從 dist/ 複製
cp dist/YOLO_UDP_Receiver.ghuser ~/Library/Application\ Support/McNeel/Rhinoceros/8.0/Plug-ins/Grasshopper/UserObjects/

# 方法 B：重新生成
gh_comp
```

### 2. 安裝 Python 發送端依賴

```bash
pip install ultralytics opencv-python
```

## 使用方法

### 步驟 1：啟動 YOLO 發送端

```bash
# 在專案根目錄執行
python opencv2gh_yolov8.py

# 或從 originalcode/ 執行
python originalcode/opencv2gh_yolov8.py
```

### 步驟 2：配置 Grasshopper 組件

1. 在 Grasshopper 中找到 `YOLO > Network > YOLO_UDP`
2. 拖放到畫布上
3. 連接參數：
   - `enable` = True（Boolean Toggle）
   - `port` = 9999（Number Slider 或直接輸入）
   - `target_joint` = "left_wrist"（Panel 或 Value List）

### 步驟 3：使用輸出數據

| 輸出 | 類型 | 說明 |
|------|------|------|
| `point` | Point3d | 目標關節的 3D 座標 |
| `x` | float | X 座標（0-100 範圍）|
| `y` | float | Y 座標（0-100 範圍）|
| `z` | float | Z 座標（通常為 0）|
| `all_points` | Point3d[] | 所有偵測到的關鍵點 |
| `joint_names` | String[] | 關鍵點名稱列表 |
| `message` | String | 狀態訊息 |
| `debug` | String | 除錯資訊 |

## 支援的關鍵點

YOLO Pose 提供 17 個關鍵點（COCO 格式）：

```
頭部：
├── nose（鼻子）
├── left_eye / right_eye（眼睛）
└── left_ear / right_ear（耳朵）

上半身：
├── left_shoulder / right_shoulder（肩膀）
├── left_elbow / right_elbow（手肘）
└── left_wrist / right_wrist（手腕）

下半身：
├── left_hip / right_hip（髖部）
├── left_knee / right_knee（膝蓋）
└── left_ankle / right_ankle（腳踝）
```

## 網路配置

### 預設設定

| 參數 | 預設值 | 說明 |
|------|--------|------|
| 協議 | UDP | 無連接，低延遲 |
| 地址 | 127.0.0.1 | 本機 |
| 端口 | 9999 | 可自訂 |
| 緩衝區 | 8192 bytes | 足夠容納單幀數據 |

### 自訂端口

**發送端（Python）**：
```python
# opencv2gh_yolov8.py
UDP_PORT = 9999  # 修改這裡
```

**接收端（Grasshopper）**：
```
port = 9999  # 修改 Number Slider
```

### 防火牆設定

如果在不同機器上運行：

```bash
# macOS - 允許 UDP 9999
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --add /path/to/python

# Windows - 允許 UDP 9999
netsh advfirewall firewall add rule name="YOLO UDP" dir=in action=allow protocol=UDP localport=9999
```

## 數據格式

### UDP 封包格式（JSON）

```json
{
  "type": "keypoint",
  "name": "left_wrist",
  "x": 0.456,
  "y": 0.789,
  "confidence": 0.95
}
```

### 座標轉換

| 來源 | 目標 | 公式 |
|------|------|------|
| YOLO (0-1) | GH (0-100) | `x_gh = x_yolo * 100` |
| 圖像座標 | 3D 座標 | `Point3d(x, y, 0)` |

## 熱重載開發

### 架構

```
YOLO_UDP_Receiver.ghuser
    ↓
components/YOLO_UDP_Receiver/code.py (31 行)
    ↓ importlib.reload()
gh_yolo_udp/gh_yolo_udp.py (196 行) ← 可隨時修改！
```

### 修改邏輯

1. 編輯 `gh_yolo_udp/gh_yolo_udp.py`
2. 修改 `scale_factor`、算法、任何邏輯
3. 在 Grasshopper 中按 F5 重新計算
4. **立即看到效果！**（無需重啟 GH）

### 範例：修改座標縮放

```python
# gh_yolo_udp/gh_yolo_udp.py 第 144 行
scale_factor = 100.0  # 修改為 200.0 試試
x = float(kp['x']) * scale_factor
```

## 常見問題

### Q1：無法接收數據

**檢查清單**：
- [ ] YOLO 發送端是否運行？
- [ ] 端口是否一致？（發送端 vs 接收端）
- [ ] `enable` 是否為 True？
- [ ] 防火牆是否阻擋？

**除錯方式**：
```python
# 查看 debug 輸出
# "Received 0 packets" → 發送端問題
# "Socket created" → 端口問題
# "No keypoints data" → JSON 解析問題
```

### Q2：數據延遲

**原因**：UDP 緩衝區堆積

**解決**：
- 組件每幀讀取 50 個封包以清空緩衝區
- 確保 GH 計時器間隔合適（建議 50-100ms）

### Q3：Socket 端口佔用

**錯誤訊息**：`Address already in use`

**解決**：
1. 設 `enable = False` 關閉現有 Socket
2. 等待 1-2 秒
3. 設 `enable = True` 重新連接

或：
```bash
# 強制釋放端口（macOS/Linux）
lsof -i :9999 | awk 'NR>1 {print $2}' | xargs kill -9
```

### Q4：找不到目標關節

**錯誤訊息**：`No 'left_wrist' (have: nose, left_eye...)`

**解決**：
- 確認 `target_joint` 拼寫正確
- 使用 `joint_names` 輸出查看可用關節
- 確認 YOLO 有偵測到該關節（信心度 > 0.5）

## 應用場景

### 1. 互動裝置設計

```
[攝影機] → [YOLO] → [Grasshopper] → [Arduino/LED]
         手勢追蹤    參數化設計      實體輸出
```

### 2. 動作捕捉可視化

```
[攝影機] → [YOLO] → [Grasshopper] → [Rhino 3D]
         骨架追蹤    幾何變換       3D 視覺化
```

### 3. 人機互動研究

```
[深度攝影機] → [YOLO] → [Grasshopper] → [數據分析]
             姿態偵測    空間分析      CSV/JSON
```

## 技術細節

### Socket 配置

```python
socket = Socket(AddressFamily.InterNetwork, SocketType.Dgram, ProtocolType.Udp)
socket.Blocking = False          # 非阻塞模式
socket.ReceiveTimeout = 10       # 10ms 超時
socket.SetSocketOption(SocketOptionLevel.Socket, SocketOptionName.ReuseAddress, True)
socket.Bind(IPEndPoint(IPAddress.Parse("127.0.0.1"), port))
```

### JSON 解析器

使用簡單字串解析（不依賴 json 庫）：

```python
def parse_json(text):
    result = {}
    text = text.strip('{}').replace('"', '').replace(' ', '')
    for pair in text.split(','):
        k, v = pair.split(':', 1)
        result[k] = float(v) if '.' in v else int(v)
    return result
```

**限制**：
- 不支援嵌套結構
- 不支援陣列
- 不支援特殊字符（逗號、冒號）

### 狀態管理

使用模組級變數保持狀態：

```python
# gh_yolo_udp/gh_yolo_udp.py
_udp_socket = None  # Socket 實例
_keypoints = {}     # 關鍵點快取

# Enable = False 時：
if not enable:
    _udp_socket.Close()
    _udp_socket = None
    _keypoints = {}
```

## 相關文件

- **發送端腳本**：`opencv2gh_yolov8.py`
- **核心邏輯套件**：`gh_yolo_udp/gh_yolo_udp.py`
- **原始參考代碼**：`originalcode/opencv2gh_yolov8.py`
- **開發指南**：`DEVELOPMENT_GUIDE.md`（熱重載章節）

## 版本歷史

- **v0.1.0** (2025-12-30)
  - 初始版本
  - 17 COCO 關鍵點支援
  - 非阻塞 Socket
  - 熱重載機制

- **v0.1.1** (2025-12-30)
  - 新增 `enable` 參數
  - 重構為外部套件架構
  - 優雅的 Socket 開關

---

**組件類別**：YOLO > Network
**GUID**：`a1b2c3d4-e5f6-7890-abcd-ef1234567890`
**版本**：v0.1.0
**作者**：Claude Code
**最後更新**：2025-12-30
