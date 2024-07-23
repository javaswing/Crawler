import json

import requests
from bs4 import BeautifulSoup

from lib.logger import logger
from . import common
from .common import LIVE_HOST


def request_user_full(k_id: str, cookie: str) -> tuple[dict, bool]:
    """
    请求快手全量用户信息
    """
    ret = {}
    url = f'{LIVE_HOST}/u/{k_id}'
    print(url)
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0",
        "sec-ch-ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Microsoft Edge\";v=\"126\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"macOS\""
    }
    cookies = {
        "did": "web_e10acf909ca50dd2b45cccf7587c201a",
        "userId": "1642623350",
        "kuaishou.live.bfb1s": "7206d814e5c089a58c910ed8bf52ace5",
        "clientid": "3",
        "client_key": "65890b29",
        # "kpn": "GAME_ZONE",
        "kuaishou.live.web_st": "ChRrdWFpc2hvdS5saXZlLndlYi5zdBKgAdSn3j0vbKMYfpkpMkbqg1ELAw-NTtnxIYCotLHYFwtYEj1GgyJMVByWEcd4xq0nXM6tNDdpwQb485SRytpd8ese7lYW9HX0is8VFe-8x2TAxAzbUJYmfQdXFnJCZoEyJUkJzT6otUNSkER1OmNbyXBz3tErhnEpZwp2w-LyP6QgIflNsEvAaxA0UPdvkPn9nB3SfgkUzIHXuMQkZevYPssaEoJNhwQ4OUDtgURWN6k9Xgm8PSIg-LrQEsTk0qBGsKMhHG1ci-AHTqO2TP8H0YBVAnwBbXYoBTAB",
        "kuaishou.live.web_ph": "0fa4fbc81c2554b95f0ef9157098b9f269e2"
    }
    response_html = None
    try:
        response = requests.get(url=url, headers=headers, cookies=cookies)
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
            print(json_str_fixed)
            try:
                initial_state = json.loads(json_str_fixed)
                author_info = initial_state.get('liveroom', {}).get('playList', [])[0].get('author', {})
                ret = author_info
                # 提取并解析 author 信息
                if author_info is not None:
                    print(author_info)
                else:
                    logger.warning('Author information not found in __INITIAL_STATE__')
            except json.JSONDecodeError as e:
                logger.error(f"Error decoding JSON: {e}")
        else:
            logger.warning('Script tag with __INITIAL_STATE__ not found')

    return ret, True
