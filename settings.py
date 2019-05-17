import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_PATH = "/home/mathgl/rglog"
HOST = "rg3.esis.vip"
HTTP_PORT = 9004
URL_PREFIX = r'/rgv'
REDIS = {
    "host": "localhost",
    "port": 21999
}
WEB = {
    "static_path": "/home/mathgl/rgw_web",
    "export_path": "/home/mathgl/rglog",
    "login_page_bkg": "login_roundgis_bkg3.png",
    'js_dir': "rgv_js",
    'template_dir': "rgv_templates",
    'tpl_dir': "rgv_tpls",
    'css_dir': "rgv_css"
}

BIZ_DB = {
    "path": "/home/mathgl/rgv_biz.db3",
    "ttl": 3*86400
}

LOG_DB = {
    "path": "/home/mathgl/rgv_log.db3",
    "ttl": 32*86400
}

GW_PORT = 11403
GW_ECHO_PORT = 11404
