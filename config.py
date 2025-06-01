import os
from dotenv import load_dotenv
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 获取当前文件所在目录的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(current_dir, 'acc.env')

# 打印环境变量文件路径
logger.info(f"Loading environment variables from: {env_path}")

# 检查文件是否存在并打印内容
if os.path.exists(env_path):
    logger.info("Environment file exists")
    try:
        with open(env_path, 'r') as f:
            logger.info("Environment file contents:")
            for line in f:
                if 'PASSWORD' not in line:  # 不打印包含密码的行
                    logger.info(line.strip())
    except Exception as e:
        logger.error(f"Error reading environment file: {e}")
else:
    logger.error("Environment file does not exist!")

# 加载环境变量
try:
    load_dotenv(env_path)
    logger.info("Environment variables loaded successfully")
except Exception as e:
    logger.error(f"Error loading environment variables: {e}")

# 打印加载的环境变量（不打印密码）
logger.info("Loaded environment variables:")
logger.info(f"DB_HOST: {os.getenv('DB_HOST')}")
logger.info(f"DB_PORT: {os.getenv('DB_PORT')}")
logger.info(f"DB_USER: {os.getenv('DB_USER')}")
logger.info(f"DB_NAME: {os.getenv('DB_NAME')}")
logger.info(f"DB_PASSWORD is set: {'Yes' if os.getenv('DB_PASSWORD') else 'No'}")

# 数据库配置
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'ClientDoc'),
    'port': int(os.getenv('DB_PORT', 3306)),
}

# 打印数据库配置（不打印密码）
logger.info("Database configuration:")
logger.info(f"Host: {DB_CONFIG['host']}")
logger.info(f"Port: {DB_CONFIG['port']}")
logger.info(f"User: {DB_CONFIG['user']}")
logger.info(f"Database: {DB_CONFIG['database']}")
logger.info(f"Password is set: {'Yes' if DB_CONFIG['password'] else 'No'}")

# API配置
API_CONFIG = {
    'host': os.getenv('API_HOST', '0.0.0.0'),
    'port': int(os.getenv('API_PORT', 5000)),
    'debug': bool(int(os.getenv('API_DEBUG', 0)))
}

# 打印API配置
logger.info("API configuration:")
logger.info(f"Host: {API_CONFIG['host']}")
logger.info(f"Port: {API_CONFIG['port']}")
logger.info(f"Debug mode: {API_CONFIG['debug']}")
