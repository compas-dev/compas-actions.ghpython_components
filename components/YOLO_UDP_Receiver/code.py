"""
YOLO UDP Receiver - Grasshopper Component
Receives YOLOv8 pose detection data via UDP and outputs keypoint positions.
Logic is delegated to 'gh_yolo_udp' package for hot-reloading support.

    Args:
        enable: Boolean to start/stop the receiver
        port: UDP port number (default: 9999)
        target_joint: Target joint name (e.g., 'left_wrist', 'nose', 'right_shoulder')

    Returns:
        point: Target joint position as Point3d
        x: X coordinate
        y: Y coordinate
        z: Z coordinate
        all_points: All detected keypoints as Point3d list
        joint_names: List of all detected joint names
        message: Status message
        debug: Debug information
"""

from ghpythonlib.componentbase import executingcomponent as component
import gh_yolo_udp
import gh_yolo_udp.gh_yolo_udp
import importlib

# Force reload of the logic package every time the component runs (or is recomputed)
# IMPORTANT: Since logic is now in a submodule, we must reload the submodule first!
importlib.reload(gh_yolo_udp.gh_yolo_udp)
importlib.reload(gh_yolo_udp)

class YOLOUDPReceiver(component):
    def RunScript(self, enable, port, target_joint):
        self.Message = 'v{{version}}'
        
        # Delegate all work to the external package
        # Pass 'enable' as the first argument
        result = gh_yolo_udp.get_pose_data(enable, port, target_joint)
        
        # Unpack results to match the component outputs
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