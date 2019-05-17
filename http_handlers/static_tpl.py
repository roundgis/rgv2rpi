# -*- coding: utf-8 -*-
import os.path as os_path
from cyclone import web as cyclone_web
import rgv_consts
import settings


class AbstractHandler(cyclone_web.RequestHandler):
    def initialize(self, **kwargs):
        self.tpl_param_tbl = {}

    def get(self, path, include_body=True):
        self.SetExtraHeaders()
        tpl_name = path
        if tpl_name in self.tpl_param_tbl:
            self.render(tpl_name, **self.tpl_param_tbl[tpl_name])
        else:
            self.render(tpl_name)

    def SetExtraHeaders(self):
        raise NotImplementedError()


class JsHandler(AbstractHandler):
    def initialize(self, **kwargs):
        self.tpl_param_tbl = {
            'em_rpc.js': {
                'url': rgv_consts.URLs.API_EM
            },

            'basic_user_rpc.js': {
                'url': rgv_consts.URLs.API_BASIC_USER
            },

            'group_adm_rpc.js': {
                'url': rgv_consts.URLs.API_GROUP_ADM
            },

            'switch_adm_rpc.js': {
                'url': rgv_consts.URLs.API_SWITCH_ADM
            },

            'sensor_adm_rpc.js': {
                'url': rgv_consts.URLs.API_SENSOR_ADM
            },

            'sensor_measurement_rpc.js': {
                'url': rgv_consts.URLs.API_SENSOR_MEASUREMENT
            },

            'sensor_type_adm_rpc.js': {
                'url': rgv_consts.URLs.API_SENSOR_TYPE_ADM
            },

            'rggw_adm_rpc.js': {
                'url': rgv_consts.URLs.API_RGGW_ADM
            },

            'user_adm_rpc.js': {
                'url': rgv_consts.URLs.API_USER_ADM
            },

            'camera_rpc.js': {
                'url': rgv_consts.URLs.API_CAMERA
            },

            'sys_cfg_rpc.js': {
                'url': rgv_consts.URLs.API_SYS_CFG
            },

            'sensor_trigger_rpc.js': {
                'url': rgv_consts.URLs.API_SENSOR_TRIGGER
            }
        }

    def SetExtraHeaders(self):
        self.set_header('Content-Type', 'text/javascript')

    def get_template_path(self):
        return os_path.join(settings.WEB['static_path'], settings.WEB['js_dir'])


class CssHandler(AbstractHandler):
    def SetExtraHeaders(self):
        self.set_header('Content-Type', 'text/css')

    def get_template_path(self):
        return os_path.join(settings.WEB['static_path'], settings.WEB['css_dir'])


class DojoTplHandler(AbstractHandler):
    def SetExtraHeaders(self):
        self.set_header('Content-Type', 'text/html')

    def get_template_path(self):
        return os_path.join(settings.WEB['static_path'], settings.WEB['template_dir'])

