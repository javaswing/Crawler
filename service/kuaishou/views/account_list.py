from utils.error_code import ErrorCode
from utils.reply import reply
from ..models import accounts, accounts_live


def account_list():
    """
    获取快手账号
    """
    return reply(ErrorCode.OK, "OK", accounts.load())


def account_live_list():
    """
    获取快手直播账号
    """
    return reply(ErrorCode.OK, "OK", accounts_live.load())
