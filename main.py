from flask import Flask
from service.douyin.urls import douyin
from service.kuaishou.urls import kuaishou
from service.bilibili.urls import bilibili
from service.xhs.urls import xhs
from service.taobao.urls import taobao
from service.jd.urls import jd
from service.weibo.urls import weibo
from lib.logger import logger
import yaml

app = Flask(__name__)
app.register_blueprint(douyin, url_prefix="/douyin")
app.register_blueprint(kuaishou, url_prefix="/kuaishou")
app.register_blueprint(bilibili, url_prefix="/bilibili")
app.register_blueprint(xhs, url_prefix="/xhs")
app.register_blueprint(taobao, url_prefix="/taobao")
app.register_blueprint(jd, url_prefix="/jd")
app.register_blueprint(weibo, url_prefix="/weibo")


def init_service():
    config_file = "config/config.yaml"
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)
    logger.setup(config)
    app.logger.handlers = logger.get_logger().handlers
    app.logger.setLevel(logger.get_logger().level)


init_service()

if __name__ == '__main__':
    app.run(debug=True, port=8080)
