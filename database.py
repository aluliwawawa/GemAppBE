import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self.connection = None
        self.connect()

    def connect(self):
        """建立数据库连接"""
        try:
            # 打印连接信息（不打印密码）
            logger.info(f"Attempting to connect to MySQL database at {DB_CONFIG['host']}:{DB_CONFIG['port']}")
            logger.info(f"Using database: {DB_CONFIG['database']}")
            logger.info(f"Using user: {DB_CONFIG['user']}")
            
            self.connection = mysql.connector.connect(**DB_CONFIG)
            if self.connection.is_connected():
                db_info = self.connection.get_server_info()
                logger.info(f"Successfully connected to MySQL database. Server version: {db_info}")
                
                cursor = self.connection.cursor()
                cursor.execute("select database();")
                db_name = cursor.fetchone()[0]
                logger.info(f"Connected to database: {db_name}")
                cursor.close()
        except Error as e:
            logger.error(f"Error connecting to MySQL database: {e}")
            raise

    def disconnect(self):
        """关闭数据库连接"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            logger.info("MySQL connection closed")

    def get_user_info(self, user_id):
        """从总计划表中获取用户信息"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT username, startdatum, zieldatum, aktueldatum 
                FROM 总计划 
                WHERE id = %s
            """
            logger.info(f"Executing query: {query} with user_id: {user_id}")
            cursor.execute(query, (user_id,))
            result = cursor.fetchone()
            cursor.close()
            
            if result:
                logger.info(f"Found user info: {result}")
                return {
                    'username': result['username'],
                    'startdatum': result['startdatum'],
                    'zieldatum': result['zieldatum'],
                    'aktueldatum': result['aktueldatum']
                }
            logger.warning(f"No user found with id: {user_id}")
            return None
        except Error as e:
            logger.error(f"Error fetching user info: {e}")
            raise

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()
