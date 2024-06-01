# -*- coding: utf-8 -*-

"""
@author: takeEasy9
@description:
@version: 1.0.0
@since: 2024/5/18 18:03
"""

# sqlalchemy 数据库实体类基类
from sqlalchemy import Column, BigInteger, String, TIMESTAMP, text
from sqlalchemy.orm import declarative_base

_Base = declarative_base()


class IdBase(_Base):
    """mysql 数据库 id 实体类基类"""
    __abstract__ = True
    id = Column('id', BigInteger, primary_key=True, autoincrement=True, comment='物理编码,自增长')

    def __str__(self) -> str:
        return 'IdBase{' \
               + f'id={self.id}' \
               + '}'


class AuditingBase(IdBase):
    """mysql 数据库 包含审计信息 实体类基类"""
    __abstract__ = True
    created_by = Column('created_by', String(50), nullable=False, comment='创建者')
    created_at = Column('created_at', TIMESTAMP(True), nullable=False,
                        default=text('CURRENT_TIMESTAMP'), comment='创建时间,UTC时间')
    last_modified_by = Column('last_modified_by', String(50), nullable=True, comment='最后修改者', )
    last_modified_at = Column('last_modified_at', TIMESTAMP(True), nullable=True, comment='最后修改时间,UTC时间')

    def __init__(self, **kwargs):
        super(AuditingBase, self).__init__(**kwargs)
        self.created_by = kwargs.get('created_by', '')
        self.created_at = kwargs.get('created_at', None)
        self.last_modified_by = kwargs.get('last_modified_by', None)
        self.last_modified_at = kwargs.get('last_modified_at', None)

    def __str__(self) -> str:
        return 'AuditingBase{' \
               + f'super={super(IdBase, self).__str__()}' \
               + f'id={self.created_by}' \
               + f'id={self.created_at}' \
               + f'id={self.last_modified_by}' \
               + f'id={self.last_modified_at}' \
               + '}'
