
# -*- coding: utf-8 -*-

"""
@author: takeEasy9
@description: 生成word文档并发送邮件
@version: 1.0.0
@since: 2024/5/18 17:36
"""
import asyncio
import os
import uuid
from os.path import basename
from typing import List

from docxtpl import DocxTemplate
from fastapi import UploadFile
from jinja2 import FileSystemLoader, Environment
from starlette.background import BackgroundTask
from starlette.responses import FileResponse

from app.common.error_code_msg import GuiErrorCodeMsg, CallableErrorCodeMsg
from app.conf.env import environment
from app.conf.logConfiguration import logger
from app.model.API_VO import StockDocDataVO, StockMailVO
from app.serice.file_service import doc2pdf_linux
from app.serice.mail_service import send_mail, send_short_message
from app.utils.file_util import zip_dir, remove_dir
from app.utils.response_util import response_error, response_ok


def get_doc_render_datas(raw_render_data: dict[str, list[StockDocDataVO]]) -> dict:
    """ 获取 doc 模板渲染数据 """
    trading_date_dict = {}
    for trade_date, stocks in raw_render_data.items():
        if trade_date not in trading_date_dict.keys():
            trading_date_dict[trade_date] = {
                "productName": "底稿",
                'tradingDay': trade_date,
                "dailyGoldList": stocks
            }
        if any(trade_date != stock.tradeDate for stock in stocks):
            logger.error(f"底稿交易日 {trade_date} 交易日不一致")
    return trading_date_dict


async def gen_convert(tpl, render_data, trading_date, docx_tmp_dir) -> bool:
    file_name = f"工作底稿_{trading_date}"
    try:
        # word 模板数据填充
        tpl.render(render_data)
        doc_path = f"{docx_tmp_dir}{os.sep}{file_name}.docx"
        logger.info(f"开始生成{file_name}.docx文件")
        # 保存填充后的文件
        tpl.save(doc_path)
        logger.info(f"生成{file_name}完成, 开始转换{file_name}为pdf文件")
        # 转换为pdf
        await doc2pdf_linux(doc_path, docx_tmp_dir, rm_doc=False)
        logger.info(f"生成{file_name} pdf文件完成")
        # 上传到minio
        pdf_path = f"{docx_tmp_dir}{os.sep}{file_name}.pdf"
        # upload_doc = upload_file('doc', f'{file_name}.docx', doc_path, "application/docx")
        os.remove(doc_path)
        # upload_pdf = upload_file('doc', f'{file_name}.pdf', pdf_path, 'application/pdf')
        # logger.info(f"上传{file_name}.docx文件到minio,结果是:{upload_doc}, 上传{file_name}.pdf文件到minio,结果是:{upload_pdf}")
        return True
    except Exception as e:
        logger.error(f"生成 {file_name}.docx 并转换为pdf上传至 MinIO失败, 原因是: {e}")
        return False


