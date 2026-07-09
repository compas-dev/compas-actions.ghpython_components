import System
import Rhino.Geometry as rg
from System.Net import IPEndPoint, IPAddress
from System.Net.Sockets import Socket, AddressFamily, SocketType, ProtocolType
from System.Net.Sockets import SocketOptionLevel, SocketOptionName
from System.Text import Encoding

# Module-level state to persist across component runs
# Note: reload(gh_yolo_udp) will reset these to None/Empty, which causes a socket reconnect.
# This is desirable for development (updating logic), though it might cause a brief glitch.
_udp_socket = None
_keypoints = {}

def parse_json(text):
    """Simple JSON parser without external dependencies"""
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

def get_pose_data(enable, port_input, target_joint_input):
    """
    Main logic function to retrieve and process YOLO pose data.
    
    Args:
        enable: Boolean to control whether the receiver is active.
        port_input: The UDP port to listen on.
        target_joint_input: The specific joint name to track.
        
    Returns:
        dict: A dictionary containing all output data expected by the GH component.
    """
    global _udp_socket, _keypoints
    
    # Initialize default outputs
    x = 0.0
    y = 0.0
    z = 0.0
    point = rg.Point3d(0.0, 0.0, 0.0)
    all_points = []
    joint_names = []
    debug_lines = []
    
    # === DISABLE LOGIC ===
    if not enable:
        if _udp_socket is not None:
            try:
                _udp_socket.Close()
            except:
                pass
            _udp_socket = None
            debug_lines.append("Socket closed.")
            
        # Optional: Clear memory when disabled? Usually good practice.
        _keypoints = {} 
        
        message = "Disabled"
        return {
            "point": point,
            "x": x,
            "y": y,
            "z": z,
            "all_points": all_points,
            "joint_names": joint_names,
            "message": message,
            "debug": "\n".join(debug_lines)
        }

    # === ENABLE LOGIC ===
    message = "Initializing (HOT RELOADED)..."
    
    try:
        # Process inputs
        port_num = int(port_input) if port_input else 9999
        target = str(target_joint_input).strip() if target_joint_input else "left_wrist"

        debug_lines.append("Loaded from: " + __file__)
        debug_lines.append("Port: {}".format(port_num))
        debug_lines.append("Target: '{}'".format(target))

        # Setup socket
        if _udp_socket is None:
            _udp_socket = Socket(
                AddressFamily.InterNetwork,
                SocketType.Dgram,
                ProtocolType.Udp
            )
            _udp_socket.Blocking = False
            # Timeout is less critical in non-blocking but good practice
            _udp_socket.ReceiveTimeout = 10 
            _udp_socket.SetSocketOption(
                SocketOptionLevel.Socket,
                SocketOptionName.ReuseAddress,
                True
            )
            _udp_socket.Bind(
                IPEndPoint(IPAddress.Parse("127.0.0.1"), port_num)
            )
            debug_lines.append("Socket created/reconnected")

        # Receive data
        buffer = System.Array.CreateInstance(System.Byte, 8192)
        received = 0

        # Read up to 50 packets per frame to clear buffer/get latest data
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
                # No data available or other socket error
                break
            except Exception:
                break

        debug_lines.append("Received {} packets".format(received))
        debug_lines.append("Keypoints in memory: {}".format(len(_keypoints)))

        # Process target joint
        if target in _keypoints:
            kp = _keypoints[target]

            # Scale coordinates (assuming 0-1 normalized input, scaling to 0-100 units)
            # You can adjust this logic here without touching the GH component!
            scale_factor = 100.0
            x = float(kp['x']) * scale_factor
            y = float(kp['y']) * scale_factor
            z = 0.0

            point = rg.Point3d(x, y, z)

            debug_lines.append("Found '{}'".format(target))
            debug_lines.append("Raw: ({:.4f}, {:.4f})".format(kp['x'], kp['y']))
            debug_lines.append("Scaled: ({:.2f}, {:.2f}, {:.2f})".format(x, y, z))

            message = "OK: {} ({} pts)".format(target, len(_keypoints))
        else:
            point = rg.Point3d(0.0, 0.0, 0.0)

            if _keypoints:
                available = ', '.join(list(_keypoints.keys())[:5])
                message = "No '{}' (have: {}...)".format(target, available)
                debug_lines.append("Target '{}' not found".format(target))
            else:
                message = "No data yet (RELOADED V2)"
                debug_lines.append("No keypoints data")

        # Process all joints for list output
        all_points = []
        joint_names = []
        for name in sorted(_keypoints.keys()):
            kp = _keypoints[name]
            # Same scaling applied here
            pt = rg.Point3d(float(kp['x']) * 100.0, float(kp['y']) * 100.0, 0.0)
            all_points.append(pt)
            joint_names.append(name)

        debug_lines.append("Total output points: {}".format(len(all_points)))

    except Exception as e:
        message = "ERROR: {}".format(str(e)[:50])
        debug_lines.append("Exception: {}".format(str(e)))
        # Reset state on critical error could be an option, but let's keep it safe
    
    debug = "\n".join(debug_lines)
    
    return {
        "point": point,
        "x": x,
        "y": y,
        "z": z,
        "all_points": all_points,
        "joint_names": joint_names,
        "message": message,
        "debug": debug
    }
