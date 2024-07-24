from flask import Blueprint
from . import views

kuaishou = Blueprint('kuaishou', __name__)

kuaishou.add_url_rule('/add_account', 'add_account', views.add_account, methods=['POST'])
kuaishou.add_url_rule('/add_account_live', 'add_account_live', views.add_account_live, methods=['POST'])
kuaishou.add_url_rule('/account_list', 'account_list', views.account_list, methods=['GET'])
kuaishou.add_url_rule('/account_live_list', 'account_live_list', views.account_live_list, methods=['GET'])
kuaishou.add_url_rule('/detail', 'detail', views.detail, methods=['GET'])
kuaishou.add_url_rule('/comments', 'comments', views.comments, methods=['GET'])
kuaishou.add_url_rule('/replys', 'replys', views.replys, methods=['GET'])
kuaishou.add_url_rule('/search', 'search', views.search, methods=['GET'])
kuaishou.add_url_rule('/user', 'user', views.user, methods=['GET'])
kuaishou.add_url_rule('/user_full', 'user_full', views.user_full, methods=['GET'])