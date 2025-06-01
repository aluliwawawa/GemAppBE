#!/bin/bash

# 设置工作目录
cd /gemapp

# 打印当前目录
echo "Current directory: $(pwd)"

# 检查Python版本
echo "Python version:"
python3 --version

# 检查pip版本
echo "Pip version:"
pip3 --version

# 检查已安装的包
echo "Installed packages:"
pip3 list

# 设置环境变量
export FLASK_APP=app.py
export FLASK_ENV=development
export FLASK_DEBUG=1

# 启动Flask应用
echo "Starting Flask application..."
/usr/local/bin/python3.7 -m flask run --host=0.0.0.0 --port=5000 --debugger
