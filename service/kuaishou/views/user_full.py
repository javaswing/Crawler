import random

from flask import request

from lib.logger import logger
from utils.error_code import ErrorCode
from utils.reply import reply
from ..logic.user_full import request_user_full
from ..models import accounts_live


# route
def user_full():
    """
    获取用户信息
    """
    u_id = request.args.get('id', '')

    _accounts = accounts_live.load()
    random.shuffle(_accounts)
    for account in _accounts:
        if account.get('expired', 0) == 1:
            continue
        res, succ = request_user_full(u_id, account.get('cookie', ''))
        if not succ:
            accounts_live.expire(account.get('id', ''))
        if res == {} or not succ:
            continue
        logger.info(f'get user detail success, id: {u_id}, res: {res}')
        return reply(ErrorCode.OK, '成功', res)
    logger.warning(f'get user detail failed, don\'t have enough effective account. id: {u_id}')
    return reply(ErrorCode.INTERNAL_ERROR, '内部错误请重试')
