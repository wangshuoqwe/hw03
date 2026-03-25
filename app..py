# app.py

import streamlit as st
from PIL import Image
import numpy as np
import face_utils  # 我们自定义的模块

# 设置页面标题和布局
st.set_page_config(page_title="人脸识别系统", layout="wide")
st.title("基于 face_recognition 的人脸识别系统")
st.markdown("上传一张图片，系统将自动检测并识别其中的人脸。")

# 侧边栏：显示已知人脸库信息
st.sidebar.header("已知人脸库")
# 使用 st.cache_resource 缓存加载结果，避免每次交互都重新加载
@st.cache_resource
def load_known_faces_cached():
    return face_utils.load_known_faces("known_faces")

known_encodings, known_names = load_known_faces_cached()
st.sidebar.write(f"已加载 {len(known_names)} 个已知人脸：")
if known_names:
    st.sidebar.write(", ".join(known_names))
else:
    st.sidebar.info("请将已知人脸图片放入 known_faces 文件夹")

# 上传图片区域
uploaded_file = st.file_uploader("请选择一张图片", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # 读取图片为 PIL Image
    image = Image.open(uploaded_file).convert("RGB")
    
    # 显示原图
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("原图")
        st.image(image, use_container_width=True)
    
    # 处理图片
    with st.spinner("正在处理..."):
        # 1. 人脸检测
        face_locations = face_utils.detect_faces(image)
        
        if not face_locations:
            st.warning("未检测到任何人脸，请上传包含清晰人脸的图片。")
        else:
            # 2. 提取人脸编码
            img_np = np.array(image)
            face_encodings = face_utils.get_face_encodings(img_np)
            
            # 3. 识别（如果已知库非空且有编码）
            if known_encodings and face_encodings:
                labels = face_utils.recognize_faces(face_encodings, known_encodings, known_names)
            else:
                # 如果已知库为空，则全部标为 Unknown
                labels = ["Unknown"] * len(face_locations)
            
            # 4. 绘制结果
            result_image = face_utils.draw_boxes(image.copy(), face_locations, labels)
            
            # 显示结果图
            with col2:
                st.subheader("检测结果")
                st.image(result_image, use_container_width=True)
            
            # 5. 显示详细列表
            st.subheader("检测到的人脸详情")
            for i, (loc, label) in enumerate(zip(face_locations, labels)):
                top, right, bottom, left = loc
                st.write(f"{i+1}. {label} – 位置: (左:{left}, 上:{top}, 右:{right}, 下:{bottom})")
    
else:
    st.info("等待上传图片...")
