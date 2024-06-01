# -*- coding: utf-8 -*-

"""
@author: takeEasy9
@description: file util
@version: 1.0.0
@since: 2024/1/28 11:51
"""
import os
import zipfile
from pathlib import Path
from zipfile import ZipFile



def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def touch_file(path: str, override: bool = False):
    f = Path(path)
    if f.is_file():
        if override:
            with open(f, 'w', encoding='utf-8') as file:
                pass
    else:
        with open(f, 'w', encoding='utf-8') as file:
            pass


def zip_dir(zip_target_dir, zip_file_name, dir_stripe=True, compression=zipfile.ZIP_STORED) -> bool:
    """
    创建zip文件
    :param zip_target_dir: zip文件目标目录
    :param zip_file_name: zip文件名称
     :param dir_stripe: 是否去除目录层级
    :param compression: 压缩方式
    :return: True-成功 False-失败
    """
    from app.conf.logConfiguration import logger
    logger.info(f"开始将文件下 {zip_target_dir} 文件及目录压缩为zip文件 {zip_file_name}")
    try:
        with ZipFile(zip_file_name, 'w', compression) as file:
            # 遍历文件夹
            for dir_, sub_dir, files in os.walk(zip_target_dir):
                if dir_stripe:
                    fpath = dir_.replace(zip_target_dir, '')
                    fpath = fpath and fpath + os.sep or ''
                    for f in files:
                        file.write(os.path.join(dir_, f), fpath + f)
                else:
                    file.write(dir_)
                    for f in files:
                        file.write(os.path.join(dir_, f))
        return True
    except Exception as e:
        logger.error(f"创建{zip_file_name}zip文件失败, 原因是:{e}")
        print(e)
        return False


def remove_dir(target_dir) -> bool:
    """
    删除目录
    :param target_dir: 目标目录
    :return: True-成功 False-失败
    """
    from app.conf.logConfiguration import logger
    logger.info(f"开始删除目录 {target_dir}")
    try:
        if not os.path.exists(target_dir):
            logger.info(f"待删除目录 {target_dir}不存在, 无需删除")
            return True
        for root, dirs, files in os.walk(target_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(target_dir)
        return True
    except Exception as e:
        logger.error(f"删除目录失败, 原因是:{e}")
        return False
