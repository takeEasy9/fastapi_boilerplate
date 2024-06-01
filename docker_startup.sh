#!/bin/bash
echo "当前目录为$PWD"
if [ -d "fastapi_boilerplate/" ]
then
  echo "fastapi_boilerplate文件夹存在"
  echo "开始删除 fastapi_boilerplate 目录下的代码"
  rm -rf fastapi_boilerplate/*
else
  mkdir fastapi_boilerplate
fi
echo "开始解压到 fastapi_boilerplate 目录..."
tar -zxf fastapi_boilerplate.tgz -C ./fastapi_boilerplate
echo "fastapi_boilerplate.tgz 解压完成"
echo "开始停止fastapi_boilerplate服务"
python_path=$PWD/fastapi_boilerplate
CONTAINER_ID=$(docker ps -a | grep "fastapi_boilerplate:8080" | grep -v grep | awk '{print $1}')
IMAGE=$(docker images | grep "fastapi_boilerplate.*8080" | grep -v grep | awk '{print $3}')
if [ -z "$CONTAINER_ID" ]
then
  echo "[ 找不到fastapi_boilerplate API服务 ]"
else
  echo "fastapi_boilerplate 服务容器ID: $CONTAINER_ID"
  echo "image ID: $IMAGE"
  docker stop "$CONTAINER_ID"
  docker rm "$CONTAINER_ID"
  echo "成功停止 fastapi_boilerplate 服务"
fi
echo "开始启动fastapi_boilerplate API服务"
echo "开始构建 fastapi_boilerplate docker 镜像..."
docker build -t fastapi_boilerplate:8080 .
current_time=$(date "+%Y%m%d%H%M%S")
mkdir "log"$current_time
docker run -d -p 8080:8080 --privileged=true --name="fastapi_boilerplate_8080" -v $PWD/"log"$current_time:/home/app/fastapi_boilerplate/logs fastapi_boilerplate:8080
echo "fastapi_boilerplate 服务启动成功"
IMAGE_TAG=$(docker images | grep $IMAGE | grep -v grep | awk '{print $2}')
echo "old image tag: $IMAGE_TAG"
if [ "$IMAGE_TAG" = "<none>" ]
then
  echo "删除旧版docker镜像"
  docker rmi $IMAGE
else
  echo "docker镜像无变更"