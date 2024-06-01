# -*- coding: utf-8 -*-

"""
@author: takeEasy9
@description:
@version: 1.0.0
@since: 2024/5/18 16:50
"""
from app.utils.constant_util import Invariable
from app.utils.enum_util import CallableCode, GuiCode, SystemCode


class ErrorCodeMsg(Invariable):
    def __init__(self, code, msg):
        self.code = code
        self.msg = msg

    def get_code(self):
        return self.code

    def get_msg(self):
        return self.msg


class CallableErrorCodeMsg(ErrorCodeMsg):
    # 调用第三方服务正常
    CALLABLE_SUCCESS = ErrorCodeMsg(CallableCode.CALLABLE_SUCCESS, "调用第三方服务正常")
    # 调用第三方服务失败
    CALLABLE_FAILED = ErrorCodeMsg(CallableCode.CALLABLE_FAILED, "调用第三方服务失败")
    SHORT_MESSAGE_SEND_SUCCESS = ErrorCodeMsg(CallableCode.CALLABLE_SUCCESS, "短信发送成功")
    SHORT_MESSAGE_SEND_FAILED = ErrorCodeMsg(CallableCode.CALLABLE_FAILED, "短信发送失败")

    MAIL_SEND_SUCCESS = ErrorCodeMsg(CallableCode.CALLABLE_SUCCESS, "邮件发送成功")
    MAIL_SEND_FAILED = ErrorCodeMsg(CallableCode.CALLABLE_FAILED, "邮件发送失败")

    WORD_CONVERT_TO_PDF_SUCCESS = ErrorCodeMsg(CallableCode.CALLABLE_SUCCESS, "word文件转pdf成功")
    WORD_CONVERT_TO_PDF_FAILED = ErrorCodeMsg(CallableCode.CALLABLE_FAILED, "word文件转pdf失败")


class GuiErrorCodeMsg(ErrorCodeMsg):
    # 调用第三方服务正常
    ACCESS_PARAMETER_INVALID = ErrorCodeMsg(GuiCode.ACCESS_PARAMETER_INVALID, "入参无效,请检查")

    DAILY_GOLD_STOCK_GEN_DOC_SEND_MAIL_SUCCESS = ErrorCodeMsg(CallableCode.CALLABLE_SUCCESS, "生成报告并发送邮件成功")
    DAILY_GOLD_STOCK_GEN_DOC_SEND_MAIL_FAIL = ErrorCodeMsg(CallableCode.CALLABLE_FAILED, "生成报告并发送邮件失败")


class SystemErrorCode(ErrorCodeMsg):
    DATA_INSERT_FAILED = ErrorCodeMsg(SystemCode.DATA_INSERT_FAILED, "记录新增失败,请检查您的输入是否正确")

    DATA_UPDATE_FAILED = ErrorCodeMsg(SystemCode.DATA_UPDATE_FAILED, "记录更新失败,请检查您的输入是否正确")

    DATA_DELETE_FAILED = ErrorCodeMsg(SystemCode.DATA_DELETE_FAILED, "记录删除失败,请检查您的输入是否正确")

    DATA_QUERY_FAILED = ErrorCodeMsg(SystemCode.DATA_QUERY_FAILED, "记录查询失败,请检查您的输入是否正确")
