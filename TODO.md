# TODO - 待辦事項與未來開發計劃

> 最後更新：2026-01-06
> 專案評分：8.3/10（已從 7.5 提升）

---

## 📋 待辦事項

### 🔴 高優先級

#### 1. Component_Updater 自動更新功能
- **狀態**: 🚧 開發中（目前僅支援檢查）
- **目標**: 實現一鍵自動更新組件
- **技術挑戰**:
  - Grasshopper SDK 不允許直接替換組件
  - 需要研究 GH Kernel 深層 API
  - 可能需要 C# 插件支援
- **Phase 規劃**:
  - [x] Phase 1: 版本檢查（已完成 ✅）
  - [ ] Phase 2: 更新提示與指引
  - [ ] Phase 3: 自動替換（需 C# 支援）
- **參考**: `VERSION_MANAGEMENT.md`

#### 2. 單元測試基礎設施
- **狀態**: ❌ 缺失
- **目標**: 建立 pytest 測試套件
- **待辦**:
  - [ ] 創建 `tests/` 目錄結構
  - [ ] 新增 `test_component_updater.py`
  - [ ] 新增 `test_swarm_dynamics.py`
  - [ ] 新增 `test_yolo_receiver.py`
  - [ ] 新增 `pytest.ini` 配置
  - [ ] 在 CI/CD 中新增測試 job

```
tests/
├── __init__.py
├── conftest.py
├── test_component_updater.py
├── test_swarm_dynamics.py
├── test_yolo_receiver.py
└── fixtures/
    └── manifest.json
```

---

### 🟡 中優先級

#### 3. Swarm_Dynamics 性能優化
- **狀態**: ⚠️ 可改進
- **問題**: K-NN 使用 O(n²) 暴力搜尋
- **目標**: 節點數 > 100 時性能下降明顯
- **解決方案**:
  - [ ] 使用 KD-Tree（scipy.spatial.cKDTree）
  - [ ] 或使用空間分割（Spatial Hashing）
- **預估提升**: 10-50 倍（視節點數量）

#### 4. YOLO_UDP_Receiver JSON 解析改進
- **狀態**: ⚠️ 功能受限
- **問題**: 自製解析器不支援嵌套結構
- **解決方案**:
  - [ ] 改用 `json` 標準庫
  - [ ] 或增強自製解析器支援陣列
- **影響**: 提升數據格式彈性

#### 5. 數值穩定性（Swarm_Dynamics）
- **狀態**: ⚠️ 可能有問題
- **問題**:
  - Euler 積分誤差累積
  - 粒子可能逃離邊界框
  - 無碰撞檢測
- **解決方案**:
  - [ ] 改用 RK4 積分法
  - [ ] 新增邊界約束
  - [ ] 新增簡單碰撞檢測

---

### 🟢 低優先級

#### 6. Pre-commit Hooks
- **狀態**: ❌ 缺失
- **目標**: 代碼提交前自動檢查
- **待辦**:
  - [ ] 新增 `.pre-commit-config.yaml`
  - [ ] 配置 pylint/flake8 規則
  - [ ] 配置 black 格式化
  - [ ] 配置 isort 導入排序

#### 7. 文檔自動化
- **狀態**: ❌ 手動維護
- **目標**: 從代碼生成文檔
- **待辦**:
  - [ ] 設置 Sphinx 或 MkDocs
  - [ ] 自動生成 API 文檔
  - [ ] 自動 CHANGELOG（commitizen）
  - [ ] 部署到 GitHub Pages

#### 8. 版本同步自動化
- **狀態**: ⚠️ 手動同步
- **問題**: manifest.json vs COMPONENT_CATALOG.md 可能不一致
- **解決方案**:
  - [ ] 創建腳本自動驗證版本一致性
  - [ ] 在 CI 中檢查版本號同步
  - [ ] 或從 manifest.json 生成文檔

---

## 📊 專案狀態

### 組件完成度

| 組件 | 功能 | 文檔 | 測試 | 整體 |
|------|------|------|------|------|
| Component_Updater | 70% | 100% | 0% | 57% |
| Swarm_Dynamics | 90% | 100% | 0% | 63% |
| YOLO_UDP_Receiver | 95% | 100% | 0% | 65% |
| Test_GhTimber | 100% | 100% | 0% | 67% |

### 基礎設施完成度

| 項目 | 狀態 |
|------|------|
| CI/CD 構建 | ✅ 完成 |
| CI/CD 驗證 | ✅ 完成 |
| CI/CD 測試 | ❌ 缺失 |
| PR 模板 | ✅ 完成 |
| Issue 模板 | ❌ 缺失 |
| Pre-commit | ❌ 缺失 |
| 文檔自動化 | ❌ 缺失 |

---

## 🎯 版本規劃

### v0.2.0（下一版本）
- [ ] Component_Updater Phase 2（更新提示）
- [ ] 基本單元測試
- [ ] Swarm_Dynamics 邊界約束

### v0.3.0
- [ ] YOLO JSON 解析改進
- [ ] Swarm_Dynamics KD-Tree 優化
- [ ] Pre-commit hooks

### v1.0.0（穩定版）
- [ ] 完整測試覆蓋率（> 80%）
- [ ] 文檔自動化
- [ ] Component_Updater 自動更新

---

## 📝 開發筆記

### 2026-01-06 Opus 專案檢查

**發現的問題**:
1. YOLO_UDP_Receiver 缺 README ✅ 已修復
2. manifest.json 結構不規範 ✅ 已修復
3. 依賴版本未鎖定 ✅ 已修復
4. Test_GhTimber 缺 README ✅ 已修復
5. CI/CD 缺 validate job ✅ 已修復
6. 缺 PR 模板 ✅ 已修復

**評分提升**: 7.5 → 8.3（+0.8）

### 2025-12-30 熱重載機制

**實現**: YOLO_UDP_Receiver 重構為外部套件架構
- code.py: 155 行 → 31 行（-80%）
- 邏輯分離到 gh_yolo_udp 套件
- 支援 importlib.reload() 熱重載

### 2025-12-21 初始版本

**完成**:
- 4 個組件開發完成
- 版本管理系統建立
- 完整文檔系統（11 個文檔）
- macOS ARM64 支援

---

## 🔗 相關資源

- **Pull Request**: https://github.com/compas-dev/compas-actions.ghpython_components/pull/19
- **專案倉庫**: https://github.com/fred1357944/compas-actions.ghpython_components
- **開發指南**: `DEVELOPMENT_GUIDE.md`
- **版本管理**: `VERSION_MANAGEMENT.md`
- **變更日誌**: `CHANGELOG.md`

---

**維護者**: Claude Code
**最後檢查**: 2026-01-06（Opus）
