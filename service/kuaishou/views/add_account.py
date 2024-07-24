import flask
from utils.error_code import ErrorCode
from utils.reply import reply
from ..models import accounts, accounts_live
from lib.logger import logger


def add_account():
    """
    添加快手账号
    """

    id = flask.request.json.get('id', '')
    cookie = flask.request.json.get('cookie', '')
    if id == '' or cookie == '':
        logger.error(f'id or cookie is empty, id: {id}, cookie: {cookie}')
        return reply(ErrorCode.PARAMETER_ERROR, "id and cookie is required")

    accounts.save(id, cookie, 0)
    logger.info(f'kuaishou add account, id: {id}, cookie: {cookie}')
    return reply()


def add_account_live():
    """
    添加快手直播账号
    """
    id = flask.request.json.get('id', '')
    cookie = flask.request.json.get('cookie', '')
    if id == '' or cookie == '':
        logger.error(f'id or cookie is empty, id: {id}, cookie: {cookie}')
        return reply(ErrorCode.PARAMETER_ERROR, "id and cookie is required")

    accounts_live.save(id, cookie, 0)
    logger.info(f'kuaishou live add account, id: {id}, cookie: {cookie}')
    return reply()