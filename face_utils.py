# face_utils.py

import face_recognition
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os
import cv2  # 用于格式转换（可选）

def load_image(file_path):
    """
    从文件路径加载图片，返回 PIL Image 对象
    """
    return Image.open(file_path).convert('RGB')

def detect_faces(image):
    """
    检测图片中所有人脸的位置
    参数:
        image: PIL Image 或 numpy array
    返回:
        face_locations: 列表，每个元素为 (top, right, bottom, left) 的元组
    """
    # 如果输入是 PIL Image，转换为 numpy array
    if isinstance(image, Image.Image):
        image = np.array(image)
    # face_recognition 要求 RGB 格式（我们已经是）
    face_locations = face_recognition.face_locations(image)
    return face_locations

def get_face_encodings(image):
    """
    提取图片中所有人脸的 128 维特征编码
    参数:
        image: PIL Image 或 numpy array
    返回:
        encodings: 列表，每个元素是 128 维的 numpy 数组
    """
    if isinstance(image, Image.Image):
        image = np.array(image)
    encodings = face_recognition.face_encodings(image)
    return encodings

def draw_boxes(image, face_locations, labels=None):
    """
    在图片上绘制人脸框和可选的标签
    参数:
        image: PIL Image 对象（将被修改）
        face_locations: 人脸坐标列表
        labels: 字符串列表，对应每个人脸的标签，长度应与 face_locations 相同
    返回:
        修改后的 PIL Image 对象
    """
    draw = ImageDraw.Draw(image)
    for i, (top, right, bottom, left) in enumerate(face_locations):
        # 绘制红色矩形框，线宽 3
        draw.rectangle(((left, top), (right, bottom)), outline="red", width=3)
        if labels and i < len(labels):
            # 在左上角绘制标签文字
            draw.text((left, top - 10), labels[i], fill="red")
    return image

def load_known_faces(known_dir="known_faces"):
    """
    加载已知人脸库中的所有图片，提取每张图片的第一张人脸编码，并以文件名（不含扩展名）作为标签
    参数:
        known_dir: 存放已知人脸图片的文件夹路径
    返回:
        known_encodings: 编码列表
        known_names: 标签列表
    """
    known_encodings = []
    known_names = []
    
    # 遍历文件夹中的所有图片文件
    for filename in os.listdir(known_dir):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            name = os.path.splitext(filename)[0]  # 文件名作为人名
            file_path = os.path.join(known_dir, filename)
            # 加载图片
            image = face_recognition.load_image_file(file_path)
            # 提取人脸编码
            encodings = face_recognition.face_encodings(image)
            if encodings:
                # 假设每张图片只有一个人脸，取第一个
                known_encodings.append(encodings[0])
                known_names.append(name)
            else:
                print(f"警告：图片 {filename} 中未检测到人脸，已跳过")
    return known_encodings, known_names

def recognize_faces(unknown_encodings, known_encodings, known_names, tolerance=0.6):
    """
    将未知人脸编码与已知库比对，返回每个未知人脸对应的标签
    参数:
        unknown_encodings: 待识别的人脸编码列表
        known_encodings: 已知人脸编码列表
        known_names: 已知人脸标签列表
        tolerance: 距离阈值，小于该值视为匹配
    返回:
        labels: 字符串列表，长度与 unknown_encodings 相同
    """
    if not known_encodings:
        return ["Unknown"] * len(unknown_encodings)
    
    labels = []
    for enc in unknown_encodings:
        # 计算与所有已知人脸的距离
        distances = face_recognition.face_distance(known_encodings, enc)
        best_index = np.argmin(distances)
        if distances[best_index] < tolerance:
            labels.append(known_names[best_index])
        else:
            labels.append("Unknown")
    return labels
