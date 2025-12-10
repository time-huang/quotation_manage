from flask import Flask
from flask_cors import CORS
from routes import api_bp
from database import create_tables

# 初始化Flask应用
app = Flask(__name__)

# 配置CORS，允许所有来源的请求
CORS(app)

# 注册API蓝图
app.register_blueprint(api_bp, url_prefix='/api')

# 初始化数据库表
create_tables()

@app.route('/')
def index():
    """ 根路由 """
    return "Quotation Management System API is running"

if __name__ == '__main__':
    # 启动Flask应用，监听所有网络接口，端口5000
    app.run(host='0.0.0.0', port=5000, debug=True)
