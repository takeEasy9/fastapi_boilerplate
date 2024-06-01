# -*- coding: utf-8 -*-

"""
@author: takeEasy9
@description: 常量
@version: 1.0.0
@since: 2024/5/18 16:37
"""
import re


class Invariable(object):
    class ConstError(PermissionError):
        pass

    def __setattr__(self, name, value):
        if name in self.__dict__.keys():
            raise self.ConstError("Can't rebind const(%s)" % name)
        self.__dict__[name] = value

    def __delattr__(self, name):
        if name in self.__dict__:
            raise self.ConstError("Can't unbind const(%s)" % name)
        raise NameError(name)


class ConstantUtil(Invariable):
    # 默认编码
    DEFAULT_CHARSET = 'utf-8'

    MAIL_CHECK_PATTERN = re.compile(r"^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){1,3}$")

    PROFILE_DEV = 'dev'
    PROFILE_PROD = 'prod'

    SHORT_MESSAGE_CONTENT_BOUND = 128
    SHORT_MESSAGE_URL = 'http://localhost:8084/api/message/send'
