#!/bin/bash
echo "开始删除当前 fastapi_boilerplate 目录下旧的代码"
rm -rf ./fastapi_boilerplate/*
echo "开始解压新代码到 fastapi_boilerplate 目录"
tar -zxf fastapi_boilerplate.tar.gz -C ./fastapi_boilerplate
echo "开始创建虚拟 Python 虚拟环境"
cd ./fastapi_boilerplate || exit
python3.10 -m venv venv
echo "开始激活虚拟 fastapi_boilerplate Python 虚拟环境"
source venv/bin/activate
echo "开始安装 fastapi_boilerplate requirements.txt 中的依赖"
pip3.10 install -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com --no-cache-dir -r requirements.txt
echo "退出 fastapi_boilerplate Python 虚拟环境"
deactivate
echo "开始停止fastapi Python 服务"
sp_pid=$(pgrep -al python | grep "fastapi_boilerplate_main.py" | awk '{print $1}')
if [ -z "$sp_pid" ];
then
  echo "[ 找不到fastapi Python 服务 ]"
  echo "开始启动fastapi Python 服务"
  current_time=$(date "+%Y%m%d%H%M%S")
  format=".log"
  log_file="../fastapi_boilerplate_$current_time$format"
  nohup venv/bin/python3.10 fastapi_boilerplate_main.py --profile=prod > "$log_file" < /dev/tty &
  echo "fastapi Python 服务启动成功"
else
  echo "找到线程: $sp_pid "
  kill -9 "$sp_pid"
  echo "成功停止fastapi Python 服务"
  echo "开始启动fastapi Python 服务"
  current_time=$(date "+%Y%m%d%H%M%S")
  format=".log"
  log_file="../fastapi_boilerplate_$current_time$format"
  nohup venv/bin/python3.10 fastapi_boilerplate_main.py --profile=prod > "$log_file" < /dev/tty &
  echo "fastapi Python 服务启动成功"
fi