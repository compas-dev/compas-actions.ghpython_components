"""
opencv2gh - YOLOv8 姿態辨識版本
使用 Ultralytics YOLOv8-Pose 模型
"""

import cv2
from ultralytics import YOLO
import socket
import json
import numpy as np

# === UDP 設定 ===
UDP_IP = "127.0.0.1"
UDP_PORT = 9999  # 改用 9999（高 Port，較少衝突）

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# === 載入 YOLOv8 Pose 模型 ===
print("📦 載入 YOLOv8-Pose 模型...")
model = YOLO('yolov8n-pose.pt')  # n=nano(最快), s=small, m=medium
print("✅ 模型載入完成\n")

# === 攝影機設定 ===
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

print("🎥 攝影機已啟動 (YOLOv8-Pose)")
print(f"📡 UDP 發送至 {UDP_IP}:{UDP_PORT}")
print("按 'q' 鍵離開\n")

# === COCO Keypoints 格式（17個點）===
KEYPOINT_NAMES = [
    "nose",           # 0
    "left_eye",       # 1
    "right_eye",      # 2
    "left_ear",       # 3
    "right_ear",      # 4
    "left_shoulder",  # 5
    "right_shoulder", # 6
    "left_elbow",     # 7
    "right_elbow",    # 8
    "left_wrist",     # 9
    "right_wrist",    # 10
    "left_hip",       # 11
    "right_hip",      # 12
    "left_knee",      # 13
    "right_knee",     # 14
    "left_ankle",     # 15
    "right_ankle"     # 16
]

frame_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1
    h, w = frame.shape[:2]

    # === YOLOv8 推論 ===
    results = model(frame, verbose=False)

    # 處理結果
    for result in results:
        # 繪製偵測結果（包含骨架）
        annotated_frame = result.plot()

        # 如果有偵測到姿態
        if result.keypoints is not None and len(result.keypoints) > 0:
            # 取第一個人（可擴展為多人）
            keypoints_data = result.keypoints[0].data.cpu().numpy()[0]

            # 準備數據
            keypoints = {}

            for i, (x, y, conf) in enumerate(keypoints_data):
                if i >= len(KEYPOINT_NAMES):
                    break

                name = KEYPOINT_NAMES[i]

                # 正規化座標
                keypoints[name] = {
                    "x": round(float(x / w), 4),
                    "y": round(float(y / h), 4),
                    "confidence": round(float(conf), 3),
                    "raw_x": int(x),
                    "raw_y": int(y)
                }

            # 計算額外資訊
            # 身體中心點（肩膀和髖部的中點）
            if "left_shoulder" in keypoints and "right_shoulder" in keypoints:
                center_x = (keypoints["left_shoulder"]["x"] +
                           keypoints["right_shoulder"]["x"]) / 2
                center_y = (keypoints["left_shoulder"]["y"] +
                           keypoints["right_shoulder"]["y"]) / 2
            else:
                center_x, center_y = 0.5, 0.5

            # 組合完整數據
            data = {
                "type": "pose_yolov8",
                "frame": frame_count,
                "keypoints": keypoints,
                "body_center": {
                    "x": round(center_x, 4),
                    "y": round(center_y, 4)
                },
                "num_people": len(result.keypoints),
                "timestamp": frame_count / 30.0
            }

            # 發送 UDP - 優化：分批發送每個關鍵點
            for name, coords in keypoints.items():
                mini_data = {
                    "type": "keypoint_yolo",
                    "frame": frame_count,
                    "name": name,
                    **coords
                }
                try:
                    sock.sendto(json.dumps(mini_data).encode(), (UDP_IP, UDP_PORT))
                except Exception as e:
                    print(f"發送錯誤: {e}")

            # 顯示資訊
            cv2.putText(annotated_frame, f"Frame: {frame_count}",
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(annotated_frame, f"People: {len(result.keypoints)}",
                       (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            # 顯示畫面
            cv2.imshow('opencv2gh - YOLOv8 Pose', annotated_frame)
        else:
            cv2.putText(frame, "No pose detected",
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.imshow('opencv2gh - YOLOv8 Pose', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 清理
cap.release()
cv2.destroyAllWindows()
sock.close()
print("\n✅ 程式結束")
