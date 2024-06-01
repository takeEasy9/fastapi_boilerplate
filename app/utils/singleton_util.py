# -*- coding: utf-8 -*-

"""
@author: takeEasy9
@description: python 实现单例模式
@version: 1.0.0
@since: 2024/5/18 16:37
"""


from typing import TypeVar, Type

T = TypeVar('T')


class _SingletonContainer:
    def __init__(self) -> None:
        self.__singleton_map = {}
        self.__singleton_factory_map = {}

    def register_by_type(self, singleton_type: Type[T], instance=None) -> None:
        """通过类型注册单例"""
        assert (isinstance(instance, singleton_type))
        self.register_by_name(singleton_type.__name__, instance)

    def register_by_name(self, name: str, instance=None) -> None:
        """通过名称注册单例"""
        if instance is None:
            self.__singleton_factory_map[name] = lambda: instance
        else:
            self.__singleton_map[name] = instance

    def get_instance_by_type(self, singleton_type: Type[T]) -> T:
        """通过类型获取单例"""
        return self.get_instance_by_name(singleton_type.__name__)

    def get_instance_by_name(self, name: str) -> T:
        """通过名称获取单例"""
        assert (name in self.__singleton_map.keys()
                or name in self.__singleton_factory_map.keys())
        if name not in self.__singleton_map.keys():
            self.__singleton_map[name] = self.__singleton_factory_map[name]()
        return self.__singleton_map[name]


singletonContainer = _SingletonContainer()
