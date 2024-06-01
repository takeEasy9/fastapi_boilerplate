# -*- coding: utf-8 -*-

"""
@author: takeEasy9
@description: 程序入口
@version: 1.0.0
@since: 2024/1/27 16:02
"""
import smtplib

import uvicorn
from fastapi import FastAPI
from minio import Minio

from app.utils.singleton_util import singletonContainer

app = FastAPI()


def create_environment():
    from app.conf.env import environment
    environment.prepare_environment()
    return environment


def print_banner(e, logger_):
    """打印 banner"""
    with open("banner.txt", "r", encoding="utf-8") as bf:
        banner = bf.read()
        logger_(banner)
    application_name = e.get_property("application.name")
    application_version = e.get_property("application.version")
    logger_(f"INFO:\t\tApplication Name: {application_name}")
    logger_(f"INFO:\t\tApplication Version: {application_version}")
    profile = e.get_property("profile")
    logger_(f"INFO:\t\tApplication Environment: {profile}")
    server_host = e.get_property("server.host")
    logger_(f"INFO:\t\tApplication Server Host: {server_host}")
    server_port = e.get_property("server.port")
    logger_(f"INFO:\t\tApplication Server Port: {server_port}")


def init_mysql_data_source(web_logger):
    """初始化MySQL数据源"""
    try:
        web_logger.info("构建MySQL数据源...")
        from app.conf.mysqlConfiguration import mysql_chat_sql_session_factory
        web_logger.info("构建MySQL数据源完成")
    except Exception as e:
        web_logger.error(f"构建MySQL数据源失败,原因是:{e}")
        raise e


def main():
    environment = create_environment()
    logger_path = environment.get_property("logger.path", "./log")
    logger_file_name = environment.get_property("logger.file_name", "logfile.log")
    with open(f"{logger_path}/{logger_file_name}", "a",
              encoding=environment.get_property("logger.encoding")) as log_file:
        def logger_(log: str):
            # 写入到控制台
            print(log)
            # 写入到日志文件
            print(log, file=log_file)
        logger_("INFO:\t\t启动 fastapi web 应用...")
        # 初始化日志设置
        logger_level = environment.get_property("logger.level")
        logger_(f"INFO:\t\t初始化日志设置,当前日志级别为:{logger_level}")
        from app.conf.logConfiguration import logger
        logger_("INFO:\t\t初始化日志设置完成")
        # 打印 banner
        print_banner(environment, logger_)
    # 初始化MySQL数据源
    init_mysql_data_source(logger)
    # minio client
    minio_client = Minio(environment.get_property("minio.port"),
                         access_key=environment.get_property("minio.access_key"),
                         secret_key=environment.get_property("minio.secret_key"),
                         secure=False)
    singletonContainer.register_by_name('minio_client', minio_client)
    # mail server
    mail_server = smtplib.SMTP_SSL(environment.get_property("mail.host"), environment.get_property("mail.port"))
    singletonContainer.register_by_name('mail_server', mail_server)
    # 启动web服务
    uvicorn.run(app,
                host=environment.get_property("server.host", "127.0.0.1"),
                port=environment.get_property("server.port", "8080"))


if __name__ == "__main__":
    main()
