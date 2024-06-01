# -*- coding: utf-8 -*-

"""
@author: takeEasy9
@description: 邮件服务
@version: 1.0.0
@since: 2024/5/18 16:58
"""
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate

import requests

from app.common.error_code_msg import GuiErrorCodeMsg
from app.common.exception import MethodArgumentNotValidException
from app.conf.env import environment
from app.conf.logConfiguration import logger
from app.utils.constant_util import ConstantUtil
from app.utils.enum_util import CallableCode
from app.utils.singleton_util import singletonContainer


def send_short_message(msg: str, mobiles: list[str] = None) -> bool:
    if not msg:
        logger.error("待发送短信内容为空, 无法调用短信服务")
        return False
    profile = environment.get_property("profile")
    if profile != ConstantUtil.PROFILE_PROD:
        logger.info(f"当前环境为 {profile}, 不调用短信服务")
        return True
    if len(msg) > ConstantUtil.SHORT_MESSAGE_CONTENT_BOUND:
        msg = msg[:ConstantUtil.SHORT_MESSAGE_CONTENT_BOUND] + '...'
    # 发送告警短信
    try:
        if not mobiles:
            mobiles = environment.get_property("sms.mobiles")
        else:
            default_mobiles = environment.get_property("sms.default-mobiles")
            mobiles.extend(default_mobiles)
        response = requests.post(ConstantUtil.SHORT_MESSAGE_URL,
                                 headers={'content-type': 'application/json'},
                                 json={'mobiles': mobiles, 'content': msg})
        if not response \
                or not response.json() \
                or 'code' not in response.json() \
                or response.json().get('code') != CallableCode.CALLABLE_SUCCESS.get_value():
            logger.error(f"短信服务调用失败,原因是 {response.json()}")
        logger.info("短信服务调用成功")
    except Exception as e:
        logger.error(f"短信服务调用失败,原因是 {e}")
        return False


def is_mail_address_invalid(addr: str) -> bool:
    return not addr or not ConstantUtil.MAIL_CHECK_PATTERN.match(addr)


def is_mail_addresses_invalid(addr: str, defaulted: bool) -> bool:
    if defaulted:
        if not addr:
            return False
    else:
        if not addr:
            return True
    addresses = addr.split(',')
    for address in addresses:
        if is_mail_address_invalid(address):
            return True
    return False


def check_send_mail_param_invalid(to: str, cc: str, bcc: str, subject: str, content: str, subtype='html') -> bool:
    if is_mail_addresses_invalid(to, False):
        logger.error(f"收件人邮件地址 {to} 无效, 请检查")
        return True
    if is_mail_addresses_invalid(cc, True):
        logger.error(f"抄送人地址 {cc} 无效, 请检查")
        return True
    if is_mail_addresses_invalid(bcc, True):
        logger.error(f"收件人邮件地址 {bcc} 无效, 请检查")
        return True
    if not subject:
        logger.error("邮件主题为空, 请检查")
        return True
    if not content:
        logger.error("邮件内容为空, 请检查")
        return True
    if subtype not in {'html', 'plain'}:
        logger.error(f"邮件内容类型 {subtype} 无效, 请检查")
        return True
    return False


def send_mail(to: str, cc: str, bcc: str, subject: str, content: str, subtype='html',
              attachments: dict[str, bytes] = None) -> bool:
    """
    发送邮件
    :param to: 收件人地址,多个收件人以,分隔
    :param cc: 抄送人地址,多个收件人以,分隔, 可选参数
    :param bcc: 密抄送人地址,多个收件人以,分隔, 可选参数
    :param subject: 邮件主题
    :param content: 邮件内容
    :param subtype: 邮件内容类型, 可选参数, 默认为html
    :param attachments: 邮件附件, 可选参数
    :return: True-发送成功 False-发送失败
    """

    mail_server = singletonContainer.get_instance_by_name('mail_server')
    logger.info(f"开始发送邮件, 收件人 {to}, 抄送人 {cc}, 密抄送人 {bcc}, 主题 {subject}, 内容 {content}, 内容类型 {subtype}")
    try:
        # 检查参数是否合法
        if check_send_mail_param_invalid(to, cc, bcc, subject, content, subtype):
            raise MethodArgumentNotValidException(GuiErrorCodeMsg.ACCESS_PARAMETER_INVALID.get_code(),
                                                  GuiErrorCodeMsg.ACCESS_PARAMETER_INVALID.get_msg())
        mail_server.connect(environment.get_property("mail.host"))
        mail_server.login(environment.get_property("mail.username"), environment.get_property("mail.password"))
        msg = MIMEMultipart()
        msg['From'] = environment.get_property("mail.username")
        msg['To'] = to
        msg['Cc'] = cc
        msg['Bcc'] = bcc
        msg['Subject'] = subject
        msg['Date'] = formatdate(localtime=True)
        msg.attach(MIMEText(content, subtype, 'utf-8'))
        for filename, file_bytes in attachments.items() or {}:
            part = MIMEApplication(file_bytes, Name=filename)
            part['Content-Disposition'] = f'attachment; filename={filename}'
            msg.attach(part)
        to_list = to.split(',')
        if cc:
            to_list.extend(cc.split(','))
        if bcc:
            to_list.extend(bcc.split(','))
        mail_server.sendmail(msg['From'], to_list, msg.as_bytes())
        return True
    except Exception as e:
        logger.error(f"发送邮件失败, 原因是:{e}")
        return False
    finally:
        mail_server.quit()
