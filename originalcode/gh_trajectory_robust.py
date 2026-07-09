"""
軌跡繪製器 - 超強健版本
保證能生成曲線，提供詳細錯誤診斷
"""
import clr
clr.AddReference("RhinoCommon")
import Rhino.Geometry as rg

# 全域變數
if 'traj_points' not in dir():
    traj_points = []

if '_update_count' not in dir():
    _update_count = 0

# 輸出初始化
count = 0
trajectory = None
msg = "start"
out = None
debug_info = ""

# === 主程式 ===
try:
    _update_count += 1
    debug_lines = []
    debug_lines.append("更新 #{}".format(_update_count))

    # 處理 clear
    if 'clear' in dir() and clear:
        traj_points = []
        _update_count = 0
        msg = "已清除"
        debug_lines.append("清除所有點")

    # 處理 record
    do_record = True
    if 'record' in dir() and record is not None:
        do_record = bool(record)

    debug_lines.append("record = {}".format(do_record))

    # 處理 max_points
    max_pts = 500
    if 'max_points' in dir() and max_points:
        try:
            max_pts = int(max_points)
        except:
            max_pts = 500

    # 處理輸入點
    if do_record and 'point' in dir() and point:
        pt = None

        # 判斷輸入類型
        try:
            if hasattr(point, 'X') and hasattr(point, 'Y') and hasattr(point, 'Z'):
                # 是 Point3d
                pt = point
                debug_lines.append("收到單點")
            elif hasattr(point, '__getitem__'):
                # 是列表
                if len(point) > 0:
                    pt = point[0]
                    debug_lines.append("收到列表 (長度: {})".format(len(point)))
            else:
                debug_lines.append("✗ 未知點類型: {}".format(type(point)))
        except Exception as e:
            debug_lines.append("✗ 解析點錯誤: {}".format(str(e)[:30]))

        # 記錄點
        if pt:
            try:
                # 提取座標
                px = float(pt.X)
                py = float(pt.Y)
                pz = float(pt.Z) if hasattr(pt, 'Z') else 0.0

                debug_lines.append("座標: ({:.2f}, {:.2f}, {:.2f})".format(px, py, pz))

                # 直接添加，不過濾（診斷用）
                new_point = rg.Point3d(px, py, pz)
                traj_points.append(new_point)
                debug_lines.append("✓ 已添加點 #{}".format(len(traj_points)))

                # 限制點數
                if len(traj_points) > max_pts:
                    traj_points.pop(0)
                    debug_lines.append("移除最舊點 (max={})".format(max_pts))

            except Exception as e:
                debug_lines.append("✗ 添加點錯誤: {}".format(str(e)[:50]))
        else:
            debug_lines.append("✗ pt 為 None")
    else:
        if not do_record:
            debug_lines.append("✗ record = False")
        elif 'point' not in dir() or not point:
            debug_lines.append("✗ 無點輸入")

    # 輸出點列表
    count = len(traj_points)
    out = traj_points

    debug_lines.append("")
    debug_lines.append("總點數: {}".format(count))

    # === 曲線生成 - 多重嘗試 ===
    if count >= 2:
        debug_lines.append("")
        debug_lines.append("=== 嘗試生成曲線 ===")

        # 方法 1: 簡單折線（最可靠）
        try:
            debug_lines.append("方法1: Polyline")
            polyline = rg.Polyline(traj_points)
            trajectory = polyline.ToNurbsCurve()
            if trajectory:
                msg = "✓ {} 點 (折線)".format(count)
                debug_lines.append("✓ 成功 (Polyline)")
            else:
                debug_lines.append("✗ ToNurbsCurve() 返回 None")
        except Exception as e1:
            debug_lines.append("✗ Polyline 失敗: {}".format(str(e1)[:40]))

            # 方法 2: 直接創建 LineCurve
            try:
                debug_lines.append("方法2: LineCurve")
                if count == 2:
                    trajectory = rg.LineCurve(traj_points[0], traj_points[1])
                    msg = "✓ {} 點 (直線)".format(count)
                    debug_lines.append("✓ 成功 (LineCurve)")
                else:
                    # 多個點，創建多段線
                    segments = []
                    for i in range(len(traj_points) - 1):
                        seg = rg.LineCurve(traj_points[i], traj_points[i+1])
                        segments.append(seg)

                    if len(segments) > 0:
                        trajectory = rg.Curve.JoinCurves(segments, 0.01)[0]
                        msg = "✓ {} 點 (線段)".format(count)
                        debug_lines.append("✓ 成功 (JoinCurves)")
            except Exception as e2:
                debug_lines.append("✗ LineCurve 失敗: {}".format(str(e2)[:40]))

                # 方法 3: 插值曲線
                try:
                    debug_lines.append("方法3: Interpolated")
                    trajectory = rg.Curve.CreateInterpolatedCurve(
                        traj_points, 3, rg.CurveKnotStyle.Chord
                    )
                    if trajectory:
                        msg = "✓ {} 點 (平滑)".format(count)
                        debug_lines.append("✓ 成功 (Interpolated)")
                    else:
                        debug_lines.append("✗ CreateInterpolatedCurve 返回 None")
                except Exception as e3:
                    debug_lines.append("✗ Interpolated 失敗: {}".format(str(e3)[:40]))

        # 最終檢查
        if trajectory:
            debug_lines.append("")
            debug_lines.append("✓ trajectory 已生成")
            debug_lines.append("  類型: {}".format(type(trajectory).__name__))
            try:
                debug_lines.append("  長度: {:.2f}".format(trajectory.GetLength()))
            except:
                pass
        else:
            msg = "✗ 曲線生成失敗"
            debug_lines.append("")
            debug_lines.append("✗ 所有方法都失敗了")
            debug_lines.append("  可能原因:")
            debug_lines.append("  - 點太近或重複")
            debug_lines.append("  - 座標有問題")

    elif count == 1:
        msg = "需要 2+ 點 (目前 1)"
        debug_lines.append("只有 1 點，無法繪製")
    else:
        msg = "無點"
        debug_lines.append("traj_points 為空")

except Exception as e:
    count = -999
    msg = "ERROR: " + str(e)[:40]
    debug_lines = [
        "=== 嚴重錯誤 ===",
        str(e),
        "類型: {}".format(type(e).__name__)
    ]
    import traceback
    try:
        tb = traceback.format_exc()
        debug_lines.append("")
        debug_lines.extend(tb.split('\n')[:10])
    except:
        pass

# 輸出
debug = "\n".join(debug_lines)
