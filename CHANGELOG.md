# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Planned
- Component Updater 自動更新功能（Phase 2-3）
- 批次更新多個 .gh 文件
- 從 GitHub 自動下載最新組件
- 單元測試基礎設施
- Swarm_Dynamics KD-Tree 性能優化

---

## [0.1.1] - 2026-01-06

### 🎉 MVP Release - 專案品質優化

基於 Opus 模型的全面專案檢查，完成多項品質改進。專案評分從 7.5 提升至 8.3。

### ✨ Added - 新增

#### 組件文檔
1. **YOLO_UDP_Receiver README** (新增)
   - 完整系統架構說明
   - 網路配置指南（端口、防火牆）
   - 17 個 COCO 關鍵點參考
   - 熱重載開發流程
   - 常見問題與除錯指南

2. **Test_GhTimber README** (新增)
   - 組件用途說明
   - 模板使用指南
   - 技術特點說明

#### 專案管理
3. **TODO.md** (新增)
   - 完整待辦事項清單
   - 版本規劃（v0.2.0 → v1.0.0）
   - 專案狀態追蹤
   - 開發筆記時間線

4. **PR 模板** (新增)
   - `.github/PULL_REQUEST_TEMPLATE.md`
   - 標準化變更類型
   - 測試計劃檢查清單
   - 影響範圍說明

### 🔧 Changed - 變更

#### manifest.json 結構完善
- 新增 `$schema` 聲明
- 補完所有組件的 `description`
- 新增 `repository`、`license` 欄位
- 新增 Component_Updater（之前缺失）
- 更新 YOLO_UDP_Receiver inputs（含 enable 參數）
- 所有參數新增 `description`

#### environment.yml 依賴鎖定
- pythonnet 版本鎖定：`3.0.3`
- 移除未使用的 networkx
- 新增詳細註解說明
- 新增 channels 配置

#### CI/CD 工作流升級
- 新增 `validate` job（配置驗證）
- 驗證 manifest.json 結構
- 驗證組件目錄結構
- 更新 actions 版本（v4）
- 新增條件觸發（paths）

### 📊 專案評分

| 維度 | 之前 | 之後 |
|------|------|------|
| 文檔完整性 | 8.5/10 | 9/10 |
| 配置規範 | 7/10 | 8.5/10 |
| 可維護性 | 7.5/10 | 8.5/10 |
| **整體** | **7.5/10** | **8.3/10** |

---

## [0.1.0] - 2025-12-30

### 🎉 Initial Enhanced Fork Release

這是基於 compas-dev/compas-actions.ghpython_components 的增強版本，添加了完整的團隊協作和版本管理功能。

### ✨ Added - 新增功能

#### 新組件

1. **Component Updater** (v0.1.0)
   - 版本檢查工具（靈感來自 Ladybug Tools）
   - 掃描畫布上的組件並比對版本
   - 偵測 input/output 參數變化
   - 生成詳細的版本報告
   - 支援 manifest.json 版本管理
   - 分類: Utilities > Version
   - 檔案: `dist/Component_Updater.ghuser` (7.1 KB)

2. **Swarm Dynamics** (v0.1.0)
   - 粒子群體動力學模擬系統
   - 粒子-彈簧物理模擬
   - K-近鄰自動連接演算法
   - 全域旋轉與呼吸效果
   - 主動彈簧（動態長度變化）
   - Euler 積分法更新
   - 分類: Physics > Simulation
   - 檔案: `dist/Swarm_Dynamics.ghuser` (9.8 KB)

3. **YOLO UDP Receiver** (v0.1.0)
   - YOLOv8 姿態偵測 UDP 數據接收器
   - 支援 17 個人體關鍵點（COCO 格式）
   - 輸出 Point3d 座標
   - 無阻塞 Socket 通訊
   - 簡單 JSON 解析（無外部依賴）
   - 分類: YOLO > Network
   - 檔案: `dist/YOLO_UDP_Receiver.ghuser` (4.3 KB)

#### 版本管理系統

1. **manifest.json**
   - 集中管理所有組件版本資訊
   - 記錄 GUID、版本號、參數定義
   - 支援自動版本檢查

2. **Semantic Versioning 支援**
   - 版本號格式: MAJOR.MINOR.PATCH
   - 自動版本號替換（`{{version}}`）
   - 版本比對演算法

#### 文檔系統

1. **DEVELOPMENT_GUIDE.md**
   - 完整的組件開發教學
   - YOLO UDP Receiver 實戰範例
   - 組件結構詳解
   - 常見問題解答
   - 進階開發技巧

2. **TEAM_COLLABORATION.md**
   - 團隊協作最佳實踐
   - Git 工作流程
   - 為什麼適合小團隊開發
   - pip 套件管理優勢
   - 多人協作範例

3. **VERSION_MANAGEMENT.md**
   - 完整的版本管理系統設計
   - Ladybug Tools 研究成果
   - 技術實作細節
   - Phase 1/2/3 發展路線圖
   - MVP 與未來功能規劃

4. **COMPONENT_CATALOG.md**
   - 所有組件的詳細目錄
   - 參數說明與使用範例
   - 技術特色與應用場景
   - 安裝與使用指南

5. **CHANGELOG.md** (本文件)
   - 詳細的變更記錄
   - 版本歷史追蹤

6. **組件專屬 README**
   - `components/Swarm_Dynamics/README.md`
   - `components/Component_Updater/README.md`

#### 原始代碼參考

在 `originalcode/` 資料夾新增：
- `opencv2gh_yolov8.py` - YOLOv8 姿態偵測發送端
- `gh_udp_receiver_final.py` - UDP 接收器範例
- `gh_trajectory_robust.py` - 軌跡處理範例

### 🔧 Changed - 變更

