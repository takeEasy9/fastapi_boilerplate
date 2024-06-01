# -*- coding: utf-8 -*-

"""
@author: takeEasy9
@description: 时间工具类
@version: 1.0.0
@since: 2024/5/18 16:38
"""
import datetime

from app.conf.logConfiguration import logger


def is_date_valid(date: str, date_format='%Y-%m-%d') -> bool:
    """
    判断日期是否合法
    :param date: 日期
    :param date_format: 日期格式
    :return: True-有效 False-无效
    """
    try:
        if not date or not date_format:
            logger.error(f"判断日期是否合法, 日期或日期格式无效，date={date}, date_format={date_format}")
            return False
        datetime.datetime.strptime(date, date_format)
        return True
    except ValueError:
        return False


def is_range_date_valid(start_date: str, end_date: str, date_format='%Y-%m-%d', both_required=True) -> bool:
    """
    判断日期范围是否合法

    :param start_date: 开始日期
    :param end_date: 结束日期
    :param date_format: 日期格式
    :param both_required: 是否必须同时存在
    :return: True-有效 False-无效
    """

    if both_required:
        if not start_date or not end_date:
            return False
        return is_date_valid(start_date, date_format) \
               and is_date_valid(end_date, date_format) \
               and start_date <= end_date
    else:
        if not start_date and not end_date:
            return True
        elif not start_date and end_date:
            return is_date_valid(end_date, date_format)
        elif start_date and not end_date:
            return is_date_valid(start_date, date_format)
        else:
            return is_date_valid(start_date, date_format) \
                   and is_date_valid(end_date, date_format) \
                   and start_date <= end_date
