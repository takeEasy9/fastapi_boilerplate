# -*- coding: utf-8 -*-

"""
@author: takeEasy9
@description: MySQL configuration
@version: 1.0.0
@since: 2024/1/27 21:59
"""
from contextlib import contextmanager
from urllib.parse import quote_plus

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from app.conf.logConfiguration import logger
from app.conf.env import environment


class MysqlConfiguration:
    def __init__(self, config_prefix: str):
        schema = environment.get_property(f"{config_prefix}.schema")
        logger.info(f'开始创建并配置 {schema} sqlalchemy engine')
        uri = f'mysql+pymysql://{quote_plus(environment.get_property(f"{config_prefix}.username"))}:' \
              f'{quote_plus(environment.get_property(f"{config_prefix}.password"))}' \
              f'@{environment.get_property(f"{config_prefix}.host")}:' \
              f'{environment.get_property(f"{config_prefix}.port")}' \
              f'/{schema}?charset=utf8'
        # 创建数据库引擎
        engine = create_engine(uri,
                               echo=False,
                               isolation_level=environment.get_property(f"{config_prefix}.isolation_level"),
                               max_overflow=environment.get_property(f"{config_prefix}.max_overflow"),
                               pool_size=environment.get_property(f"{config_prefix}.pool_size"),
                               pool_timeout=environment.get_property(f"{config_prefix}.pool_timeout"),
                               pool_recycle=environment.get_property(f"{config_prefix}.pool_recycle"))
        # 会话工厂
        session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        # scoped_session 保证多线程下的访问
        self.__session = scoped_session(session_factory)

    @contextmanager
    def session_factory(self, auto_commit=False):
        try:
            yield self.__session
            if auto_commit:
                self.__session.commit()
        except Exception as error:
            logger.critical(f'sqlalchemy session error: {error}')
            self.__session.rollback()
            raise
        finally:
            self.__session.close()


mysql_chat_sql_session_factory = MysqlConfiguration("datasource.mysql_chat").session_factory
