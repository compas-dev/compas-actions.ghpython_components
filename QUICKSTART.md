# Quick Start Guide - 快速開始指南

本指南幫助你快速上手 compas-actions.ghpython_components 專案。

## 📋 目錄

1. [初次設置](#初次設置)
2. [每日開發流程](#每日開發流程)
3. [可用組件](#可用組件)
4. [常用指令](#常用指令)

---

## 初次設置

### 1. Clone 專案

```bash
git clone https://github.com/fred1357944/compas-actions.ghpython_components.git
cd compas-actions.ghpython_components
```

### 2. 建立 Conda 環境

```bash
# 創建環境
conda env create -f environment.yml

# 啟動環境
conda activate gh_timber
```

### 3. 初始化 Conda（如果需要）

```bash
# 如果 conda activate 無效，執行
conda init zsh  # 或 conda init bash

# 然後重啟終端機，或執行
source ~/.zshrc
```

### 4. 設定便捷 Alias（推薦）

在 `~/.zshrc` 或 `~/.bash_profile` 中已自動設定：

```bash
alias gh_comp='cd /Users/laihongyi/Downloads/compas-actions.ghpython_components && /opt/homebrew/Caskroom/miniconda/base/envs/gh_timber/bin/python componentize_cpy.py components dist --version "0.1.0"'
```

重新載入：
```bash
source ~/.zshrc
```

---

## 每日開發流程

### 從零開始（電腦重啟後）

#### 1. 開啟終端機

打開 Terminal.app

#### 2. 進入專案資料夾

```bash
cd /path/to/compas-actions.ghpython_components
```

#### 3. 啟動 Conda 環境

```bash
conda activate gh_timber
```

你應該會看到終端機提示符前面出現 `(gh_timber)`

#### 4. 開始開發

**方法 1: 使用 Alias（最快）**
```bash
gh_comp
```

**方法 2: 完整指令**
```bash
python componentize_cpy.py components dist --version "0.1.0"
```

### 開發工作流程

```
1. 編輯組件 → 2. 構建 → 3. 安裝 → 4. 測試
    ↓             ↓          ↓         ↓
components/   gh_comp    UserObjects  Grasshopper
```

#### 步驟詳解

**1. 編輯組件**
```bash
# 修改現有組件
code components/YOLO_UDP_Receiver/code.py

# 或創建新組件
mkdir components/MyNewComponent
cp components/YOLO_UDP_Receiver/icon.png components/MyNewComponent/
# 創建 code.py 和 metadata.json
```

**2. 構建組件**
```bash
gh_comp
# 或
python componentize_cpy.py components dist --version "0.1.0"
```

**3. 安裝到 Grasshopper**
- 在 Grasshopper: `File > Special Folders > User Object Folder`
- 複製 `dist/*.ghuser` 到該資料夾
- 重啟 Grasshopper

**4. 測試組件**
- 在 Grasshopper 中找到組件
- 拖放到畫布測試

---

## 可用組件

本專案目前包含 4 個組件：

### 1. Component Updater (v0.1.0)
- **分類**: Utilities > Version
- **功能**: 版本檢查與管理工具
- **特色**: 掃描畫布組件、比對版本、偵測參數變化
- **文檔**: [components/Component_Updater/README.md](components/Component_Updater/README.md)

### 2. Swarm Dynamics (v0.1.0)
- **分類**: Physics > Simulation
- **功能**: 粒子群體動力學模擬系統
- **特色**: 彈簧物理、旋轉效果、呼吸效果、K-近鄰連接
- **文檔**: [components/Swarm_Dynamics/README.md](components/Swarm_Dynamics/README.md)

### 3. YOLO UDP Receiver (v0.1.0)
- **分類**: YOLO > Network
- **功能**: YOLOv8 姿態偵測 UDP 數據接收器
- **特色**: 17 個關鍵點、Point3d 輸出、無阻塞 Socket
- **配套**: [originalcode/opencv2gh_yolov8.py](originalcode/opencv2gh_yolov8.py)

### 4. Test GhTimber (v0.1.0)
- **分類**: GhTimber > Utilities
- **功能**: 測試與範例組件
- **特色**: 演示基本組件結構

📖 **完整組件目錄**: [COMPONENT_CATALOG.md](COMPONENT_CATALOG.md)

---

## 常用指令

### Conda 環境管理

```bash
# 查看所有環境
conda env list

# 啟動環境
conda activate gh_timber

# 退出環境
conda deactivate

# 更新環境（當 environment.yml 修改後）
conda env update -f environment.yml
```

### 構建組件

```bash
# 使用 alias（推薦）
gh_comp

# 完整指令
python componentize_cpy.py components dist --version "0.1.0"

# 指定版本號
python componentize_cpy.py components dist --version "0.2.0"

# 查看生成的文件
ls -lh dist/
```

### 版本檢查

```bash
# 檢查 Python 版本和路徑
which python
python --version

# 檢查已安裝的套件
conda list

# 檢查 pythonnet 是否正確安裝
python -c "from pythonnet import set_runtime; print('pythonnet OK')"
```

### Git 操作

```bash
# 查看狀態
git status

# 查看最近的 commits
git log --oneline -10

# 查看變更
git diff

# 提交變更
git add components/MyComponent/
git commit -m "新增：MyComponent 組件"
git push
```

---

## 設定快捷指令（一次性設定）

### 方法 1: 設定 Alias（推薦）

編輯你的 shell 配置文件：

```bash
# 如果使用 zsh（macOS 預設）
nano ~/.zshrc

# 如果使用 bash
nano ~/.bash_profile
```

在文件最後加入：

```bash
# GH Timber Development
alias gh_comp='cd /Users/laihongyi/Downloads/compas-actions.ghpython_components-main && /opt/homebrew/Caskroom/miniconda/base/envs/gh_timber/bin/python componentize_cpy.py components dist --version "0.1.0"'
alias gh_dev='cd /Users/laihongyi/Downloads/compas-actions.ghpython_components-main && conda activate gh_timber'
```

保存後執行：
```bash
source ~/.zshrc  # 或 source ~/.bash_profile
```

**以後使用：**
```bash
gh_dev    # 進入專案並啟動環境
gh_comp   # 產生組件文件
```

### 方法 2: 創建執行腳本

創建一個執行腳本：

```bash
cat > ~/gh_componentize.sh << 'EOF'
#!/bin/bash
cd /Users/laihongyi/Downloads/compas-actions.ghpython_components-main
/opt/homebrew/Caskroom/miniconda/base/envs/gh_timber/bin/python componentize_cpy.py components dist --version "$1"
EOF

chmod +x ~/gh_componentize.sh
```

**使用：**
```bash
~/gh_componentize.sh "0.1.0"
```

## 常用指令速查表

### Conda 環境管理

```bash
# 查看所有環境
conda env list

# 啟動環境
conda activate gh_timber

# 退出環境
conda deactivate

# 更新環境（當 environment.yml 修改後）
conda env update -f environment.yml
```

### 開發工作流

```bash
# 1. 進入專案
cd /Users/laihongyi/Downloads/compas-actions.ghpython_components-main

# 2. 啟動環境
conda activate gh_timber

# 3. 產生組件
/opt/homebrew/Caskroom/miniconda/base/envs/gh_timber/bin/python componentize_cpy.py components dist --version "0.1.0"

# 4. 查看產生的文件
ls -lh dist/
```

### 檢查環境狀態

```bash
# 檢查 Python 版本和路徑
which python
python --version

# 檢查已安裝的套件
conda list

# 檢查 pythonnet 是否正確安裝
python -c "from pythonnet import set_runtime; print('pythonnet OK')"
```

## 故障排除

### 問題 1: `conda: command not found`

**解決：**
```bash
# 初始化 conda
/opt/homebrew/Caskroom/miniconda/base/bin/conda init

# 重啟終端機或
source ~/.zshrc
```

### 問題 2: `conda activate` 後 Python 還是系統版本

**檢查：**
```bash
which python
```

**如果顯示 `/usr/bin/python3`，使用完整路徑：**
```bash
/opt/homebrew/Caskroom/miniconda/base/envs/gh_timber/bin/python componentize_cpy.py components dist --version "0.1.0"
```

### 問題 3: ModuleNotFoundError: No module named 'pythonnet'

**確認使用正確的 Python：**
```bash
/opt/homebrew/Caskroom/miniconda/base/envs/gh_timber/bin/python -c "import pythonnet; print('OK')"
```

如果還是錯誤，重新安裝：
```bash
/opt/homebrew/Caskroom/miniconda/base/envs/gh_timber/bin/pip install --force-reinstall pythonnet==3.0.1
```

## 典型開發流程範例

### 早上開始工作

```bash
# 1. 開啟終端機
# 2. 進入專案
cd /Users/laihongyi/Downloads/compas-actions.ghpython_components-main

# 3. 啟動環境（如果有設定 alias）
gh_dev

# 或手動
conda activate gh_timber
```

### 開發迭代

```bash
# 編輯代碼...
# 使用你喜歡的編輯器編輯 components/ 中的文件

# 產生組件
gh_comp  # 如果有設定 alias

# 或完整指令
/opt/homebrew/Caskroom/miniconda/base/envs/gh_timber/bin/python componentize_cpy.py components dist --version "0.1.0"

# 複製到 Grasshopper
# 在 Grasshopper: File > Special Folders > User Object Folder
# 複製 dist/*.ghuser

# 重啟 Grasshopper 測試
```

### 結束工作

```bash
# 退出環境（可選）
conda deactivate
```

## 更新版本號

當你準備發布新版本時：

```bash
# 修改版本號
gh_comp  # 或
/opt/homebrew/Caskroom/miniconda/base/envs/gh_timber/bin/python componentize_cpy.py components dist --version "0.2.0"
```

## 備註

- ✅ env_path.txt 已配置，無需每次修改
- ✅ python.runtimeconfig.json 已配置，無需每次修改
- ✅ componentize_cpy.py 已修正，無需每次修改
- 🔄 只需專注於開發 `components/` 中的組件代碼

---

## 進階主題

### 版本管理

使用 Component Updater 檢查版本：

```
1. 在 Grasshopper 中放置 Component Updater 組件
2. check = True
3. 查看 report 輸出
```

詳見 [VERSION_MANAGEMENT.md](VERSION_MANAGEMENT.md)

### 團隊協作

多人協作最佳實踐：

```bash
# 同步最新代碼
git pull origin main

# 創建功能分支
git checkout -b feature/my-new-component

# 開發...
gh_comp

# 提交
git add .
git commit -m "新增：MyComponent"
git push origin feature/my-new-component

# 在 GitHub 創建 Pull Request
```

詳見 [TEAM_COLLABORATION.md](TEAM_COLLABORATION.md)

### 開發新組件

完整教學請參閱：
- [DEVELOPMENT_GUIDE.md](DEVELOPMENT_GUIDE.md) - 組件開發指南
- [COMPONENT_CATALOG.md](COMPONENT_CATALOG.md) - 組件範例

---

## 相關文檔

- **[README.md](README.md)** - 專案說明
- **[DEVELOPMENT_GUIDE.md](DEVELOPMENT_GUIDE.md)** - 開發指南
- **[TEAM_COLLABORATION.md](TEAM_COLLABORATION.md)** - 團隊協作
- **[VERSION_MANAGEMENT.md](VERSION_MANAGEMENT.md)** - 版本管理
- **[COMPONENT_CATALOG.md](COMPONENT_CATALOG.md)** - 組件目錄
- **[CHANGELOG.md](CHANGELOG.md)** - 變更日誌
- **[SETUP_FIXES.md](SETUP_FIXES.md)** - 故障排除

---

**最後更新**: 2025-12-30
**維護者**: Claude Code
**專案**: https://github.com/fred1357944/compas-actions.ghpython_components
