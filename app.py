from flask import Flask, jsonify
from database import Database

app = Flask(__name__)
db = Database()  # 创建数据库连接实例

@app.route('/api/user/<user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user_data = db.get_user_info(user_id)
        if user_data:
            return jsonify(user_data), 200
        else:
            return jsonify({"error": "用户不存在"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
