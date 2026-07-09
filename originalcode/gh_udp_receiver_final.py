"""
UDP Receiver - 最終修正版
確保輸出正確的 Point3d，並提供詳細診斷
"""
import clr
clr.AddReference("System")
clr.AddReference("RhinoCommon")

from System.Net import IPEndPoint, IPAddress
from System.Net.Sockets import Socket, AddressFamily, SocketType, ProtocolType
from System.Net.Sockets import SocketOptionLevel, SocketOptionName
from System.Text import Encoding
import Rhino.Geometry as rg
import System

# === 輸出初始化 - 明確類型 ===
x = 0.0
y = 0.0
z = 0.0
point = rg.Point3d(0.0, 0.0, 0.0)  # 明確初始化為 Point3d
all_points = []
joint_names = []
msg = "啟動中..."
debug = ""

# === 全域變數 ===
if '_udp_socket' not in dir():
    _udp_socket = None
if '_keypoints' not in dir():
    _keypoints = {}

# === JSON 解析 ===
def parse_json(text):
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

# === 主程式 ===
try:
    debug_lines = []

    # 處理輸入
    port_num = int(port) if 'port' in dir() and port else 9999
    target = str(target_joint).strip() if 'target_joint' in dir() and target_joint else "left_wrist"

    debug_lines.append("Port: {}".format(port_num))
    debug_lines.append("Target: '{}'".format(target))

    # Socket 設置
    if _udp_socket is None:
        _udp_socket = Socket(AddressFamily.InterNetwork, SocketType.Dgram, ProtocolType.Udp)
        _udp_socket.Blocking = False
        _udp_socket.ReceiveTimeout = 10
        _udp_socket.SetSocketOption(SocketOptionLevel.Socket, SocketOptionName.ReuseAddress, True)
        _udp_socket.Bind(IPEndPoint(IPAddress.Parse("127.0.0.1"), port_num))
        debug_lines.append("Socket 已建立")

    # 接收數據
    buffer = System.Array.CreateInstance(System.Byte, 8192)
    received = 0

    for i in range(50):
        try:
            n = _udp_socket.Receive(buffer)
            if n > 0:
                received += 1
                text = Encoding.UTF8.GetString(buffer, 0, n)
                data = parse_json(text)

                if 'keypoint' in data.get('type', ''):
                    name = data.get('name', '')
                    if name:
                        _keypoints[name] = {
                            'x': float(data.get('x', 0)),
                            'y': float(data.get('y', 0)),
                            'confidence': float(data.get('confidence', 1.0))
                        }
        except System.Net.Sockets.SocketException:
            break
        except:
            break

    debug_lines.append("收到 {} 封包".format(received))
    debug_lines.append("關鍵點: {}".format(len(_keypoints)))

    # 處理目標關節
    if target in _keypoints:
        kp = _keypoints[target]

        # 明確轉換為 float
        x_coord = float(kp['x'])
        y_coord = float(kp['y'])

        # 縮放座標
        x = x_coord * 100.0
        y = y_coord * 100.0
        z = 0.0

        # 明確創建 Point3d（這是關鍵！）
        point = rg.Point3d(x, y, z)

        debug_lines.append("✓ 找到 '{}'".format(target))
        debug_lines.append("原始: ({:.4f}, {:.4f})".format(x_coord, y_coord))
        debug_lines.append("縮放: ({:.2f}, {:.2f}, {:.2f})".format(x, y, z))
        debug_lines.append("point 類型: {}".format(type(point).__name__))
        debug_lines.append("point 值: {}".format(point))

        msg = "OK: {} ({} pts)".format(target, len(_keypoints))
    else:
        # 沒找到也要確保 point 是 Point3d
        x = 0.0
        y = 0.0
        z = 0.0
        point = rg.Point3d(0.0, 0.0, 0.0)

        if _keypoints:
            available = ', '.join(list(_keypoints.keys())[:5])
            msg = "✗ 無 '{}' (有: {})".format(target, available)
            debug_lines.append("✗ 目標 '{}' 不存在".format(target))
            debug_lines.append("可用: {}".format(', '.join(_keypoints.keys())))
        else:
            msg = "✗ 無數據"
            debug_lines.append("✗ _keypoints 為空")

    # 處理所有關節點
    all_points = []
    joint_names = []
    for name in sorted(_keypoints.keys()):
        kp = _keypoints[name]
        pt = rg.Point3d(float(kp['x']) * 100.0, float(kp['y']) * 100.0, 0.0)
        all_points.append(pt)
        joint_names.append(name)

    debug_lines.append("all_points: {}".format(len(all_points)))

    # 最終確認
    debug_lines.append("")
    debug_lines.append("=== 輸出確認 ===")
    debug_lines.append("x = {} ({})".format(x, type(x).__name__))
    debug_lines.append("y = {} ({})".format(y, type(y).__name__))
    debug_lines.append("z = {} ({})".format(z, type(z).__name__))
    debug_lines.append("point = {} ({})".format(point, type(point).__name__))

except Exception as e:
    msg = "ERROR: {}".format(str(e)[:50])
    debug_lines = ["例外: {}".format(str(e))]
    # 即使出錯也要確保類型正確
    x = 0.0
    y = 0.0
    z = 0.0
    point = rg.Point3d(0.0, 0.0, 0.0)

# 輸出
debug = "\n".join(debug_lines)
