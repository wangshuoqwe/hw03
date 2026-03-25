import face_recognition
import cv2
import numpy as np
from pathlib import Path

def load_known_faces(known_faces_dir: str = "known_faces"):
    """加载已知人脸库，返回编码和姓名列表"""
    known_encodings = []
    known_names = []
    
    for img_path in Path(known_faces_dir).glob("*.jpg"):
        image = face_recognition.load_image_file(img_path)
        encodings = face_recognition.face_encodings(image)
        if encodings:
            known_encodings.append(encodings[0])
            known_names.append(img_path.stem)  # 文件名作为人名
    return known_encodings, known_names

def detect_and_recognize_faces(image: np.ndarray, known_encodings, known_names):
    """检测并识别人脸，返回带框和标签的图像及结果"""
    # 检测人脸位置
    face_locations = face_recognition.face_locations(image)
    # 提取人脸特征编码
    face_encodings = face_recognition.face_encodings(image, face_locations)
    
    face_names = []
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_encodings, face_encoding)
        name = "Unknown"
        face_distances = face_recognition.face_distance(known_encodings, face_encoding)
        if face_distances.size > 0:
            best_match_idx = np.argmin(face_distances)
            if matches[best_match_idx]:
                name = known_names[best_match_idx]
        face_names.append(name)
    
    # 在图像上绘制人脸框和标签
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.rectangle(image, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(image, name, (left + 6, bottom - 6), font, 0.6, (255, 255, 255), 1)
    
    return image, face_locations, face_names

