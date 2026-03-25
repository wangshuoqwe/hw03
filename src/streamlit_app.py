import streamlit as st
import cv2
import numpy as np
from PIL import Image
from face_recognition_logic import load_known_faces, detect_and_recognize_faces

# 页面配置
st.set_page_config(page_title="人脸识别系统", page_icon="👤")
st.title("👤 基于 face_recognition 的人脸识别系统")

# 加载已知人脸库
known_encodings, known_names = load_known_faces()

# 上传或选择示例图片
uploaded_file = st.file_uploader("上传图片", type=["jpg", "jpeg", "png"])
example_option = st.selectbox("或选择示例图片", ["无", "示例1", "示例2"], index=0)

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    image_np = np.array(image)
elif example_option != "无":
    # 可预先准备示例图片放在项目中
    st.info("请先将示例图片放入项目目录，或替换为实际路径")
    image_np = None
else:
    image_np = None

if image_np is not None:
    st.subheader("原始图片")
    st.image(image_np, channels="RGB")
    
    # 执行检测与识别
    result_image, face_locations, face_names = detect_and_recognize_faces(
        image_np.copy(), known_encodings, known_names
    )
    
    st.subheader("识别结果")
    st.image(result_image, channels="RGB")
    
    # 展示识别信息
    st.subheader("识别详情")
    for i, (loc, name) in enumerate(zip(face_locations, face_names)):
        st.write(f"人脸 {i+1}: 位置 {loc}, 识别为 {name}")

