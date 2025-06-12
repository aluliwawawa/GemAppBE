from flask import Flask, jsonify
from cache import get_user_info_cached
from database import Database
import logging
import sys
from config import API_CONFIG

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 初始化 Flask 和数据库
app = Flask(__name__)
db = Database()

# 获取用户 homevalue 状态
@app.route('/api/user/<user_id>/status', methods=['GET'])
def get_user_status(user_id):
    try:
        homevalue = db.get_user_homevalue(user_id)
        if homevalue is not None:
            logger.info(f"[homevalue] 用户 {user_id} 的 homevalue = {homevalue}")
            return jsonify({'status': 'success', 'data': {'homevalue': homevalue}}), 200
        else:
            return jsonify({'status': 'error', 'message': '用户不存在'}), 404
    except Exception as e:
        logger.error(f"获取用户状态失败: {e}")
        return jsonify({'status': 'error', 'message': '获取用户状态失败'}), 500

# 获取单个用户信息（缓存）
@app.route('/api/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user_data = get_user_info_cached(user_id)
        if user_data:
            return jsonify({"status": "success", "data": user_data}), 200
        else:
            return jsonify({"status": "error", "message": "用户不存在"}), 404
    except Exception as e:
        logger.error(f"Error fetching user {user_id}: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# 获取所有用户信息
@app.route('/api/users', methods=['GET'])
def get_all_users():
    try:
        users = db.get_all_users()
        return jsonify({"status": "success", "data": users}), 200
    except Exception as e:
        logger.error(f"Error fetching all users: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# 获取申请信息
@app.route('/api/user/<int:user_id>/application', methods=['GET'])
def get_user_applications(user_id):
    try:
        results = db.get_user_applications(user_id)
        return jsonify({
            'status': 'success',
            'data': results or []  # 为空也返回 success
        }), 200
    except Exception as e:
        logger.error(f"获取用户 {user_id} 的申请记录失败: {e}")
        return jsonify({
            'status': 'error',
            'message': '获取申请记录失败'
        }), 500

# 404 错误处理
@app.errorhandler(404)
def not_found(error):
    return jsonify({"status": "error", "message": "资源未找到"}), 404

# 500 错误处理
@app.errorhandler(500)
def internal_error(error):
    return jsonify({"status": "error", "message": "服务器错误"}), 500

# 启动服务
if __name__ == '__main__':
    try:
        logger.info(f"启动 Flask 应用: {API_CONFIG['host']}:{API_CONFIG['port']}")
        app.run(
            host=API_CONFIG['host'],
            port=API_CONFIG['port'],
            debug=API_CONFIG['debug']
        )
    except Exception as e:
        logger.error(f"Flask 启动失败: {e}")
        sys.exit(1)
