# -*- coding: utf-8 -*-

"""
@author: takeEasy9
@description: 文件服务
@version: 1.0.0
@since: 2024/5/18 17:40
"""
import os
import subprocess

from app.conf.logConfiguration import logger
from app.utils.singleton_util import singletonContainer


def upload_file(bucket_name, object_name, file_path, content_type="application/octet-stream") -> bool:
    logger.info(f"开始上传文件 file_path={file_path} 至minio bucket_name={bucket_name}, object_name={object_name}")
    try:

        minio_client = singletonContainer.get_instance_by_name("minio_client")
        if not minio_client.bucket_exists(bucket_name):
            logger.info(f"Bucket '{bucket_name}' 不存在, 需创建Bucket")
            minio_client.make_bucket(bucket_name)
        minio_client.fput_object(bucket_name, object_name, file_path, content_type)
        return True
    except Exception as e:
        logger.error(f"上传文件至minio失败, 原因是:{e}")
        return False


async def doc2pdf_linux(doc_path, out_dir, rm_doc=False):
    logger.info(f"开始将文档: {doc_path} 文档转换为 outdir: {out_dir}目录下的pdf文件")
    cmd = 'libreoffice7.4 --headless --convert-to pdf'.split() + [doc_path] + ['--outdir'] + [out_dir]
    p = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    stdout, stderr = p.communicate()
    if stderr:
        logger.info(f"将文档转换为pdf失败, 原因是 {stderr}")
        raise subprocess.SubprocessError(stderr)
    logger.info(f"将文档: {doc_path} 文档转换为 outdir: {out_dir}目录下的pdf文件成功")
    if rm_doc:
        os.remove(doc_path)
