# 人脸识别系统 (HW03)
基于 face_recognition 和 Streamlit 的人脸识别 Web 应用。

## 项目结构
 hw03/
├── src/                  # 核心代码
│   ├── face_recognition_logic.py  # 人脸识别逻辑
│   └── streamlit_app.py           # Web界面
├── known_faces/          # 已知人脸库
├── requirements.txt      # 依赖列表
└── README.md             # 项目说明

## 运行方式
1. 安装依赖：`pip install -r requirements.txt`
2. 启动服务：`streamlit run src/streamlit_app.py`
3. 访问浏览器中显示的本地地址（如 http://localhost:8501）

## 功能说明
- 支持上传图片或选择示例图片
- 自动检测图片中的人脸位置并框选
- 与已知人脸库比对，输出识别结果（姓名或Unknown）
- 展示识别详情（人脸位置、识别标签）
