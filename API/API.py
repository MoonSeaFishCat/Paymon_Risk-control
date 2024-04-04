import os
import logging
import sqlite3

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint

# 设置日志
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

# 获取当前文件的绝对路径
current_file_path = os.path.abspath(os.path.dirname(__file__))

# 获取当前文件所在的目录的上级目录（即项目的根目录）
project_root = os.path.dirname(current_file_path)

# 想要获取的main.py的文件名
main_py_filename = 'start.py'

# 构造main.py的绝对路径
main_py_absolute_path = os.path.join(project_root, main_py_filename)

# 获取main.py文件所在的目录
basedir = os.path.dirname(main_py_absolute_path)

print(basedir)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data/plugins_risk_data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# 定义数据库模型
class Plugin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    md5 = db.Column(db.String(32), nullable=False)
    server_ip = db.Column(db.String(15), nullable=False)
    machine_code = db.Column(db.String(100), nullable=False)

    # 设置唯一性约束，防止重复数据
    __table_args__ = (UniqueConstraint('name', 'author', 'md5', 'server_ip', 'machine_code', name='_plugin_uc'),)


class Plugin_SH(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    qq = db.Column(db.String(100), nullable=False)

    # 设置唯一性约束，防止重复数据
    __table_args__ = (UniqueConstraint('name', 'author', 'qq', name='_plugin_uc'),)


# 创建数据表
with app.app_context():
    db.create_all()


# 定义错误处理函数
def handle_error(message, code):
    logger.error(message)
    return jsonify({'message': message, 'code': code}), code


# 定义提交路由
@app.route('/submit_plugin', methods=['POST'])
def submit_plugin():
    logger.info("执行风控提交")
    data = request.get_json()
    if not data:
        return handle_error("未提供输入数据", 400)

    name = data.get('name')
    author = data.get('author')
    md5 = data.get('md5')
    server_ip = data.get('server_ip')
    machine_code = data.get('machine_code')

    if not name or not author or not md5 or not server_ip or not machine_code:
        return handle_error("缺失必填字段", 400)

    # 检查插件是否已存在
    existing_plugin = Plugin.query.filter_by(name=name, author=author, md5=md5, server_ip=server_ip,
                                             machine_code=machine_code).first()
    if existing_plugin:
        logger.info("插件信息已经存在")
        return jsonify({'message': '插件信息已经存在', 'code': 409}), 409

    # 创建新插件记录
    new_plugin = Plugin(name=name, author=author, md5=md5, server_ip=server_ip, machine_code=machine_code)
    db.session.add(new_plugin)
    try:
        db.session.commit()
        logger.info(f"异常服务器ip： {server_ip}, 异常插件： {name}")
        logger.info(f"插件信息提交成功，ID: {new_plugin.id}")
        return jsonify({'message': '插件信息提交成功', 'plugin_id': new_plugin.id, 'code': 200}), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"写入数据库时发生错误: {e}")
        return handle_error("服务器内部错误", 500)


# 定义检测路由
@app.route('/check_risk_keywords', methods=['POST'])
def check_risk_keywords():
    logger.info("执行信息校验")
    data = request.get_json()
    if not data:
        return handle_error("未提供输入数据", 400)

    text = data.get('text')
    if not text:
        return handle_error("未提供文本数据", 400)
    logger.info(f"提交的检测文本为： {text}")

    # 缓存违禁词列表
    risk_keywords = getattr(app, 'risk_keywords', None)
    if risk_keywords is None:
        db_path = os.path.join(basedir, 'data/plugins_risk_data.db')
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT keyword FROM risk_keywords')
            risk_keywords = [row[0] for row in cursor.fetchall()]
        app.risk_keywords = risk_keywords

    # 检查文本是否包含违禁词
    for keyword in risk_keywords:
        if keyword in text:
            logger.info(f"检测结果：文本包含违禁词 {keyword}")
            return jsonify({'message': f'文本包含违禁词 {keyword}', 'code': 404}), 404

    # 文本不包含违禁词
    logger.info("检测结果：文本检测通过")
    return jsonify({'message': '文本不包含违禁词', 'code': 200}), 200


# 定义审核路由
@app.route('/info_submit', methods=['POST'])
def submit_info():
    data = request.get_json()
    if not data:
        return handle_error("未提供输入数据", 400)

    name = data.get('name')
    author = data.get('author')
    qq = data.get('qq')
    if not name or not author or not qq:
        return handle_error("缺失必填字段", 400)

    # 检查插件是否已存在
    existing_plugin = Plugin_SH.query.filter_by(name=name, author=author, qq=qq).first()
    if existing_plugin:
        logger.info("插件信息已经存在")
        return jsonify({'message': '插件信息已经存在', 'code': 409}), 409

    # 创建新插件记录
    new_plugin = Plugin_SH(name=name, author=author, qq=qq)
    db.session.add(new_plugin)
    try:
        db.session.commit()
        logger.info(f"执行插件审核")
        logger.info(f"插件名称： {name}, 插件作者： {author}, 插件提交者： {qq}")
        logger.info("插件信息提交成功")
        return jsonify({'message': '插件信息提交成功', 'code': 200}), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"写入数据库时发生错误: {e}")
        return handle_error("服务器内部错误", 500)


# 定义首页
@app.route('/')
def default_route():
    return jsonify({
        'message': '欢迎使用Paymon风控处理终端',
        'code': 200,
        'info': '本系统由汐娅是小白推出，用于框架消息风控'
    }), 200


# 定义查询路由
@app.route('/info_search', methods=['POST'])
def info_search():
    logger.info("执行插件审核情况查询")
    data = request.get_json()
    if not data:
        return handle_error("未提供输入数据", 400)

    name = data.get('name')
    if not name:
        return handle_error("未提供文本数据", 400)
    logger.info(f"待检测插件名称为： {name}")

    # 查询违禁词
    risk_keywords = getattr(app, 'risk_keywords', None)
    if risk_keywords is None:
        db_path = os.path.join(basedir, 'data/plugins_risk_data.db')
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT keyword FROM risk_keywords')
            risk_keywords = [row[0] for row in cursor.fetchall()]
        app.risk_keywords = risk_keywords

    # 检查文本是否包含违禁词
    for keyword in risk_keywords:
        if keyword in name:
            logger.info(f"检测结果：插件审核不通过，包含违禁词 {keyword}")
            return jsonify({'message': f'插件包含违禁词 {keyword}，审核不通过', 'code': 403}), 403

    # 文本不包含违禁词
    logger.info("检测结果：插件审核通过")
    return jsonify({'message': '插件审核通过', 'code': 200}), 200


def main_api():
    logger.info("启动系统")
    app.run(debug=False)
