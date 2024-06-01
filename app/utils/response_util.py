# -*- coding: utf-8 -*-

"""
@author: takeEasy9
@description: response util
@version: 1.0.0
@since: 2024/5/18 16:37
"""
from typing import Any

from app.common.error_code_msg import ErrorCodeMsg


def response_ok(code_msg: ErrorCodeMsg, data: Any) -> dict:
    return {
        "code": code_msg.get_code(),
        "msg": code_msg.get_msg(),
        "data": data
    }


def response_error(code_msg: ErrorCodeMsg) -> dict:
    return {
        "code": code_msg.get_code(),
        "msg": code_msg.get_msg()
    }
