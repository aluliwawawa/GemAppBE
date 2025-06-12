from functools import lru_cache
from database import Database

# 实例化数据库对象
db = Database()

# 缓存包装函数
@lru_cache(maxsize=512)
def get_user_info_cached(user_id):
    """
    缓存用户信息查询，最多保留512个用户结果。
    """
    return db.get_user_info(user_id)

def clear_user_cache():
    """
    清除所有用户缓存（适用于更新或创建用户后）。
    """
    get_user_info_cached.cache_clear()
