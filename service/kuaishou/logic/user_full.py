import json

import requests
from bs4 import BeautifulSoup

from lib.logger import logger
from . import common
from .common import LIVE_HOST


def request_user_full(id: str, cookie: str) -> tuple[dict, bool]:
    """
    请求快手全量用户信息
    """
    ret = {}

    url = f'{LIVE_HOST}/u/{id}'

    print(url)

    headers = {"cookie": cookie}
    headers.update(common.COMMON_HEADERS)
    response_html = None
    try:
        response = requests.get(url=url, headers=headers)
        response_html = response.text
    except requests.exceptions.HTTPError as http_err:
        logger.error(f'HTTP error occurred: {http_err}')
    except Exception as err:
        logger.error(f'Other error occurred: {err}')

    # 提取特定内容
    if response_html:
        soup = BeautifulSoup(response_html, 'html.parser')
        # 查找包含 'window.__INITIAL_STATE__' 的脚本标签
        script_tag = soup.find('script', text=lambda x: x and 'window.__INITIAL_STATE__' in x)

        if script_tag:
            # 提取并解析 'window.__INITIAL_STATE__' 的 JSON 数据
            script_content = script_tag.string
            start = script_content.find('window.__INITIAL_STATE__=') + len('window.__INITIAL_STATE__=')
            end = script_content.find(';(function()')
            json_data = script_content[start:end]
            json_str_fixed = json_data.replace('undefined', 'null')
            logger.debug(json_str_fixed)
            try:
                initial_state = json.loads(json_str_fixed)
                author_info = initial_state.get('liveroom', {}).get('playList', [])[0].get('author', {})
                ret = author_info
                # 提取并解析 author 信息
                if author_info is not None:
                    logger.info('Author Info:', author_info)
                else:
                    logger.warning('Author information not found in __INITIAL_STATE__')
            except json.JSONDecodeError as e:
                logger.error(f"Error decoding JSON: {e}")
        else:
            logger.warning('Script tag with __INITIAL_STATE__ not found')

    return ret, True
