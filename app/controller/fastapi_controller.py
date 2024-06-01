# -*- coding: utf-8 -*-

"""
@author: takeEasy9
@description: controller
@version: 1.0.0
@since: 2024/5/18 16:28
"""
import os
from typing import List

from fastapi import APIRouter, Form, UploadFile, File

from app.common.error_code_msg import GuiErrorCodeMsg, CallableErrorCodeMsg
from app.common.exception import MethodArgumentNotValidException
from app.conf.logConfiguration import logger
from app.model.API_VO import StockMailVO
from app.serice.gen_stock_doc_service import word_doc_to_pdf, gen_stock_doc_file
from app.serice.mail_service import is_mail_addresses_invalid, send_mail
from app.utils.enum_util import EnumEntity
from app.utils.response_util import response_error, response_ok

fastapi_router = APIRouter(
    prefix="/api/v1",
    tags=["dataSync"],
    responses={404: {"description": "Not found"}},
)


@fastapi_router.post("/genDocAndSendMail", summary="生成word文件并发送邮件", )
async def gen_stock_doc(stock_mail: StockMailVO):
    logger.info(f"开始根据 {stock_mail} 数据生成每日金股底稿并发送邮件")
    if is_mail_addresses_invalid(stock_mail.to, False) \
            or is_mail_addresses_invalid(stock_mail.cc, True) \
            or is_mail_addresses_invalid(stock_mail.bcc, True):
        logger.error(f"待生成底稿并发送邮件, 邮件地址 收件人地址 {stock_mail.to}, "
                     f"抄送人人地址 {stock_mail.cc}, "
                     f"密抄送人人地址 {stock_mail.bcc} 存在无效的邮件地址, 请检查")
    if stock_mail.docRenderDatas is None or len(stock_mail.docRenderDatas) == 0:
        logger.error("待生成底稿文件的 docRenderDatas 数据不存在, 请检查")
        return response_error(GuiErrorCodeMsg.ACCESS_PARAMETER_INVALID)

    return await gen_stock_doc_file(stock_mail)


@fastapi_router.post("/sendMail", summary="邮件发送接口", )
async def send_mail_api(to: str = Form(...),
                        cc: str = Form(default=None),
                        bcc: str = Form(default=None),
                        subject: str = Form(...),
                        content: str = Form(...),
                        mail_content_type: str = Form(alias="mailContentType"),
                        attachments: List[UploadFile] = File(default=None)) -> dict:

    try:

        if EnumEntity.MailContentType.MAIL_CONTENT_TYPE_PLAIN_TEXT.get_value() == mail_content_type:
            subtype = "plain"
        elif EnumEntity.MailContentType.MAIL_CONTENT_TYPE_HTML.get_value() == mail_content_type:
            subtype = "html"
        else:
            logger.error(f"邮件内容类型参数 {mail_content_type} 不是有效的值(1-简单文本, 2-HTML)")
            return response_error(GuiErrorCodeMsg.ACCESS_PARAMETER_INVALID)
        logger.info(f"发送收件人地址 {to} , 抄送人地址 {cc}, 密抄送人地址 {bcc},"
                    f" 邮件主题 {subject}, 邮件内容 {content}, 邮件内容类型 {mail_content_type},"
                    f" 邮件附件有 {0 if attachments is None else len(attachments)} 个")
        name_bytes_dict = {}
        for file in attachments or []:
            name_bytes_dict[file.filename] = await file.read()
        # 发送邮件
        ret = send_mail(to,
                        cc,
                        bcc,
                        subject,
                        content,
                        subtype=subtype,
                        attachments=name_bytes_dict)
        if ret:
            logger.info(f"发送收件人地址 {to} , 抄送人地址 {cc}, 密抄送人地址 {bcc}的邮件成功")
            return response_ok(CallableErrorCodeMsg.MAIL_SEND_SUCCESS, 1)
        else:
            logger.error(f"发送收件人地址 {to} , 抄送人地址 {cc}, 密抄送人地址 {bcc}的邮件失败")
            return response_error(CallableErrorCodeMsg.MAIL_SEND_FAILED)
    except MethodArgumentNotValidException as e:
        logger.error(f"待发送邮件参数不合法, 原因是 {e}")
        return response_error(GuiErrorCodeMsg.ACCESS_PARAMETER_INVALID)
    except Exception as e:
        logger.error(f"邮件服务调用失败,原因是 {e}")
        return response_error(CallableErrorCodeMsg.CALLABLE_FAILED)


@fastapi_router.post("/word2pdf", summary="word文档转pdf接口", )
async def word2pdf(files: List[UploadFile] = File(default=None)) -> dict:
    if not files:
        logger.error("待转换的 word 文件参数无效")
        return response_error(GuiErrorCodeMsg.ACCESS_PARAMETER_INVALID)
    logger.info("本次共有 <{}> 个待转换为 pdf 的 word 文件")
    if any(os.path.splitext(f.filename)[-1].lower() not in {".doc", ".docx"} for f in files):
        logger.error("待转换的 word 文件, 存在不是 doc、docx格式的文件")
        return response_error(GuiErrorCodeMsg.ACCESS_PARAMETER_INVALID)
    return await word_doc_to_pdf(files)
