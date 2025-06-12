import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG
import logging

class Database:
    def __init__(self):
        self.connection = None
        self.connect()

    def connect(self):
        try:
            self.connection = mysql.connector.connect(**DB_CONFIG)
            logging.info("数据库连接成功")
        except Exception as e:
            logging.error(f"数据库连接失败: {e}")
            raise

    def ensure_connection(self):
        if not self.connection or not self.connection.is_connected():
            logging.warning("MySQL 连接断开，正在重新连接...")
            self.connect()

    def get_user_info(self, user_id):
        self.ensure_connection()
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT id, username, startdatum, zieldatum, aktueldatum FROM 总计划 WHERE id = %s", (user_id,))
            result = cursor.fetchone()
            cursor.close()
            return result
        except Error as e:
            logging.error(f"获取用户信息失败: {e}")
            return None

    def get_user_homevalue(self, user_id):
        self.ensure_connection()
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT Homevalue FROM 总计划 WHERE id = %s", (user_id,))
            result = cursor.fetchone()
            cursor.close()
            return result[0] if result else 0
        except Error as e:
            logging.error(f"获取 Homevalue 失败: {e}")
            return None

    def get_all_users(self):
        self.ensure_connection()
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT id, username, startdatum, zieldatum, aktueldatum FROM 总计划")
            results = cursor.fetchall()
            cursor.close()
            return results
        except Error as e:
            logging.error(f"获取所有用户失败: {e}")
            return []

    def get_user_applications(self, user_id):
        self.ensure_connection()
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM 申请 WHERE id = %s", (user_id,))
            results = cursor.fetchall()
            cursor.close()
            return results
        except Error as e:
            logging.error(f"获取用户申请记录失败: {e}")
            return []

    def close(self):
        if self.connection:
            self.connection.close()
            logging.info("数据库连接已关闭")
