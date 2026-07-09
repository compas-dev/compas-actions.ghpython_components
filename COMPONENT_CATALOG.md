# Component Catalog - 組件目錄

本專案包含的所有 Grasshopper 組件詳細說明。

---

## 📊 組件總覽

| 組件名稱 | 版本 | 分類 | 檔案大小 | 狀態 |
|---------|------|------|---------|------|
| [Component Updater](#component-updater) | v0.1.0 | Utilities > Version | 7.1 KB | ✅ 穩定 |
| [Swarm Dynamics](#swarm-dynamics) | v0.1.0 | Physics > Simulation | 9.8 KB | ✅ 穩定 |
| [YOLO UDP Receiver](#yolo-udp-receiver) | v0.1.0 | YOLO > Network | 4.3 KB | ✅ 穩定 |
| [Test GhTimber](#test-ghtimber) | v0.1.0 | GhTimber > Utilities | 3.1 KB | 📝 範例 |

---

## Component Updater

**版本管理與更新工具**

### 基本資訊

- **完整名稱**: Component Updater
- **暱稱**: Updater
- **分類**: Utilities > Version
- **GUID**: `c7d8e9f0-a1b2-3456-cdef-678901234567`
- **版本**: v0.1.0
- **文檔**: [components/Component_Updater/README.md](components/Component_Updater/README.md)

### 功能描述

檢查並管理 Grasshopper 畫布上組件的版本，靈感來自 Ladybug Tools 的 "Sync Grasshopper File" 組件。

**核心功能**：
- ✅ 掃描畫布上的所有組件
- ✅ 比對組件版本號
- ✅ 偵測 input/output 參數變化
- ✅ 生成詳細的版本檢查報告
- 🚧 自動更新組件（開發中）

### 參數說明

#### 輸入參數（3個）

| 參數 | 類型 | 必填 | 預設值 | 說明 |
|------|------|------|--------|------|
| check | Boolean | 否 | False | 檢查版本 |
| update | Boolean | 否 | False | 執行更新（開發中）|
| manifest_path | String | 否 | 自動偵測 | manifest.json 路徑 |

#### 輸出參數（4個）

| 參數 | 類型 | 說明 |
|------|------|------|
| report | String | 詳細的版本檢查報告 |
| outdated | List | 需要更新的組件清單 |
| updated | List | 已更新的組件清單（開發中）|
| errors | List | 錯誤訊息 |

### 使用範例

```python
# 在 Grasshopper 中
1. 放置 Component Updater 組件
2. check = True
3. 查看 report 輸出

輸出範例：
==================================================
組件版本檢查報告
==================================================

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
```

### 技術特色

- 使用 `manifest.json` 管理組件版本
- Semantic Versioning 版本比對
- 參數相容性智能檢測
- 自動搜尋 manifest.json 位置

### 相關文檔

- [VERSION_MANAGEMENT.md](VERSION_MANAGEMENT.md) - 版本管理系統設計
- [manifest.json](manifest.json) - 組件版本清單

---

## Swarm Dynamics

**粒子群體動力學模擬系統**

### 基本資訊

- **完整名稱**: Swarm Dynamics
- **暱稱**: Swarm
- **分類**: Physics > Simulation
- **GUID**: `b5c6d7e8-f9a0-1234-bcde-567890abcdef`
- **版本**: v0.1.0
- **文檔**: [components/Swarm_Dynamics/README.md](components/Swarm_Dynamics/README.md)

### 功能描述

模擬具有粒子-彈簧系統的群體動力學，包含旋轉、呼吸和主動彈簧效果。

**核心特色**：
- 🔵 粒子與彈簧物理模擬
- 🔗 K-近鄰自動連接
- 🌀 全域旋轉效果
- 💨 呼吸效果（週期性伸縮）
- ⚡ 主動彈簧（動態長度變化）
- 🎯 Euler 積分法模擬

### 參數說明

#### 輸入參數（14個）

##### 基本參數

| 參數 | 類型 | 預設值 | 說明 |
|------|------|--------|------|
| N | int | 7 | 初始桿件數量 |
| Prec | int | 3 | 座標精度 |
| Seed | int | 1 | 隨機種子 |
| Box | Box | 100×100×10 | 粒子生成範圍 |

##### 物理參數

| 參數 | 類型 | 預設值 | 說明 |
|------|------|--------|------|
| Stiff | float | 1.5 | 彈簧剛度 |
| Damp | float | 0.12 | 阻尼係數 |
| Dt | float | 0.03 | 時間步長 |

##### 連接參數

| 參數 | 類型 | 預設值 | 說明 |
|------|------|--------|------|
| Knn | int | 4 | K-近鄰數量 |
| Radius | float | 0.0 | 連接半徑（0 = 無限制）|

##### 動畫參數

| 參數 | 類型 | 預設值 | 說明 |
|------|------|--------|------|
| Speed | float | 0.6 | 旋轉速度 (rad/s) |
| Amp | float | 0.0 | 呼吸振幅 |
| Act | float | 0.15 | 主動彈簧振幅 |

##### 控制參數

| 參數 | 類型 | 說明 |
|------|------|------|
| Start | bool | True 開始模擬 |
| Reset | bool | True 重置系統 |

#### 輸出參數（9個）

| 參數 | 類型 | 說明 |
|------|------|------|
| L | Line[] | 桿件線條 |
| Links | Line[] | 彈簧連接線 |
| Nodes | Point3d[] | 粒子位置 |
| MidPts | Point3d[] | 桿件中點 |
| Labels | String[] | 桿件長度標籤 |
| Lengths | float[] | 桿件長度 |
| t | float | 模擬時間 |
| Frame | int | 幀計數 |
| out | String | 除錯訊息 |

### 使用範例

#### 基本旋轉效果

```python
N = 10
Speed = 0.5      # 慢速旋轉
Amp = 0.0        # 無呼吸
Act = 0.2        # 中等彈簧振盪
Start = True
```

#### 複雜動態系統

```python
N = 15
Speed = 0.8      # 快速旋轉
Amp = 3.0        # 中等呼吸
Act = 0.25       # 強彈簧振盪
Stiff = 2.0      # 高剛度
Damp = 0.1       # 低阻尼
```

### 技術特色

- **物理模擬**: F = k * (L - L0(t))
- **動態自然長度**: L0(t) = L_init * (1 + Act * sin(Speed * t + phi))
- **K-近鄰演算法**: 自動建立最近鄰連接
- **類變數狀態**: 保持模擬狀態跨調用

### 應用場景

1. 建築結構動態分析
2. 藝術裝置動畫
3. 群體行為研究
4. 有機形態生成

---

## YOLO UDP Receiver

**YOLOv8 姿態偵測數據接收器**

### 基本資訊

- **完整名稱**: YOLO UDP Receiver
- **暱稱**: YOLO_UDP
- **分類**: YOLO > Network
- **GUID**: `a1b2c3d4-e5f6-7890-abcd-ef1234567890`
- **版本**: v0.1.0
- **原始代碼**: [originalcode/opencv2gh_yolov8.py](originalcode/opencv2gh_yolov8.py)

### 功能描述

接收 YOLOv8 姿態偵測系統通過 UDP 發送的關鍵點數據，並在 Grasshopper 中輸出為 Point3d 格式。

**核心功能**：
- 📡 UDP 網路通訊
- 🏃 支援 17 個人體關鍵點
- 📍 輸出 Point3d 座標
- 🔍 簡單 JSON 解析（無外部依賴）
- ⚡ 高性能（50 次讀取循環）

### 參數說明

#### 輸入參數（2個）

| 參數 | 類型 | 預設值 | 說明 |
|------|------|--------|------|
| port | int | 9999 | UDP 端口號 |
| target_joint | String | "left_wrist" | 目標關節名稱 |

#### 輸出參數（8個）

| 參數 | 類型 | 說明 |
|------|------|------|
| point | Point3d | 目標關節的 3D 座標 |
| x | float | X 座標 |
| y | float | Y 座標 |
| z | float | Z 座標（通常為 0）|
| all_points | Point3d[] | 所有偵測到的關鍵點 |
| joint_names | String[] | 關鍵點名稱列表 |
| message | String | 狀態訊息 |
| debug | String | 除錯資訊 |

### 支援的關鍵點

YOLO Pose 提供 17 個關鍵點（COCO 格式）：

```
上半身：
- nose (鼻子)
- left_eye, right_eye (眼睛)
- left_ear, right_ear (耳朵)
- left_shoulder, right_shoulder (肩膀)
- left_elbow, right_elbow (手肘)
- left_wrist, right_wrist (手腕)

下半身：
- left_hip, right_hip (髖部)
- left_knee, right_knee (膝蓋)
- left_ankle, right_ankle (腳踝)
```

### 使用範例

#### 系統架構

```
[攝影機] → [YOLOv8] → [UDP:9999] → [YOLO_UDP_Receiver] → [Point3d]
         opencv2gh_yolov8.py         Grasshopper Component
```

#### 基本使用

```python
# 1. 在外部運行 YOLO 發送端
python opencv2gh_yolov8.py

# 2. 在 Grasshopper 中
port = 9999
target_joint = "left_wrist"

# 3. 輸出
point → 手腕的 3D 座標
all_points → 所有 17 個關鍵點
```

#### 追蹤特定關節

```python
# 追蹤鼻子
target_joint = "nose"

# 追蹤右手
target_joint = "right_wrist"

# 追蹤左腳踝
target_joint = "left_ankle"
```

### 技術特色

- **無阻塞 Socket**: `Blocking = False`
- **批次讀取**: 50 次循環讀取
- **座標縮放**: 0-1 正規化 → 0-100 座標系
- **類變數狀態**: 保持 socket 和關鍵點數據
- **簡單 JSON 解析**: 不依賴外部庫

### 相關文件

- **發送端**: [originalcode/opencv2gh_yolov8.py](originalcode/opencv2gh_yolov8.py)
- **接收端範例**: [originalcode/gh_udp_receiver_final.py](originalcode/gh_udp_receiver_final.py)

### 應用場景

1. 互動裝置設計
2. 動作捕捉可視化
3. 人體姿態分析
4. 即時參數化設計

---

## Test GhTimber

**測試與範例組件**

### 基本資訊

- **完整名稱**: Timber
- **暱稱**: Timber
- **分類**: GhTimber > Utilities
- **GUID**: `cdd47086-f912-4b77-825b-6b79c3aaecc1`
- **版本**: v0.1.0
- **狀態**: 📝 範例組件

### 功能描述

簡單的測試組件，用於演示 compas-actions.ghpython_components 的基本用法。

**功能**：
- 計算木材體積（長 × 寬 × 高）
- 演示 executingcomponent 基類用法
- 展示外部模組導入（gh_timber）

### 參數說明

#### 輸入參數（3個）

| 參數 | 類型 | 說明 |
|------|------|------|
| x | float | 長度 |
| y | float | 寬度 |
| z | float | 高度 |

#### 輸出參數（1個）

| 參數 | 類型 | 說明 |
|------|------|------|
| result | float | 體積（x * y * z）|

### 使用範例

```python
x = 100.0  # 長度
y = 50.0   # 寬度
z = 20.0   # 高度

result = 100000.0  # 體積
```

### 技術特色

- 使用 `executingcomponent` 基類
- 導入外部 Python 模組（gh_timber）
- 使用 `importlib.reload()` 支援熱重載
- 版本號顯示 `v{{version}}`

---

## 🔧 安裝與使用

### 安裝步驟

1. **下載組件**
   ```bash
   # 從 dist/ 資料夾獲取 .ghuser 文件
   ls dist/*.ghuser
   ```

2. **安裝到 Grasshopper**
   - 在 Grasshopper: `File > Special Folders > User Object Folder`
   - 複製 `.ghuser` 文件到該資料夾
   - 重啟 Grasshopper

3. **使用組件**
   - 在對應分類下找到組件
   - 拖放到畫布上使用

### 快速開始

詳細教學請參閱：
- [QUICKSTART.md](QUICKSTART.md) - 快速開始指南
- [DEVELOPMENT_GUIDE.md](DEVELOPMENT_GUIDE.md) - 完整開發教學

---

## 📊 版本資訊

### 當前版本

所有組件當前版本：**v0.1.0** (2025-12-30)

### 版本管理

- **manifest.json**: 組件版本清單
- **Component Updater**: 版本檢查工具
- **Semantic Versioning**: 版本號規範

詳見 [VERSION_MANAGEMENT.md](VERSION_MANAGEMENT.md)

---

## 🔗 相關資源

### 文檔

- [README.md](README.md) - 專案說明
- [DEVELOPMENT_GUIDE.md](DEVELOPMENT_GUIDE.md) - 開發指南
- [TEAM_COLLABORATION.md](TEAM_COLLABORATION.md) - 團隊協作
- [VERSION_MANAGEMENT.md](VERSION_MANAGEMENT.md) - 版本管理

### 範例代碼

- [originalcode/](originalcode/) - 原始參考代碼
  - opencv2gh_yolov8.py - YOLO 發送端
  - gh_udp_receiver_final.py - UDP 接收範例
  - gh_trajectory_robust.py - 軌跡處理範例

### 配置文件

- [manifest.json](manifest.json) - 組件版本清單
- [environment.yml](environment.yml) - Conda 環境配置
- [python.runtimeconfig.json](python.runtimeconfig.json) - .NET Runtime 配置

---

## 📝 授權

MIT License

---

**最後更新**: 2025-12-30
**維護者**: Claude Code
**專案**: https://github.com/fred1357944/compas-actions.ghpython_components
