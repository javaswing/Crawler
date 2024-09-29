from .common import common_request, load_graphql_queries, GraphqlQuery


def request_search(keyword: str, cookie: str,  offset: int = 0, limit: int = 20, search_type: str = 'video',) -> tuple[dict, bool]:
    """
    请求快手获取搜索信息
    """
    pcursor = ''
    headers = {"Cookie": cookie}
    page_size = 20
    start_page = int((offset - 1) / page_size) + 1
    end_page = int((offset + limit - 1) / page_size) + 1
    ret = []
    search_session_id = None
    search_user_model = search_type == 'user'
    for page in range(start_page, end_page + 1):
        if page - 1 > 0:
            pcursor = str(page - 1)
        data = {
            "operationName": "visionSearchPhoto" if not search_user_model else "graphqlSearchUser",
            "variables": {
                "keyword": keyword,
            },
            "query": load_graphql_queries(GraphqlQuery.SEARCH) if not search_user_model else load_graphql_queries(GraphqlQuery.SEARCH_USER)
        }
        if not search_user_model:
            data['variables']['pcursor'] = pcursor
            data['variables']['page'] = "search"
            if search_session_id and search_session_id != '':
                data['variables']['searchSessionId'] = search_session_id
        else:
            headers['Referer'] = f'https://www.kuaishou.com/search/author?searchKey={keyword}'
        resp, succ = common_request(data, headers)
        if not succ:
            return {}, succ
        if not search_user_model:
            data = resp.get('data', {}).get('visionSearchPhoto', {}).get('feeds', [])
            search_session_id = resp.get('data', {}).get('visionSearchPhoto', {}).get('searchSessionId', '')
            ret.extend(data)
            ret = ret[(offset % page_size):(offset % page_size + limit)]
        else:
            data = resp.get('data', {}).get('visionSearchUser', {}).get('users', [])
            search_session_id = resp.get('data', {}).get('visionSearchUser', {}).get('searchSessionId', '')
            ret.extend(data)
    return ret, succ
