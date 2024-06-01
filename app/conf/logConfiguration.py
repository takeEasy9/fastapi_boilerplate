# -*- coding: utf-8 -*-

"""
@author: takeEasy9
@description: log configuration
@version: 1.0.0
@since: 2024/1/27 22:04
"""
import logging
import sys
from logging import handlers

from app.conf.env import environment
from app.utils.file_util import mkdir, touch_file


class LoggerConfiguration:
    def __init__(self):
        # logger
        root_logger = logging.getLogger('root')
        console_logger = logging.getLogger('console')
        file_logger = logging.getLogger('file')
        # handler
        stream_handler = logging.StreamHandler(sys.stdout)
        logger_path = environment.get_property("logger.path", "./log")
        mkdir(logger_path)
        logger_file_name = environment.get_property("logger.file_name", "logfile.log")
        file_name = f"{logger_path}/{logger_file_name}"
        touch_file(file_name)
        file_handler = handlers.RotatingFileHandler(filename=file_name,
                                                    maxBytes=environment.get_property("logger.max_file_size", 30 * 10124 * 1024),
                                                    backupCount=environment.get_property("logger.backup_count", 3),
                                                    mode='a',
                                                    encoding=environment.get_property("logger.encoding", "logfile.log"))
        # 设置日志等级 默认为DEBUG
        logger_level = environment.get_property("logger.level", "DEBUG")
        root_logger.setLevel(logger_level)
        console_logger.setLevel(logger_level)
        file_logger.setLevel(logger_level)
        stream_handler.setLevel(logger_level)
        file_handler.setLevel(logger_level)
        # 设置日志格式
        logger_date_time_formatter = environment.get_property("logger.date_time_format", "%Y-%m-%d %H:%M:%S")
        log_formatter = environment.get_property("logger.formatter", "%(asctime)s.%(msecs)03d\
                                                                      %(levelname)s [%(filename)s\
                                                                       %(funcName)s line:%(lineno)d] %(message)s ")
        formatter = logging.Formatter(log_formatter, logger_date_time_formatter)
        stream_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)
        # 为logger设置handler
        root_logger.addHandler(stream_handler)
        root_logger.addHandler(file_handler)
        console_logger.addHandler(stream_handler)
        file_logger.addHandler(file_handler)

        # 关闭打开的日志文件
        file_handler.close()

        self.__loggers = {'root': root_logger, 'console': console_logger, 'file': file_logger}

    def get_logger(self, name='root'):
        assert (name in self.__loggers.keys())
        return self.__loggers[name]


logger = LoggerConfiguration().get_logger()
