# 人脸识别系统 (HW03)
基于 face_recognition 和 Streamlit 实现的人脸识别 Web 应用，用于《人工智能通识课》课程作业。

## 项目结构
 hw03/
├── src/                 
│   ├── face_recognition_logic.py 
│   └── streamlit_app.py          
├── known_faces/          
├── requirements.txt    
└── README.md            

## 运行方式
1. 安装依赖：`pip install -r requirements.txt`
2. 启动服务：`streamlit run src/streamlit_app.py`
3. 访问浏览器中显示的本地地址（如 http://localhost:8501）

## 功能说明
- 支持上传图片或选择示例图片
- 自动检测图片中的人脸位置并框选
- 与已知人脸库比对，输出识别结果（姓名或Unknown）
- 展示识别详情（人脸位置、识别标签）

## 环境准备
1. 确保已安装 Python 3.8~3.11
2. 安装依赖：
   ```bash
   pip install -r requirements.txt
