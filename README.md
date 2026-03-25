# 人脸识别系统 (HW03)
基于 `face_recognition` 和 `Streamlit` 构建的人脸检测与识别 Web 应用。
## 功能特点
- 上传图片，自动检测其中所有人脸并框出。
- 若配置了已知人脸库，则与库中的人脸进行比对，输出识别结果。
- 支持多人脸同时检测与识别。
## 环境要求
- Python 3.7 及以上
- 推荐使用虚拟环境
## 安装与运行
1. 克隆仓库并进入 `hw03` 目录：
   ```bash
   git clone <你的仓库地址>
   cd hw03
 ## 创建虚拟环境
 python -m venv venv
source venv/bin/activate   # macOS/Linux  或
venv\Scripts\activate      # Windows
 ## 安装依赖
 pip install -r requirements.txt
 ## 运行应用
 streamlit run app.py
