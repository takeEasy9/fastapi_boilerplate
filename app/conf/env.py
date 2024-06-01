# -*- coding: utf-8 -*-

"""
@author: takeEasy9
@description: environment
@version: 1.0.0
@since: 2024/1/27 16:56
"""
import argparse

import yaml


class __Environment:

    def __init__(self):
        self.__config_file = {}
        self.__config_commandline = {}

    def __resolve_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--profile', choices=['dev', 'test', 'prod'], )
        parser.add_argument('--server.host')
        parser.add_argument('--server.port', type=int)
        # 解析命令行参数
        args = parser.parse_args()
        args = {**vars(args)}
        self.__config_commandline["profile"] = args["profile"]
        self.__config_commandline["server.host"] = args["server.host"]
        self.__config_commandline["server.port"] = args["server.port"]

    def __resolve_config_file(self, filename, e):
        config_file = f'config/{filename}-{e}.yaml'
        with open(config_file, mode='r', encoding='utf-8') as config_file:
            config = yaml.load(config_file, Loader=yaml.FullLoader)
            self.__config_file["env"] = e
            self.__config_file["application.name"] = config['application']['name']
            self.__config_file["application.version"] = config['application']['version']

            # server 配置
            self.__config_file["server.host"] = config['server']['host']
            self.__config_file["server.port"] = int(config['server']['port'])

            # DB 配置
            self.__config_file["datasource.mysql_chat.schema"] = config['datasource']['mysql_chat']['schema']
            self.__config_file["datasource.mysql_chat.host"] = config['datasource']['mysql_chat']['host']
            self.__config_file["datasource.mysql_chat.port"] = config['datasource']['mysql_chat']['port']
            self.__config_file["datasource.mysql_chat.username"] = config['datasource']['mysql_chat']['username']
            self.__config_file["datasource.mysql_chat.password"] = config['datasource']['mysql_chat']['password']
            self.__config_file["datasource.mysql_chat.isolation_level"] = \
                config['datasource']['mysql_chat']['isolation_level']
            self.__config_file["datasource.mysql_chat.max_overflow"] = \
                config['datasource']['mysql_chat']['max_overflow']
            self.__config_file["datasource.mysql_chat.pool_size"] = \
                config['datasource']['mysql_chat']['pool_size']
            self.__config_file["datasource.mysql_chat.pool_timeout"] = \
                config['datasource']['mysql_chat']['pool_timeout']
            self.__config_file["datasource.mysql_chat.pool_recycle"] = \
                config['datasource']['mysql_chat']['pool_recycle']

            # logger 配置
            self.__config_file["logger.level"] = config['logger']['level']
            self.__config_file["logger.encoding"] = config['logger']['encoding']
            self.__config_file["logger.path"] = config['logger']['path']
            self.__config_file["logger.file_name"] = config['logger']['file_name']
            self.__config_file["logger.date_time_format"] = config['logger']['date_time_format']
            self.__config_file["logger.formatter"] = config['logger']['formatter']
            self.__config_file["logger.backup_count"] = int(config['logger']['backup_count'])
            # 单位：MB 转换为字节
            self.__config_file["logger.max_file_size"] = int(config['logger']['max_file_size']) * 1024 * 1024

            #  mail 配置
            self.__config_file["mail.host"] = config['mail']['host']
            self.__config_file["mail.port"] = config['mail']['port']
            self.__config_file["mail.username"] = config['mail']['username']
            self.__config_file["mail.password"] = config['mail']['password']
            self.__config_file["mail.default-bcc"] = config['mail']['default-bcc']

            # minio配置
            self.__config_file["minio.endpoint"] = config['minio']['endpoint']
            self.__config_file["minio.access_key"] = config['minio']['access_key']
            self.__config_file["minio.secret_key"] = config['minio']['secret_key']

            # 短信配置
            self.__config_file["sms.url"] = config['sms']['url']
            self.__config_file["sms.bound"] = config['sms']['bound']
            self.__config_file["sms.mobiles"] = config['sms']['mobiles']

    def prepare_environment(self, config_filename="config", env="dev"):
        self.__resolve_args()
        self.__resolve_config_file(config_filename, env)

    def get_property(self, k: str, d: any = None) -> any:
        if not str:
            return d
        ret = self.__config_commandline.get(k, None)
        if ret:
            return ret
        ret = self.__config_file.get(k, None)
        if ret:
            return ret
        return d


environment = __Environment()