#### README.md
- 新增 Enhanced Fork Features 區塊
- 新增組件總覽表格
- 新增 Quick Start 指南
- 新增文檔連結
- 新增 macOS ARM64 支援說明

#### SETUP_FIXES.md
- 新增詳細的故障排除步驟
- 新增 `ModuleNotFoundError: pythonnet` 解決方案
- 新增 conda 自動初始化說明
- 新增便捷 Alias 設定
- 更完整的分步驟指引

#### QUICKSTART.md
- 更新為當前專案路徑
- 新增 gh_comp alias 說明
- 更新 conda 環境設置步驟

### 🐛 Fixed - 修復

#### macOS ARM64 相容性
- 修復 pythonnet 3.x 與 Rhino 8 .NET 8.0 的相容性問題
- 新增 `python.runtimeconfig.json` 配置
- 更新 `componentize_cpy.py` 的 runtime 初始化邏輯
- 解決 conda activate 無效問題

#### 環境設置
- 修復 `env_path.txt` 路徑問題
- 新增 conda 自動初始化配置
- 更新 `.zshrc` 設置

### 🔒 Security - 安全性

- `.gitignore` 新增 `.claude/` 排除項目
- `env_path.txt` 保持在 `.gitignore` 中（本地配置）

### 📝 Documentation - 文檔改進

#### 新增文檔（7個）
1. DEVELOPMENT_GUIDE.md (54 KB)
2. TEAM_COLLABORATION.md (20 KB)
3. VERSION_MANAGEMENT.md (25 KB)
4. COMPONENT_CATALOG.md (18 KB)
5. CHANGELOG.md (本文件)
6. components/Swarm_Dynamics/README.md (9 KB)
7. components/Component_Updater/README.md (10 KB)

#### 更新文檔（3個）
1. README.md - 新增 Enhanced Fork Features
2. SETUP_FIXES.md - 新增故障排除
3. QUICKSTART.md - 更新快速開始指南

### 🛠️ Technical - 技術細節

#### 組件架構
- 使用 `executingcomponent` 基類（CPython）
- 類變數狀態管理
- 模板變數支援（`{{version}}`）
- metadata.json 配置驅動

#### 物理模擬（Swarm Dynamics）
- Euler 積分法
- 彈簧力計算: F = k * (L - L0)
- 動態自然長度
- K-近鄰演算法

#### 網路通訊（YOLO UDP Receiver）
- 無阻塞 Socket
- 批次讀取（50 次循環）
- 簡單 JSON 解析器
- 座標縮放轉換

#### 版本管理（Component Updater）
- 版本號解析演算法
- 參數相容性檢測
- manifest.json 自動搜尋
- 詳細報告生成

### 📦 Build System - 構建系統

#### 新增功能
- `manifest.json` 支援
- gh_comp alias（一鍵構建）
- 版本號自動替換
- 組件 GUID 管理

#### 環境配置
- `environment.yml` - Conda 環境定義
- `python.runtimeconfig.json` - .NET 8.0 配置
- `.gitignore` 更新

### 🎯 Project Goals - 專案目標

這個版本實現了以下目標：

1. ✅ **版本控制友善**
   - 所有代碼都是文本文件
   - Git 可以追蹤每一次變更
   - 支援 Pull Request 代碼審查

2. ✅ **團隊協作支援**
   - 統一的 conda 環境管理
   - manifest.json 版本追蹤
   - 詳細的協作文檔

3. ✅ **版本管理系統**
   - Component Updater 工具
   - Semantic Versioning
   - 版本檢查與報告

4. ✅ **完整文檔**
   - 開發指南
   - 團隊協作最佳實踐
   - 組件目錄
   - 變更日誌

5. ✅ **macOS ARM64 支援**
   - Apple Silicon 完整支援
   - pythonnet 3.x 配置
   - 詳細故障排除

---

## [0.0.0] - Before Fork

### Original compas-dev/compas-actions.ghpython_components

- 基本的組件化工具
- GitHub Actions 支援
- IronPython 和 CPython 支援
- 基本的 metadata.json 配置

---

## 版本號說明

使用 [Semantic Versioning](https://semver.org/)：

```
MAJOR.MINOR.PATCH

MAJOR: 重大更新，不向下相容（如 input/output 變化）
MINOR: 新增功能，向下相容
PATCH: Bug 修復，向下相容
```

**範例**：
- `0.1.0 → 0.2.0`: 新增功能（相容）
- `0.2.0 → 0.2.1`: Bug 修復（相容）
- `0.2.1 → 1.0.0`: 重大更新（不相容）

---

## 貢獻指南

### 如何新增變更記錄

1. 在 `[Unreleased]` 區塊下新增變更
2. 使用正確的分類：
   - `Added` - 新功能
   - `Changed` - 既有功能的變更
   - `Deprecated` - 即將移除的功能
   - `Removed` - 已移除的功能
   - `Fixed` - Bug 修復
   - `Security` - 安全性修復

3. 發布新版本時：
   - 將 `[Unreleased]` 內容移到新版本區塊
   - 更新日期
   - 更新 manifest.json 版本號

### Git Commit 格式

```
類型：簡短描述

詳細說明...

Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
```

**類型**：
- `新增` - 新功能
- `修復` - Bug 修復
- `更新` - 既有功能變更
- `文檔` - 文檔更新
- `優化` - 性能優化
- `重構` - 代碼重構

---

## 連結

- **專案**: https://github.com/fred1357944/compas-actions.ghpython_components
- **上游**: https://github.com/compas-dev/compas-actions.ghpython_components
- **問題回報**: https://github.com/fred1357944/compas-actions.ghpython_components/issues

---

**維護者**: Claude Code
**最後更新**: 2026-01-06
