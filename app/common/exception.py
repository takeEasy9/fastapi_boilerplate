# -*- coding: utf-8 -*-

"""
@author: takeEasy9
@description: 自定义异常
@version: 1.0.0
@since: 2024/5/18 17:01
"""


class BusinessException(Exception):
    """业务异常"""

    def __init__(self, code, msg):
        super().__init__(self)
        self.code = code
        self.message = msg

    def __str__(self):
        return f"{self.code}: {self.message}"


class MethodArgumentNotValidException(Exception):
    """参数无效异常"""

    def __init__(self, code, msg):
        super().__init__(self)
        self.code = code
        self.message = msg

    def __str__(self):
        return f"{self.code}: {self.message}"
