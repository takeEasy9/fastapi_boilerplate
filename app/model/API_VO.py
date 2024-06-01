# -*- coding: utf-8 -*-

"""
@author: takeEasy9
@description: 接口实体类
@version: 1.0.0
@since: 2024/5/18 16:31
"""

from typing import Optional

from pydantic import BaseModel


class RangeDateVO(BaseModel):
    """日期范围 VO"""
    startDate: str
    endDate: str


class StockDocDataVO(BaseModel):
    # 交易日期
    tradeDate: str
    # 个股编码
    stockCode: str
    # 个股名称
    stockName: str = ""
    # 交易方向，默认 买入
    tradeDirection: str = "买入"
    # 行业板块
    industrySector: str
    # 推荐理由
    recommendReason: str


class StockMailVO(BaseModel):
    """底稿发送邮件 VO"""
    to: str
    cc: Optional[str]
    bcc: Optional[str]
    docRenderDatas: dict[str, list[StockDocDataVO]]