async def gen_stock_doc_file(gold_stock_send_mail: StockMailVO) -> dict:
    """ 生成底稿文件 """
    try:
        doc_render_datas = get_doc_render_datas(gold_stock_send_mail.docRenderDatas)
        docx_tmp_dir = f"tmp_docx_{str(uuid.uuid4())}"
        if not os.path.exists(docx_tmp_dir):
            os.mkdir(docx_tmp_dir)
        doc_tpl = DocxTemplate(os.path.join(os.getcwd(), "app/templates/word/daily_gold_stock_template.docx"))
        tasks = set()
        for trading_date, data in doc_render_datas.items():
            task = asyncio.create_task(gen_convert(doc_tpl, data, trading_date, docx_tmp_dir))
            task.add_done_callback(tasks.discard)
            tasks.add(task)
        # 等待所有文件生成、转换、上传
        task_results = await asyncio.gather(*tasks)
        if not all(task_results):
            logger.error("存在生成、转换、上传失败的文件")
            return response_error(GuiErrorCodeMsg.DAILY_GOLD_STOCK_GEN_DOC_SEND_MAIL_FAIL)
        jinja2_env = Environment(loader=FileSystemLoader(os.path.join(os.getcwd(), 'app/templates/mail')))
        mail_template = jinja2_env.get_template('investment_proposal.jinja')
        zip_tmp_dir = f"tmp_zip_{str(uuid.uuid4())}"
        start_date = min(gold_stock_send_mail.docRenderDatas.keys())
        end_date = max(gold_stock_send_mail.docRenderDatas.keys())
        logger.info(f"本次生成工作底稿文件的日期范围为{start_date}-{end_date}")
        if len(doc_render_datas) > 1:
            data_range = f"{start_date}-{end_date}"
            subject = f"工作底稿 {data_range}"
            mail_content = mail_template.render(date=data_range,
                                                product_name="")
            if not os.path.exists(zip_tmp_dir):
                os.mkdir(zip_tmp_dir)
            attachment_file = f"{zip_tmp_dir}{os.sep}工作底稿_{data_range}.zip"
            # 压缩文件
            zip_dir(docx_tmp_dir, attachment_file)
        else:
            subject = f"工作底稿 {start_date}"
            mail_content = mail_template.render(date=start_date, product_name="")
            attachment_file = f"{docx_tmp_dir}{os.sep}工作底稿_{start_date}.pdf"
        # 读取文件
        attachment = {}
        logger.info(f"开始读取文件{attachment_file}作为邮件附件")
        with open(attachment_file, 'rb') as f:
            attachment[basename(attachment_file)] = f.read()
        # 发送邮件
        logger.info("开始发送底稿文件邮件")
        default_bcc = environment.get_property("mail.default-bcc")
        if gold_stock_send_mail.bcc:
            if gold_stock_send_mail.bcc.find(default_bcc) == -1:
                blind_carbon_copy = gold_stock_send_mail.bcc + ',' + default_bcc
            else:
                blind_carbon_copy = gold_stock_send_mail.bcc
        else:
            blind_carbon_copy = default_bcc
        send_res = send_mail(to=gold_stock_send_mail.to,
                             cc=gold_stock_send_mail.cc,
                             bcc=blind_carbon_copy,
                             subject=subject,
                             content=mail_content,
                             attachments=attachment)
        # 删除临时文件夹
        remove_dir(os.path.join(os.getcwd(), docx_tmp_dir))
        remove_dir(os.path.join(os.getcwd(), zip_tmp_dir))
        if send_res:
            logger.info("发送底稿文件邮件成功")
            return response_ok(GuiErrorCodeMsg.DAILY_GOLD_STOCK_GEN_DOC_SEND_MAIL_SUCCESS, 1)
        else:
            logger.info("发送底稿文件邮件失败")
            return response_error(GuiErrorCodeMsg.DAILY_GOLD_STOCK_GEN_DOC_SEND_MAIL_FAIL)
    except Exception as e:
        error_msg = f"生成底稿文件并发送邮件失败,原因是:{e}"
        logger.error(error_msg)
        send_short_message(error_msg)
        return response_error(GuiErrorCodeMsg.DAILY_GOLD_STOCK_GEN_DOC_SEND_MAIL_FAIL)


async def save_convert(tmp_dir, file) -> bool:
    try:
        logger.info(f"开始转换{file.filename}为pdf文件")
        content = await file.read()
        doc_path = f"{tmp_dir}{os.sep}{file.filename}"
        with open(doc_path, "wb") as tmp:
            tmp.write(content)
        await doc2pdf_linux(doc_path, tmp_dir, rm_doc=True)
        logger.info(f"转换{file.filename}为pdf文件成功")
        return True
    except Exception as e:
        logger.error(f"转换{file.filename}为pdf文件失败, 原因是: {e}")
        return False


def word_doc_to_pdf_background(docx_tmp_dir, zip_tmp_dir):
    remove_dir(docx_tmp_dir)
    remove_dir(zip_tmp_dir)


async def word_doc_to_pdf(files: List[UploadFile]):

    docx_tmp_dir = f"tmp_docx_{str(uuid.uuid4())}"
    try:
        logger.info(f"创建 word 文件转 pdf 临时保存的文件夹: {docx_tmp_dir}")
        if not os.path.exists(docx_tmp_dir):
            os.mkdir(docx_tmp_dir)
        tasks = set()
        for file in files:
            task = asyncio.create_task(save_convert(docx_tmp_dir, file))
            task.add_done_callback(tasks.discard)
            tasks.add(task)
        # 等待所有任务完成
        task_results = await asyncio.gather(*tasks)
        if not all(task_results):
            logger.error("存在转换 pdf 失败的 word 文件")
            # 删除临时文件夹
            remove_dir(os.path.join(os.getcwd(), docx_tmp_dir))
            return response_error(CallableErrorCodeMsg.WORD_CONVERT_TO_PDF_SUCCESS)
        zip_tmp_dir = f"tmp_zip_{str(uuid.uuid4())}"
        if len(files) > 1:
            if not os.path.exists(zip_tmp_dir):
                os.mkdir(zip_tmp_dir)
            final_path = f"{zip_tmp_dir}{os.sep}{str(uuid.uuid4())}.zip"
            zip_dir(docx_tmp_dir, final_path)
        else:
            original_filename = os.path.splitext(files[0].filename)[0]
            final_path = f"{docx_tmp_dir}{os.sep}{original_filename}.pdf"
        logger.info(f"本次将 {len(files)} 个 word 文件转 pdf 成功")

        return FileResponse(path=final_path,
                            filename=basename(final_path),
                            background=BackgroundTask(word_doc_to_pdf_background, docx_tmp_dir, zip_tmp_dir))
    except Exception as e:
        logger.error(f"word 文件转 pdf 失败, 原因是: {e}")
        # 删除临时文件夹
        remove_dir(os.path.join(os.getcwd(), docx_tmp_dir))
        return response_error(CallableErrorCodeMsg.WORD_CONVERT_TO_PDF_SUCCESS)
