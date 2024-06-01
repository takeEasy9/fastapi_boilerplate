# -*- coding: utf-8 -*-

"""
@author: takeEasy9
@description:
@version: 1.0.0
@since: 2024/5/18 16:37
"""
from enum import Enum, unique


class ValueEnum(Enum):
    """ 值枚举类基类 """

    def __new__(cls, value):
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def get_value(self):
        return self._value_

    @classmethod
    def is_exist(cls, value):
        for item in cls:
            if item.value == value:
                return True
        return False


class CodeMessageEnum(Enum):
    """ 编码消息枚举类基类 """

    def __new__(cls, code, label: str):
        obj = object.__new__(cls)
        obj._code_ = code
        obj._label_ = label
        return obj

    def get_value(self):
        return self._code_

    def get_label(self):
        return self._label_


class ValueLabelEnum(ValueEnum):
    """ 值标签枚举类基类 """

    def __new__(cls, code, label: str):
        obj = object.__new__(cls)
        obj._value_ = code
        obj._label_ = label
        return obj

    def get_value(self):
        return self._value_

    def get_label(self):
        return self._label_


def get_label_by_value(cls, value):
    """ 根据枚举值获取标签 """
    for item in cls:
        if item.get_value() == value:
            return item.get_label()
    return None


@unique
class SystemCode(ValueEnum):
    """System 消息编码"""
    # 系统正常
    SYSTEM_SUCCESS = "B0000"
    # 系统异常
    SYSTEM_FAILED = "B0001"
    # 数据获取成功
    DATA_QUERY_SUCCESS = "B0002"
    # 数据插入成功
    DATA_INSERT_SUCCESS = "B0003"
    # 数据更新成功
    DATA_UPDATE_SUCCESS = "B0004"
    # 数据删除成功
    DATA_DELETE_SUCCESS = "B0005"
    # 数据插入失败
    DATA_INSERT_FAILED = "B0006"
    # 数据更新失败
    DATA_UPDATE_FAILED = "B0007"
    # 数据删除失败
    DATA_DELETE_FAILED = "B0008"
    # 数据查询失败
    DATA_QUERY_FAILED = "B0009"

    # 数据不存在
    DATA_NOT_EXISTS = "B0100"
    PRIVATE_KEY_NOT_EXISTS = "B0101"
    PUBLIC_KEY_NOT_EXISTS = "B0102"
    SYMMETRIC_KEY_NOT_EXISTS = "B0103"
    KEY_NOT_EXISTS = "B0104"
    VALUE_IS_EMPTY = "B0105"

    # 数据已存在
    DATA_ALREADY_EXIST = "B0120"
    # 数据无效
    DATA_OPERATION_LIMITED = "B0130"

    DATE_CONVERT_FAILED = "B0136"
    DATA_CHECK_NO_MATCH = "B0137"
    DATA_CHECK_INVALID = "B0138"
    DATA_UPDATE_NO_NEED = "B0139"
    DATA_UPDATE_NO_DATA = "B0140"

    # 数据库异常
    DB_EXCEPTION = "B0400"
    DB_INIT_FAILED = "B0401"
    DB_CLOSE_FAILED = "B0402"


@unique
class CallableCode(ValueEnum):
    # 调用成功
    CALLABLE_SUCCESS = "C0000"
    # 调用失败
    CALLABLE_FAILED = "C0001"


@unique
class GuiCode(ValueEnum):
    # GUI成功
    GUI_SUCCESS = "A0000"
    # GUI失败
    GUI_FAILED = "A0001"
    # 参数无效
    ACCESS_PARAMETER_INVALID = "A0401"


class EnumEntity:
    @unique
    class StockStatus(ValueLabelEnum):
        """"状态,1-有效,2-无效"""
        DAILY_GOLD_STOCK_STATUS_VALID = ("1", "有效")
        DAILY_GOLD_STOCK_STATUS_INVALID = ("2", "无效")

    @unique
    class MailContentType(ValueLabelEnum):
        """邮件内容类型, 1-简单文本, 2-HTML"""
        MAIL_CONTENT_TYPE_PLAIN_TEXT = ("1", "plain")
        MAIL_CONTENT_TYPE_HTML = ("2", "html")
