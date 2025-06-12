#!/bin/bash

# 设置 Python 路径
PYTHON_BIN=/usr/local/bin/python3.7

# 切换到项目目录
cd /gemapp || exit 1

# 打印 Python 版本
echo "使用 Python: $PYTHON_BIN"
$PYTHON_BIN --version

# 启动 Flask 应用
echo "启动 Flask..."
nohup $PYTHON_BIN app.py > flask.log 2>&1 &

# 稍等 2 秒以确保 Flask 启动
sleep 2

# 检查端口是否已监听
if netstat -tulpn | grep 5000 > /dev/null; then
    echo "✅ Flask 成功运行中"
else
    echo "❌ Flask 启动失败，日志如下："
    tail -n 30 flask.log
fi
