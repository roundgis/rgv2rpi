# -*- coding: utf-8 -*-
from twisted.internet import defer
from twisted.python import log
from cyclone import web as cyclone_web
from cyclone import escape as c_escape
import rgv_consts
import multi_lang
import api_core
import models
import rg_lib
import settings


class UIBase(cyclone_web.RequestHandler):
    async def async_get(self):
        raise NotImplementedError()

    async def async_post(self):
        raise NotImplementedError()

    def get(self):
        return defer.ensureDeferred(self.async_get())

    def post(self):
        return defer.ensureDeferred(self.async_post())


def GetToken(req_handler):
    sid = req_handler.get_cookie(rgv_consts.Cookies.TENANT)
    if sid:
        return sid
    else:
        return req_handler.get_argument('token', '')


class Index(UIBase):
    async def async_get(self):
        self.render(rgv_consts.TPL_NAMES.INDEX)


class AppGroupAdm(UIBase):
    TITLE = "Group Adm powered by RoundGIS Lab"

    async def async_get(self):
        try:
            await api_core.ReqLimit.CheckMinuteRate("AppGroupAdm", rg_lib.Cyclone.TryGetRealIp(self), 3)
            sid = self.get_cookie(rgv_consts.Cookies.TENANT)
            if sid:
                await api_core.Login.CheckRight(sid, (rgv_consts.UserNo.ROOT,))
                self.render(rgv_consts.TPL_NAMES.APP_ADM_GROUP,
                            app_js_dir=settings.WEB['js_dir'],
                            app_css_dir=settings.WEB['css_dir'],
                            app_template_dir=settings.WEB['template_dir'],
                            title=AppGroupAdm.TITLE,
                            sessionid=sid,
                            edit_group_url=rgv_consts.URLs.APP_EDIT_GROUP[1:])
            else:
                self.redirect(rgv_consts.URLs.APP_ADM_LOGIN)
        except rg_lib.RGError as err:
            if models.ErrorTypes.TypeOfAccessOverLimit(err):
                self.finish(rgv_consts.WebContent.ACCESS_OVER_LIMIT)
            elif models.ErrorTypes.TypeOfSessionExpired(err):
                self.redirect(rgv_consts.URLs.APP_ADM_LOGIN)
            elif models.ErrorTypes.TypeOfNoRight(err):
                self.redirect(rgv_consts.URLs.APP_ADM_LOGIN)
            else:
                self.finish(rgv_consts.WebContent.SERVER_ERROR)


class AppEditGroup(UIBase):
    async def async_get(self):
        try:
            await api_core.ReqLimit.CheckMinuteRate("AppEditGroup", rg_lib.Cyclone.TryGetRealIp(self), 3)
            sid = self.get_cookie(rgv_consts.Cookies.TENANT)
            if sid:
                await api_core.Login.CheckRight(sid, (rgv_consts.UserNo.ROOT,))
                edit_mode = self.get_argument("edit_mode")
                if edit_mode == u"edit":
                    uid = self.get_argument(u"groupid")
                    self.render(rgv_consts.TPL_NAMES.APP_EDIT_GROUP,
                                app_js_dir=settings.WEB['js_dir'],
                                app_css_dir=settings.WEB['css_dir'],
                                app_template_dir=settings.WEB['template_dir'],
                                title=u"Edit Group", sessionid=sid,
                                groupid=uid, edit_mode=edit_mode)
                else:
                    self.render(rgv_consts.TPL_NAMES.APP_EDIT_GROUP,
                                app_js_dir=settings.WEB['js_dir'],
                                app_css_dir=settings.WEB['css_dir'],
                                app_template_dir=settings.WEB['template_dir'],
                                title=u"Add Group", sessionid=sid,
                                groupid=u"", edit_mode=edit_mode)
            else:
                self.finish(u"please login")
        except rg_lib.RGError as err:
            if models.ErrorTypes.TypeOfAccessOverLimit(err):
                self.finish(rgv_consts.WebContent.ACCESS_OVER_LIMIT)
            elif models.ErrorTypes.TypeOfSessionExpired(err):
                self.redirect(rgv_consts.URLs.APP_ADM_LOGIN)
            elif models.ErrorTypes.TypeOfNoRight(err):
                self.redirect(rgv_consts.URLs.APP_ADM_LOGIN)
            else:
                self.finish(rgv_consts.WebContent.SERVER_ERROR)


class AppUserAdm(UIBase):
    TITLE = "User Adm powered by RoundGIS Lab"

    async def async_get(self):
        try:
            await api_core.ReqLimit.CheckMinuteRate("AppUserAdm", rg_lib.Cyclone.TryGetRealIp(self), 3)
            sid = self.get_cookie(rgv_consts.Cookies.TENANT)
            if sid:
                await api_core.Login.CheckRight(sid, (rgv_consts.UserNo.ROOT,))
                self.render(rgv_consts.TPL_NAMES.APP_ADM_USER,
                            app_js_dir=settings.WEB['js_dir'],
                            app_css_dir=settings.WEB['css_dir'],
                            app_template_dir=settings.WEB['template_dir'],
                            title=AppUserAdm.TITLE, sessionid=sid,
                            edit_user_url=rgv_consts.URLs.APP_EDIT_USER[1:])
            else:
                self.redirect(rgv_consts.URLs.APP_ADM_LOGIN)
        except rg_lib.RGError as err:
            if models.ErrorTypes.TypeOfAccessOverLimit(err):
                self.finish(rgv_consts.WebContent.ACCESS_OVER_LIMIT)
            elif models.ErrorTypes.TypeOfSessionExpired(err):
                self.redirect(rgv_consts.URLs.APP_ADM_LOGIN)
            elif models.ErrorTypes.TypeOfNoRight(err):
                self.redirect(rgv_consts.URLs.APP_ADM_LOGIN)
            else:
                self.finish(rgv_consts.WebContent.SERVER_ERROR)


class AppEditUser(UIBase):
    def __GetUNoOptions(self):
        return [{"value": rgv_consts.UserNo.TENANT, "label": "tenant"},
                {"value": rgv_consts.UserNo.OPERATOR, "label": "operator"},
                {'value': rgv_consts.UserNo.WATCHER, 'label': "watcher"},
                {"value": rgv_consts.UserNo.ROOT, "label": "root"}]

    async def async_get(self):
        try:
            await api_core.ReqLimit.CheckMinuteRate("AppEditUser", rg_lib.Cyclone.TryGetRealIp(self), 3)
            sid = self.get_cookie(rgv_consts.Cookies.TENANT)
            if sid:
                await api_core.Login.CheckRight(sid, (rgv_consts.UserNo.ROOT,))
                uno_opts = self.__GetUNoOptions()
                edit_mode = self.get_argument("edit_mode")
                if edit_mode == "edit":
                    uid = self.get_argument("userid")
                    self.render(rgv_consts.TPL_NAMES.APP_EDIT_USER,
                                app_js_dir=settings.WEB['js_dir'],
                                app_css_dir=settings.WEB['css_dir'],
                                app_template_dir=settings.WEB['template_dir'],
                                title="Edit User", sessionid=sid,
                                userid=uid, edit_mode=edit_mode, uno_options=uno_opts)
                else:
                    self.render(rgv_consts.TPL_NAMES.APP_EDIT_USER,
                                app_js_dir=settings.WEB['js_dir'],
                                app_css_dir=settings.WEB['css_dir'],
                                app_template_dir=settings.WEB['template_dir'],
                                title="Add User", sessionid=sid,
                                userid="", edit_mode=edit_mode, uno_options=uno_opts)
            else:
                self.finish("please login")
        except rg_lib.RGError as err:
            if models.ErrorTypes.TypeOfAccessOverLimit(err):
                self.finish(rgv_consts.WebContent.ACCESS_OVER_LIMIT)
            elif models.ErrorTypes.TypeOfSessionExpired(err):
                self.redirect(rgv_consts.URLs.APP_ADM_LOGIN)
            elif models.ErrorTypes.TypeOfNoRight(err):
                self.redirect(rgv_consts.URLs.APP_ADM_LOGIN)
            else:
                self.finish(rgv_consts.WebContent.SERVER_ERROR)


class AppAdmSysCommand(UIBase):
    async def async_get(self):
        try:
            await api_core.ReqLimit.CheckMinuteRate("AppAdmSysCommand", rg_lib.Cyclone.TryGetRealIp(self), 3)
            sid = self.get_cookie(rgv_consts.Cookies.TENANT)
            uid = self.get_cookie(rgv_consts.Cookies.USERID)
            if sid:
                await api_core.Login.CheckRight(sid, (rgv_consts.UserNo.ROOT,))
                self.render(rgv_consts.TPL_NAMES.APP_ADM_SYS_COMMAND,
                            app_js_dir=settings.WEB['js_dir'],
                            app_css_dir=settings.WEB['css_dir'],
                            app_template_dir=settings.WEB['template_dir'],
                            title="Sys Command",
                            sessionid=sid, userid=uid)
            else:
                self.redirect(rgv_consts.URLs.APP_ADM_LOGIN)
        except rg_lib.RGError as rgerr:
            if models.ErrorTypes.TypeOfAccessOverLimit(rgerr):
                self.finish(rgv_consts.WebContent.ACCESS_OVER_LIMIT)
            elif models.ErrorTypes.TypeOfNoRight(rgerr):
                self.redirect(rgv_consts.URLs.APP_ADM_LOGIN)
            elif models.ErrorTypes.TypeOfSessionExpired(rgerr):
                self.redirect(rgv_consts.URLs.APP_ADM_LOGIN)
            else:
                self.finish(rgv_consts.WebContent.SERVER_ERROR)


class AppEditRGGW(UIBase):
    async def async_get(self):
        try:
            await api_core.ReqLimit.CheckMinuteRate("AppEditRGGW", rg_lib.Cyclone.TryGetRealIp(self), 3)
            sid = self.get_cookie(rgv_consts.Cookies.TENANT)
            if sid:
                await api_core.Login.CheckRight(sid, (rgv_consts.UserNo.ROOT,))
                edit_mode = self.get_argument("edit_mode")
                if edit_mode == "edit":
                    deviceid = self.get_argument("deviceid")
                    self.render(rgv_consts.TPL_NAMES.APP_EDIT_RGGW,
                                app_js_dir=settings.WEB['js_dir'],
                                app_css_dir=settings.WEB['css_dir'],
                                app_template_dir=settings.WEB['template_dir'],
                                title="Edit RGGW",
                                sessionid=sid, edit_mode=edit_mode, deviceid=deviceid)
                elif edit_mode == "add":
                    self.render(rgv_consts.TPL_NAMES.APP_EDIT_RGGW,
                                app_js_dir=settings.WEB['js_dir'],
                                app_css_dir=settings.WEB['css_dir'],
                                app_template_dir=settings.WEB['template_dir'],
                                title="Add RGGW", sessionid=sid,
                                edit_mode=edit_mode, deviceid=u"")
                else:
                    self.finish("incorrect edit mode")
            else:
                self.finish("please login")
        except rg_lib.RGError as err:
            if models.ErrorTypes.TypeOfAccessOverLimit(err):
                self.finish(rgv_consts.WebContent.ACCESS_OVER_LIMIT)
            elif models.ErrorTypes.TypeOfSessionExpired(err):
                self.redirect(rgv_consts.URLs.APP_ADM_LOGIN)
            elif models.ErrorTypes.TypeOfNoRight(err):
                self.redirect(rgv_consts.URLs.APP_ADM_LOGIN)
            else:
                self.finish(rgv_consts.WebContent.SERVER_ERROR)


class AppAdmRGGW(UIBase):
    def GetTitle(self):
        return "RGGW Adm powered by RoundGIS Lab"

    async def async_get(self):
        try:
            await api_core.ReqLimit.CheckMinuteRate("AppAdmRGGW", rg_lib.Cyclone.TryGetRealIp(self), 3)
            sid = self.get_cookie(rgv_consts.Cookies.TENANT)
            if sid:
                await api_core.Login.CheckRight(sid, (rgv_consts.UserNo.ROOT,))
                self.render(rgv_consts.TPL_NAMES.APP_ADM_RGGW,
                            app_js_dir=settings.WEB['js_dir'],
                            app_css_dir=settings.WEB['css_dir'],
                            app_template_dir=settings.WEB['template_dir'],
                            title=self.GetTitle(),
                            sessionid=sid,
                            edit_rggw_url=rgv_consts.URLs.APP_EDIT_RGGW[1:],
                            q06_view_url=rgv_consts.URLs.VIEW_Q06_LOG[1:],
                            tracker_raw_log_url=rgv_consts.URLs.APP_TRACKER_RAW_LOG[1:])
            else:
                self.redirect(rgv_consts.URLs.APP_ADM_LOGIN)
        except rg_lib.RGError as err:
            if models.ErrorTypes.TypeOfAccessOverLimit(err):
                self.finish(rgv_consts.WebContent.ACCESS_OVER_LIMIT)
            elif models.ErrorTypes.TypeOfSessionExpired(err):
                self.redirect(rgv_consts.URLs.APP_ADM_LOGIN)
            elif models.ErrorTypes.TypeOfNoRight(err):
                self.redirect(rgv_consts.URLs.APP_ADM_LOGIN)
            else:
                self.finish(rgv_consts.WebContent.SERVER_ERROR)


class AppEditSwitch(UIBase):
    async def async_get(self):
        try:
            await api_core.ReqLimit.CheckMinuteRate("AppEditSwitch", rg_lib.Cyclone.TryGetRealIp(self), 3)
            sid = self.get_cookie(rgv_consts.Cookies.TENANT)
            if sid:
                await api_core.Login.CheckRight(sid, (rgv_consts.UserNo.ROOT,))
                edit_mode = self.get_argument("edit_mode")
                if edit_mode == "edit":
                    deviceid = self.get_argument("switchid")
                    self.render(rgv_consts.TPL_NAMES.APP_EDIT_SWITCH,
                                app_js_dir=settings.WEB['js_dir'],
                                app_css_dir=settings.WEB['css_dir'],
                                app_template_dir=settings.WEB['template_dir'],
                                title="Edit Switch",
                                sessionid=sid, edit_mode=edit_mode, switchid=deviceid)
                elif edit_mode == "add":
                    self.render(rgv_consts.TPL_NAMES.APP_EDIT_SWITCH,
                                app_js_dir=settings.WEB['js_dir'],
                                app_css_dir=settings.WEB['css_dir'],
                                app_template_dir=settings.WEB['template_dir'],
                                title="Add Relay Switch", sessionid=sid,
                                edit_mode=edit_mode, switchid="")
                else:
                    self.finish("incorrect edit mode")
            else:
                self.finish("please login")
        except rg_lib.RGError as err:
            if models.ErrorTypes.TypeOfAccessOverLimit(err):
                self.finish(rgv_consts.WebContent.ACCESS_OVER_LIMIT)
            elif models.ErrorTypes.TypeOfSessionExpired(err):
                self.redirect(rgv_consts.URLs.APP_ADM_LOGIN)
            elif models.ErrorTypes.TypeOfNoRight(err):
                self.redirect(rgv_consts.URLs.APP_ADM_LOGIN)
            else:
                self.finish(rgv_consts.WebContent.SERVER_ERROR)


class AppSwitchAdm(UIBase):
    def GetTitle(self):
        return "Switch Adm powered by RoundGIS Lab"

    async def async_get(self):
        try:
            await api_core.ReqLimit.CheckMinuteRate("AppSwitchAdm", rg_lib.Cyclone.TryGetRealIp(self), 3)
            sid = self.get_cookie(rgv_consts.Cookies.TENANT)
            if sid:
                await api_core.Login.CheckRight(sid, (rgv_consts.UserNo.ROOT,))
                self.render(rgv_consts.TPL_NAMES.APP_ADM_SWITCH,
                            app_js_dir=settings.WEB['js_dir'],
                            app_css_dir=settings.WEB['css_dir'],
                            app_template_dir=settings.WEB['template_dir'],
                            title=self.GetTitle(), sessionid=sid,
                            edit_switch_url=rgv_consts.URLs.APP_EDIT_SWITCH[1:])
            else:
                self.redirect(rgv_consts.URLs.APP_ADM_LOGIN)
        except rg_lib.RGError as err:
            if models.ErrorTypes.TypeOfAccessOverLimit(err):
                self.finish(rgv_consts.WebContent.ACCESS_OVER_LIMIT)
            elif models.ErrorTypes.TypeOfSessionExpired(err):
                self.redirect(rgv_consts.URLs.APP_ADM_LOGIN)
            elif models.ErrorTypes.TypeOfNoRight(err):
                self.redirect(rgv_consts.URLs.APP_ADM_LOGIN)
            else:
                self.finish(rgv_consts.WebContent.SERVER_ERROR)


class AppEditSensor(UIBase):
    async def async_get(self):
        try:
            await api_core.ReqLimit.CheckMinuteRate("AppEditSensor", rg_lib.Cyclone.TryGetRealIp(self), 3)
            sid = self.get_cookie(rgv_consts.Cookies.TENANT)
            if sid:
                await api_core.Login.CheckRight(sid, (rgv_consts.UserNo.ROOT,))
                edit_mode = self.get_argument("edit_mode")
                if edit_mode == "edit":
                    uid = self.get_argument(u"sensorid")
                    self.render(rgv_consts.TPL_NAMES.APP_EDIT_SENSOR,
                                app_js_dir=settings.WEB['js_dir'],
                                app_css_dir=settings.WEB['css_dir'],
                                app_template_dir=settings.WEB['template_dir'],
                                title="Edit Sensor", sessionid=sid,
                                sensorid=uid, edit_mode=edit_mode)
                else:
                    self.render(rgv_consts.TPL_NAMES.APP_EDIT_SENSOR,
                                app_js_dir=settings.WEB['js_dir'],
                                app_css_dir=settings.WEB['css_dir'],
                                app_template_dir=settings.WEB['template_dir'],
                                title="Add Sensor", sessionid=sid,
                                sensorid=u"", edit_mode=edit_mode)
            else:
                self.finish(u"please login")
        except rg_lib.RGError as err:
            if models.ErrorTypes.TypeOfAccessOverLimit(err):
                self.finish(rgv_consts.WebContent.ACCESS_OVER_LIMIT)
            elif models.ErrorTypes.TypeOfSessionExpired(err):
                self.redirect(rgv_consts.URLs.APP_ADM_LOGIN)
            elif models.ErrorTypes.TypeOfNoRight(err):
                self.redirect(rgv_consts.URLs.APP_ADM_LOGIN)
            else:
                self.finish(rgv_consts.WebContent.SERVER_ERROR)


class AppSensorAdm(UIBase):
    def GetTitle(self):
        return "Sensor Adm powered by RoundGIS"

    async def async_get(self):
        try:
            await api_core.ReqLimit.CheckMinuteRate("AppSensorAdm", rg_lib.Cyclone.TryGetRealIp(self), 3)
            sid = self.get_cookie(rgv_consts.Cookies.TENANT)
            if sid:
                await api_core.Login.CheckRight(sid, (rgv_consts.UserNo.ROOT,))
                self.render(rgv_consts.TPL_NAMES.APP_ADM_SENSOR,
                            app_js_dir=settings.WEB['js_dir'],
                            app_css_dir=settings.WEB['css_dir'],
                            app_template_dir=settings.WEB['template_dir'],
                            title=self.GetTitle(), sessionid=sid,
                            edit_sensor_url=rgv_consts.URLs.APP_EDIT_SENSOR[1:],
                            measure_sensor_url=rgv_consts.URLs.APP_MEASURE_SENSOR[1:])
            else:
                self.redirect(rgv_consts.URLs.APP_ADM_LOGIN)
        except rg_lib.RGError as err:
            if models.ErrorTypes.TypeOfAccessOverLimit(err):
                self.finish(rgv_consts.WebContent.ACCESS_OVER_LIMIT)
            elif models.ErrorTypes.TypeOfSessionExpired(err):
                self.redirect(rgv_consts.URLs.APP_ADM_LOGIN)
            elif models.ErrorTypes.TypeOfNoRight(err):
                self.redirect(rgv_consts.URLs.APP_ADM_LOGIN)
            else:
                self.finish(rgv_consts.WebContent.SERVER_ERROR)


class AppEditSensorType(UIBase):
    def GetDataLenTbls(self):
        return [{"value": i, "label": str(i)} for i in range(1, 5)]

    def GetSensorNoTbls(self):
        return [{"value": rgv_consts.SensorNo.GENERAL, "label": "general"},
                {"value": rgv_consts.SensorNo.TEMPERATURE, "label": "temperature"},
                {"value": rgv_consts.SensorNo.HUMIDITY, "label": "humidity"},
                {"value": rgv_consts.SensorNo.ACC, "label": "acc"},
                {'value': rgv_consts.SensorNo.BATTERY, 'label': "battery"},
                {'value': rgv_consts.SensorNo.LIQUID_LEVEL, 'label': "liquid level"},
                {'value': rgv_consts.SensorNo.PH, 'label': "pH"},
                {'value': rgv_consts.SensorNo.EC, 'label': "EC"},
                {'value': rgv_consts.SensorNo.ILLUMINATION, 'label': 'illumination'},
                {'value': rgv_consts.SensorNo.GSM, 'label': 'gsm'},
                {'value': rgv_consts.SensorNo.SWITCHES, 'label': 'switches'}]

    async def async_get(self):
        try:
            await api_core.ReqLimit.CheckMinuteRate("AppEditSensorType", rg_lib.Cyclone.TryGetRealIp(self), 3)
            sid = self.get_cookie(rgv_consts.Cookies.TENANT)
            if sid:
                await api_core.Login.CheckRight(sid, (rgv_consts.UserNo.ROOT,))
                edit_mode = self.get_argument("edit_mode")
                if edit_mode == "edit":
                    uid = self.get_argument("typeid")
                    self.render(rgv_consts.TPL_NAMES.APP_EDIT_SENSOR_TYPE,
                                app_js_dir=settings.WEB['js_dir'],
                                app_css_dir=settings.WEB['css_dir'],
                                app_template_dir=settings.WEB['template_dir'],
                                title="Edit Sensor Type", sessionid=sid,
                                typeid=int(uid), edit_mode=edit_mode,
                                sensor_no_tbls=self.GetSensorNoTbls(),
                                data_len_tbls=self.GetDataLenTbls())
                else:
                    self.render(rgv_consts.TPL_NAMES.APP_EDIT_SENSOR_TYPE,
                                app_js_dir=settings.WEB['js_dir'],
                                app_css_dir=settings.WEB['css_dir'],
                                app_template_dir=settings.WEB['template_dir'],
                                title="Add Sensor Type", sessionid=sid,
                                typeid=0, edit_mode=edit_mode,
                                sensor_no_tbls=self.GetSensorNoTbls(),
                                data_len_tbls=self.GetDataLenTbls())
            else:
                self.finish("please login")
        except rg_lib.RGError as err:
            if models.ErrorTypes.TypeOfAccessOverLimit(err):
                self.finish(rgv_consts.WebContent.ACCESS_OVER_LIMIT)
            elif models.ErrorTypes.TypeOfSessionExpired(err):
                self.redirect(rgv_consts.URLs.APP_ADM_LOGIN)
            elif models.ErrorTypes.TypeOfNoRight(err):
                self.redirect(rgv_consts.URLs.APP_ADM_LOGIN)
            else:
                self.finish(rgv_consts.WebContent.SERVER_ERROR)


class AppSensorTypeAdm(UIBase):
    def GetTitle(self):
        return "Sensor Type Adm powered by RoundGIS Lab"

    async def async_get(self):
        try:
            await api_core.ReqLimit.CheckMinuteRate("AppSensorTypeAdm", rg_lib.Cyclone.TryGetRealIp(self), 3)
            sid = self.get_cookie(rgv_consts.Cookies.TENANT)
            if sid:
                await api_core.Login.CheckRight(sid, (rgv_consts.UserNo.ROOT,))
                self.render(rgv_consts.TPL_NAMES.APP_ADM_SENSOR_TYPE,
                            app_js_dir=settings.WEB['js_dir'],
                            app_css_dir=settings.WEB['css_dir'],
                            app_template_dir=settings.WEB['template_dir'],
                            title=self.GetTitle(), sessionid=sid,
                            edit_sensor_type_url=rgv_consts.URLs.APP_EDIT_SENSOR_TYPE[1:])
            else:
                self.redirect(rgv_consts.URLs.APP_ADM_LOGIN)
        except rg_lib.RGError as err:
            if models.ErrorTypes.TypeOfAccessOverLimit(err):
                self.finish(rgv_consts.WebContent.ACCESS_OVER_LIMIT)
            elif models.ErrorTypes.TypeOfSessionExpired(err):
                self.redirect(rgv_consts.URLs.APP_ADM_LOGIN)
            elif models.ErrorTypes.TypeOfNoRight(err):
                self.redirect(rgv_consts.URLs.APP_ADM_LOGIN)
            else:
                self.finish(rgv_consts.WebContent.SERVER_ERROR)


class AppAdmLogin(UIBase):
    def initialize(self, **kwargs):
        self.url_tbl = {"group": rgv_consts.URLs.APP_ADM_GROUP,
                        "user": rgv_consts.URLs.APP_ADM_USER,
                        "rggw": rgv_consts.URLs.APP_ADM_RGGW,
                        "switch": rgv_consts.URLs.APP_ADM_SWITCH,
                        "sensor": rgv_consts.URLs.APP_ADM_SENSOR,
                        'sensor_type': rgv_consts.URLs.APP_ADM_SENSOR_TYPE,
                        "command": rgv_consts.URLs.APP_ADM_SYS_COMMAND,
                        'eeprom': rgv_consts.URLs.APP_ADM_SYS_EEPROM,
                        'sys_cfg': rgv_consts.URLs.APP_SYS_CFG}

        self.adm_types = [{"name": "Group", "value": "group"},
                          {"name": "User", "value": "user", "checked": 1},
                          {"name": "RGGW", "value": "rggw"},
                          {"name": "Relay Switch", "value": "switch"},
                          {"name": "Sensor", "value": "sensor"},
                          {'name': "Sensor Type", "value": "sensor_type"},
                          {"name": "Command", "value": "command"},
                          {'name': "EEPROM", "value": "eeprom"},
                          {'name': 'Sys Config', 'value': 'sys_cfg'}]

    async def async_get(self):
        try:
            await api_core.ReqLimit.CheckMinuteRate("AppAdmLogin", rg_lib.Cyclone.TryGetRealIp(self), 5)
            user_lang = self.get_cookie(rgv_consts.Cookies.USERLANG, "eng")
            self.render(rgv_consts.TPL_NAMES.APP_ADM_LOGIN,
                        app_js_dir=settings.WEB['js_dir'],
                        app_template_dir=settings.WEB['template_dir'],
                        title="Adm Panel",
                        hint="", loginurl=rgv_consts.URLs.APP_ADM_LOGIN, bkgpng=settings.WEB['login_page_bkg'],
                        user_lang=user_lang, adm_types=self.adm_types)
        except rg_lib.RGError as err:
            if models.ErrorTypes.TypeOfAccessOverLimit(err):
                self.finish(rgv_consts.WebContent.ACCESS_OVER_LIMIT)
            else:
                self.finish(rgv_consts.WebContent.SERVER_ERROR)

    async def async_post(self):
        await api_core.ReqLimit.CheckMinuteRate("adm_login", rg_lib.Cyclone.TryGetRealIp(self), 5)
        userid = self.get_argument('userid', '').strip()
        pwd = self.get_argument('pwd', '').strip()
        adm_type = self.get_argument('adm_type', 'group')
        if userid and pwd:
            try:
                result = await api_core.Login.Adm(userid, pwd, rg_lib.Cyclone.TryGetRealIp(self))
                self.set_cookie(rgv_consts.Cookies.TENANT, result['sessionid'], expires=rg_lib.DateTime.ts2dt(result['expiry']), httponly=True)
                self.set_cookie(rgv_consts.Cookies.USERID, result['uid'], expires=rg_lib.DateTime.ts2dt(result['expiry']), httponly=True)
                if adm_type in self.url_tbl:
                    self.redirect(self.url_tbl[adm_type])
                else:
                    raise ValueError("adm type incorrect")
            except rg_lib.RGError as rge:
                if models.ErrorTypes.TypeOfNoUser(rge.message):
                    self.render(rgv_consts.TPL_NAMES.APP_ADM_LOGIN, title=u"Please Login", hint=u"invalid account",
                                loginurl=rgv_consts.URLs.APP_ADM_LOGIN, bkgpng=settings.WEB['login_page_bkg'],
                                adm_types=self.adm_types)
                elif models.ErrorTypes.TypeOfPwdErr(rge):
                    self.render(rgv_consts.TPL_NAMES.APP_ADM_LOGIN, title=u"Please Login", hint=u"password error",
                                loginurl=rgv_consts.URLs.APP_ADM_LOGIN, bkgpng=settings.WEB['login_page_bkg'],
                                adm_types=self.adm_types)
                elif models.ErrorTypes.TypeOfAccessOverLimit(rge):
                    self.finish(rgv_consts.WebContent.ACCESS_OVER_LIMIT)
                else:
                    self.render(rgv_consts.TPL_NAMES.APP_ADM_LOGIN, title=u"Please Login", hint=u"server error",
                                loginurl=rgv_consts.URLs.APP_ADM_LOGIN, bkgpng=settings.WEB['login_page_bkg'],
                                adm_types=self.adm_types)
            except Exception:
                log.err()
                self.render(rgv_consts.TPL_NAMES.APP_ADM_LOGIN, title="Please Login", hint="server error",
                            loginurl=rgv_consts.URLs.APP_ADM_LOGIN, bkgpng=settings.WEB['login_page_bkg'],
                            adm_types=self.adm_types)
        else:
            raise cyclone_web.HTTPError(403)


class AppLoginBase(UIBase):
    def RenderPage(self, hint_str):
        ulang = self.get_cookie(rgv_consts.Cookies.USERLANG, 'eng')
        app_opts = self.GetAppOptions()[ulang]
        self.render(rgv_consts.TPL_NAMES.APP_LOGIN,
                    app_js_dir=settings.WEB['js_dir'],
                    app_template_dir=settings.WEB['template_dir'],
                    title=self.GetTitle(),
                    hint=hint_str, loginurl=self.GetLoginUrl(), bkgpng=settings.WEB['login_page_bkg'],
                    user_lang=ulang, lang_options=self.GetLangOptions(), app_options=app_opts)

    def GetLangOptions(self):
        return [{"label": "ENG", "value": "eng"},
                {"label": "中文", "value": "zho"}]

    def GetAppOptions(self):
        raise NotImplementedError()

    def GetTitle(self):
        raise NotImplementedError()

    def GotoPage(self):
        raise NotImplementedError()

    def GetLoginUrl(self):
        raise NotImplementedError()

    async def async_get(self):
        try:
            await api_core.ReqLimit.CheckMinuteRate(self.GetLoginUrl(),
                                                    rg_lib.Cyclone.TryGetRealIp(self), 5)
            self.RenderPage("")
        except rg_lib.RGError as err:
            if models.ErrorTypes.TypeOfAccessOverLimit(err):
                self.finish(rgv_consts.WebContent.ACCESS_OVER_LIMIT)
            else:
                self.finish(rgv_consts.WebContent.SERVER_ERROR)

    async def async_post(self):
        await api_core.ReqLimit.CheckMinuteRate("AppLoginBase", rg_lib.Cyclone.TryGetRealIp(self), 5)
        userid = self.get_argument(u'userid', u'').strip()
        pwd = self.get_argument(u'pwd', u'').strip()
        ulang = self.get_argument(u'user_lang', u'eng')
        if userid and pwd:
            try:
                result = await api_core.Login.Tenant(userid, pwd, rg_lib.Cyclone.TryGetRealIp(self))
                self.set_cookie(rgv_consts.Cookies.TENANT, result['sessionid'], expires=rg_lib.DateTime.ts2dt(result['expiry']), httponly=True)
                self.set_cookie(rgv_consts.Cookies.USERID, result['uid'], expires=rg_lib.DateTime.ts2dt(result['expiry']),
                                httponly=True)
                self.set_cookie(rgv_consts.Cookies.USERLANG, ulang, httponly=True)
                self.GotoPage()
            except rg_lib.RGError as rge:
                if models.ErrorTypes.TypeOfNoUser(rge.message):
                    self.RenderPage(models.MultiText.getValue(multi_lang.invalid_account, ulang))
                elif models.ErrorTypes.TypeOfPwdErr(rge):
                    self.RenderPage(models.MultiText.getValue(multi_lang.password_error, ulang))
                elif models.ErrorTypes.TypeOfAccessOverLimit(rge):
                    self.finish(rgv_consts.WebContent.ACCESS_OVER_LIMIT)
                else:
                    self.RenderPage(models.MultiText.getValue(multi_lang.server_error, ulang))
            except Exception:
                log.err()
                self.RenderPage(models.MultiText.getValue(multi_lang.server_error, ulang))
        else:
            raise cyclone_web.HTTPError(403)


def GetGMAPAPIUrl(lang):
    return rgv_consts.Google.GMAP_API_CH if lang == "zho" else rgv_consts.Google.GMAP_API_EN


class AppAdmTrackerRawLog(UIBase):
    async def async_get(self):
        try:
            await api_core.ReqLimit.CheckMinuteRate("AppAdmTrackerRawLog", rg_lib.Cyclone.TryGetRealIp(self), 3)
            sid = self.get_cookie(rgv_consts.Cookies.TENANT)
            if sid:
                await api_core.Login.CheckRight(sid, (rgv_consts.UserNo.ROOT,))
                uid = self.get_argument("trackerid")
                self.render(rgv_consts.TPL_NAMES.APP_TRACKER_RAW_LOG,
                            app_js_dir=settings.WEB['js_dir'],
                            app_css_dir=settings.WEB['css_dir'],
                            app_template_dir=settings.WEB['template_dir'],
                            title="Tracker Raw Log", sessionid=sid,
                            trackerid=uid)
            else:
                self.redirect(rgv_consts.URLs.APP_ADM_LOGIN)
        except rg_lib.RGError as err:
            if models.ErrorTypes.TypeOfAccessOverLimit(err):
                self.finish(rgv_consts.WebContent.ACCESS_OVER_LIMIT)
            elif models.ErrorTypes.TypeOfSessionExpired(err):
                self.redirect(rgv_consts.URLs.APP_ADM_LOGIN)
            elif models.ErrorTypes.TypeOfNoRight(err):
                self.redirect(rgv_consts.URLs.APP_ADM_LOGIN)
            else:
                self.finish(rgv_consts.WebContent.SERVER_ERROR)


class EmLogin(AppLoginBase):
    def GetTitle(self):
        return "Easy Monitoring"

    def GetLoginUrl(self):
        return rgv_consts.URLs.APP_LOGIN

    def GetAppOptions(self):
        return {
            "eng": [{'label': "environment monitoring", "value": "em"}],

            "zho": [{'label': "环境监控", "value": "em"}],
        }

    def GotoPage(self):
        web_type = self.get_argument("web_type", "em")
        if web_type == "em":
            self.redirect(rgv_consts.URLs.APP_EM)
        else:
            raise cyclone_web.HTTPError(404)


class AppSensorMinsAvgLog(UIBase):
    def GetTitle(self):
        return "Sensor History Data Search by RoundGIS Lab"

    def GetMinsInterval(self):
        return [
            {"label": 1, 'value': 1},
            {"label": 2, "value": 2},
            {"label": 3, "value": 3},
            {"label": 5, "value": 5},
            {"label": 10, "value": 10},
            {"label": 20, "value": 20, "selected": True},
            {"label": 30, "value": 30}
        ]

    async def async_get(self):
        try:
            await api_core.ReqLimit.CheckMinuteRate("AppSensorMinsAvgLog", rg_lib.Cyclone.TryGetRealIp(self), 3)
            sid = self.get_cookie(rgv_consts.Cookies.TENANT)
            ulang = self.get_cookie(rgv_consts.Cookies.USERLANG, "eng")
            temp = self.get_cookie(rgv_consts.Cookies.SENSORID_FOR_LOG_VIEW, '')
            sensorids = c_escape.json_decode(c_escape.url_unescape(temp))
            if len(sensorids) < 1:
                raise cyclone_web.HTTPError(404, 'no sensor')
            if sid:
                await api_core.Login.HasTenant(sid)
                sensor_mdl = await api_core.Sensor.Get(["""select r1.*, r2.min_val,r2.max_val, r2.val_unit from
                                                               rgv_sensor r1,rgv_sensor_type r2 where r1.typeid=r2.id and r1.id=?""",
                                                        (sensorids[0],)])
                if sensor_mdl:
                    self.render(rgv_consts.TPL_NAMES.APP_SENSOR_MINS_AVG_LOG,
                                app_js_dir=settings.WEB['js_dir'],
                                app_css_dir=settings.WEB['css_dir'],
                                app_template_dir=settings.WEB['template_dir'],
                                title=self.GetTitle(),
                                sessionid=sid, user_lang=ulang,
                                sensorid=sensor_mdl['sensorid'],
                                sensor_name=sensor_mdl['name'],
                                min_val=rg_lib.Cyclone.ToTplVal(sensor_mdl['min_val']),
                                val_unit=(sensor_mdl['val_unit'] if sensor_mdl['val_unit'] else u""),
                                mins_interval_tbls=self.GetMinsInterval())
                else:
                    self.finish("no sensor")
            else:
                self.finish(rgv_consts.WebContent.PLEASE_LOGIN)
        except rg_lib.RGError as rge:
            if models.ErrorTypes.TypeOfSessionExpired(rge):
                self.redirect(rgv_consts.URLs.APP_LOGIN)
            elif models.ErrorTypes.TypeOfAccessOverLimit(rge):
                self.finish(rgv_consts.WebContent.ACCESS_OVER_LIMIT)
            else:
                self.finish(rgv_consts.WebContent.SERVER_ERROR)
        except Exception:
            log.err()
            self.finish(rgv_consts.WebContent.SERVER_ERROR)


class ViewSwitchSchedule(UIBase):
    def GetTitle(self):
        return "Switch Schedules View Powered by RoundGIS Lab"

    def GetLabel(self):
        return {
            "eng": {"remove": "remove", "refresh": "refresh"},
            "zho": {"remove": "删除", "refresh": "刷新"}
        }

    async def async_get(self):
        try:
            await api_core.ReqLimit.CheckMinuteRate("ViewSwitchSchedule", rg_lib.Cyclone.TryGetRealIp(self), 3)
            sid = self.get_cookie(rgv_consts.Cookies.TENANT)
            ulang = self.get_cookie(rgv_consts.Cookies.USERLANG, u"eng")
            if sid:
                await api_core.Login.HasTenant(sid)
                label_tbl = self.GetLabel()[ulang]
                self.render(rgv_consts.TPL_NAMES.VIEW_SWITCH_SCHEDULES,
                            app_js_dir=settings.WEB['js_dir'],
                            app_css_dir=settings.WEB['css_dir'],
                            app_template_dir=settings.WEB['template_dir'],
                            title=self.GetTitle(),
                            sessionid=sid, user_lang=ulang,
                            refresh_label=label_tbl['refresh'],
                            remove_label=label_tbl['remove'])
            else:
                self.redirect(rgv_consts.URLs.APP_LOGIN)
        except rg_lib.RGError as rge:
            if models.ErrorTypes.TypeOfSessionExpired(rge):
                self.redirect(rgv_consts.URLs.APP_LOGIN)
            elif models.ErrorTypes.TypeOfAccessOverLimit(rge):
                self.finish(rgv_consts.WebContent.ACCESS_OVER_LIMIT)
            else:
                self.finish(rgv_consts.WebContent.SERVER_ERROR)
        except Exception:
            self.finish(rgv_consts.WebContent.SERVER_ERROR)


class ViewQ06Log(UIBase):
    async def async_get(self):
        try:
            await api_core.ReqLimit.CheckMinuteRate("ViewQ06Log", rg_lib.Cyclone.TryGetRealIp(self), 5)
            sid = rg_lib.Cyclone.TryGetCookie(self, (rgv_consts.Cookies.TENANT, rgv_consts.Cookies.RGSYS))
            trackerid = self.get_argument('trackerid')
            if sid:
                await api_core.Login.CheckRight(sid, (rgv_consts.UserNo.ROOT,))
                mdl = await api_core.RGGW.Get(["select ownerid from rgv_rggw where ownerid=? limit 1", (trackerid,)])
                if mdl:
                    self.render(rgv_consts.TPL_NAMES.VIEW_Q06_LOG,
                                app_js_dir=settings.WEB['js_dir'],
                                app_template_dir=settings.WEB['template_dir'],
                                trackerid=trackerid, sessionid=sid, title=u"Q06 Log")
                else:
                    self.finish("no tracker")
            else:
                self.finish(rgv_consts.WebContent.PLEASE_LOGIN)
        except rg_lib.RGError as err:
            if models.ErrorTypes.TypeOfAccessOverLimit(err):
                self.finish(rgv_consts.WebContent.ACCESS_OVER_LIMIT)
            elif models.ErrorTypes.TypeOfSessionExpired(err):
                self.finish(rgv_consts.WebContent.PLEASE_LOGIN)
            elif models.ErrorTypes.TypeOfNoRight(err):
                self.finish(rgv_consts.WebContent.PLEASE_LOGIN)
            else:
                self.finish(rgv_consts.WebContent.SERVER_ERROR)


class ViewRecentHoursSensorData(UIBase):
    def GetLabel(self):
        return {
            "eng": {"remove": u"remove", "refresh": u"refresh"},
            "zho": {"remove": u"删除", "refresh": u"刷新"}
        }

    def GetHoursTbls(self):
        return [{'value': str(i), 'label': str(i)} for i in range(24, 0, -6)]

    async def async_get(self):
        try:
            await api_core.ReqLimit.CheckMinuteRate("ViewRecentHoursSensorData", rg_lib.Cyclone.TryGetRealIp(self), 5)
            sid = rg_lib.Cyclone.TryGetCookie(self, (rgv_consts.Cookies.TENANT,))
            ulang = self.get_cookie(rgv_consts.Cookies.USERLANG, u"eng")
            temp = self.get_cookie(rgv_consts.Cookies.SENSORID_FOR_LOG_VIEW, u'')
            sensorids = c_escape.json_decode(c_escape.url_unescape(temp))
            if len(sensorids) < 1:
                raise cyclone_web.HTTPError(404, 'no sensor')
            if sid:
                await api_core.Login.HasTenant(sid)
                label_tbl = self.GetLabel()[ulang]
                mdl = await api_core.Sensor.Get(["select id,name from rgv_sensor where id=?",
                                                 (sensorids[0],)])
                if mdl:
                    self.render(rgv_consts.TPL_NAMES.VIEW_RECENT_HOURS_SENSOR_DATA,
                                app_js_dir=settings.WEB['js_dir'],
                                app_template_dir=settings.WEB['template_dir'],
                                sensorid=sensorids[0], sessionid=sid, title=u"Recent Sensor Data",
                                sensor_name=mdl['name'],
                                hours_tbls=self.GetHoursTbls(),
                                user_lang=ulang,
                                refresh_btn_label=label_tbl['refresh'])
                else:
                    self.finish(u"no sensor")
            else:
                self.finish(rgv_consts.WebContent.PLEASE_LOGIN)
        except rg_lib.RGError as err:
            if models.ErrorTypes.TypeOfAccessOverLimit(err):
                self.finish(rgv_consts.WebContent.ACCESS_OVER_LIMIT)
            elif models.ErrorTypes.TypeOfSessionExpired(err):
                self.finish(rgv_consts.WebContent.PLEASE_LOGIN)
            elif models.ErrorTypes.TypeOfNoRight(err):
                self.finish(rgv_consts.WebContent.PLEASE_LOGIN)
            else:
                self.finish(rgv_consts.WebContent.SERVER_ERROR)


class ViewSensorMinsAvgTrend(UIBase):
    def GetTitle(self):
        return "Sensor Data Trend powered by RoundGIS Lab"

    def GetMinsInterval(self):
        return [
            {"label": 1, 'value': 1},
            {"label": 2, "value": 2},
            {"label": 3, "value": 3},
            {"label": 5, "value": 5},
            {"label": 10, "value": 10, 'selected': True},
            {"label": 20, "value": 20},
            {"label": 30, "value": 30}
        ]

    async def async_get(self):
        try:
            await api_core.ReqLimit.CheckMinuteRate("ViewSensorMinsAvgTrend", rg_lib.Cyclone.TryGetRealIp(self), 3)
            sid = self.get_cookie(rgv_consts.Cookies.TENANT)
            ulang = self.get_cookie(rgv_consts.Cookies.USERLANG, "eng")
            temp = self.get_cookie(rgv_consts.Cookies.SENSORID_FOR_LOG_VIEW)
            sensorids = c_escape.json_decode(c_escape.url_unescape(temp))
            if len(sensorids) < 1:
                raise cyclone_web.HTTPError(404, 'no sensor')
            if sid:
                await api_core.Login.HasTenant(sid)
                sql_str = rg_lib.Sqlite.GenInSql("""select COALESCE(name,'') name, id from rgv_sensor where id in """,
                                                 sensorids)
                sensors = await api_core.Sensor.Query([sql_str, sensorids])
                if len(sensors) > 0:
                    self.render(rgv_consts.TPL_NAMES.VIEW_SENSOR_MINS_AVG_TREND,
                                app_js_dir=settings.WEB['js_dir'],
                                app_css_dir=settings.WEB['css_dir'],
                                app_template_dir=settings.WEB['template_dir'],
                                title=self.GetTitle(),
                                sessionid=sid, user_lang=ulang,
                                sensorids=sensorids,
                                mins_interval_tbls=self.GetMinsInterval())
                else:
                    self.finish("no sensor")
            else:
                self.finish(rgv_consts.WebContent.PLEASE_LOGIN)
        except rg_lib.RGError as rge:
            if models.ErrorTypes.TypeOfSessionExpired(rge):
                self.redirect(rgv_consts.URLs.APP_LOGIN)
            elif models.ErrorTypes.TypeOfAccessOverLimit(rge):
                self.finish(rgv_consts.WebContent.ACCESS_OVER_LIMIT)
            else:
                self.finish(rgv_consts.WebContent.SERVER_ERROR)
        except Exception:
            log.err()
            self.finish(rgv_consts.WebContent.SERVER_ERROR)


class ViewSensorMinsAvgData(UIBase):
    def GetTitle(self):
        return "Sensor Data Log powered by RoundGIS Lab"

    def GetMinsInterval(self):
        return [
            {"label": 1, 'value': 1},
            {"label": 2, "value": 2},
            {"label": 3, "value": 3},
            {"label": 5, "value": 5},
            {"label": 10, "value": 10},
            {"label": 20, "value": 20, "selected": True},
            {"label": 30, "value": 30}
        ]

    async def async_get(self):
        try:
            await api_core.ReqLimit.CheckMinuteRate("ViewSensorMinsAvgData", rg_lib.Cyclone.TryGetRealIp(self), 3)
            sid = self.get_cookie(rgv_consts.Cookies.TENANT)
            ulang = self.get_cookie(rgv_consts.Cookies.USERLANG, u"eng")
            temp = self.get_cookie(rgv_consts.Cookies.SENSORID_FOR_LOG_VIEW)
            sensorids = c_escape.json_decode(c_escape.url_unescape(temp))
            if len(sensorids) < 1:
                raise cyclone_web.HTTPError(404, 'no sensor')
            if sid:
                await api_core.Login.HasTenant(sid)
                sql_str = rg_lib.Sqlite.GenInSql("""select COALESCE(name,'') name, id
                                                    from rgv_sensor where id in """,
                                                 sensorids)
                sensors = await api_core.Sensor.Query([sql_str, sensorids])
                sensors_tbl = {i['id']: i for i in sensors}
                if len(sensors) > 0:
                    self.render(rgv_consts.TPL_NAMES.VIEW_SENSOR_MINS_AVG_DATA,
                                app_js_dir=settings.WEB['js_dir'],
                                app_css_dir=settings.WEB['css_dir'],
                                app_template_dir=settings.WEB['template_dir'],
                                title=self.GetTitle(),
                                sessionid=sid, user_lang=ulang,
                                sensorids=sensorids,
                                sensors_tbl=sensors_tbl,
                                mins_interval_tbls=self.GetMinsInterval())
                else:
                    self.finish("no sensor")
            else:
                self.finish(rgv_consts.WebContent.PLEASE_LOGIN)
        except rg_lib.RGError as rge:
            if models.ErrorTypes.TypeOfSessionExpired(rge):
                self.redirect(rgv_consts.URLs.APP_LOGIN)
            elif models.ErrorTypes.TypeOfAccessOverLimit(rge):
                self.finish(rgv_consts.WebContent.ACCESS_OVER_LIMIT)
            else:
                self.finish(rgv_consts.WebContent.SERVER_ERROR)
        except Exception:
            log.err()
            self.finish(rgv_consts.WebContent.SERVER_ERROR)


class ViewSensorTrend(UIBase):
    def GetTitle(self):
        return "Sensor Trend powered by RoundGIS Lab"

    async def async_get(self):
        try:
            await api_core.ReqLimit.CheckMinuteRate("ViewSensorTrend", rg_lib.Cyclone.TryGetRealIp(self), 3)
            sid = self.get_cookie(rgv_consts.Cookies.TENANT)
            ulang = self.get_cookie(rgv_consts.Cookies.USERLANG, "eng")
            temp = self.get_cookie(rgv_consts.Cookies.SENSORID_FOR_LOG_VIEW)
            sensorids = c_escape.json_decode(c_escape.url_unescape(temp))
            if len(sensorids) < 1:
                raise cyclone_web.HTTPError(404, 'no sensor')
            if sid:
                await api_core.Login.HasTenant(sid)
                sql_str = rg_lib.Sqlite.GenInSql("""select COALESCE(name,'') name, id from rgv_sensor where id in """,
                                                 sensorids)
                sensors = await api_core.Sensor.Query([sql_str, sensorids])
                if len(sensors) > 0:
                    self.render(rgv_consts.TPL_NAMES.VIEW_SENSOR_TREND,
                                app_js_dir=settings.WEB['js_dir'],
                                app_css_dir=settings.WEB['css_dir'],
                                app_template_dir=settings.WEB['template_dir'],
                                title=self.GetTitle(),
                                sessionid=sid, user_lang=ulang,
                                sensorids=sensorids)
                else:
                    self.finish("no sensor")
            else:
                self.finish(rgv_consts.WebContent.PLEASE_LOGIN)
        except rg_lib.RGError as rge:
            if models.ErrorTypes.TypeOfSessionExpired(rge):
                self.redirect(rgv_consts.URLs.APP_LOGIN)
            elif models.ErrorTypes.TypeOfAccessOverLimit(rge):
                self.finish(rgv_consts.WebContent.ACCESS_OVER_LIMIT)
            else:
                self.finish(rgv_consts.WebContent.SERVER_ERROR)
        except Exception:
            log.err()
            self.finish(rgv_consts.WebContent.SERVER_ERROR)


class AppEm(UIBase):
    def GetTitle(self):
        return "Easy Monitoring powered by RoundGIS Lab"

    def GetLabel(self):
        return {
            "eng": {"open": u"turn on", "close": "turn off", "open_duration_desc": "15-9999 seconds",
                     'switch_mode': "switch mode", 'set_schedule': "set schedule",
                     'switch_schedule_view': "view schedule",
                     'set_cond_action_view': 'set action condition',
                     'cameras_view': 'cameras'},
            "zho": {"open": "打开", "close": "关闭", "open_duration_desc": "15-9999秒",
                     "switch_mode": u"切换模式", 'set_schedule': u"设置排程",
                     'switch_schedule_view': u"查看排程",
                     'set_cond_action_view': u'设置条件触发',
                     'cameras_view': u'摄像头'}
        }

    def GetMinsInterval(self):
        return [
            {"label": 1, 'value': 1},
            {"label": 2, "value": 2},
            {"label": 3, "value": 3},
            {"label": 5, "value": 5, 'selected': True},
            {"label": 10, "value": 10},
            {"label": 20, "value": 20},
            {"label": 30, "value": 30}
        ]

    def GetHoursTbls(self):
        return [
            {"label": 1, 'value': 1},
            {"label": 3, "value": 3},
            {"label": 6, "value": 6, 'selected': True},
            {"label": 12, "value": 12},
            {"label": 18, "value": 18},
            {"label": 24, "value": 24}
        ]

    async def async_get(self):
        try:
            await api_core.ReqLimit.CheckMinuteRate("AppEm", rg_lib.Cyclone.TryGetRealIp(self), 3)
            sid = self.get_cookie(rgv_consts.Cookies.TENANT)
            ulang = self.get_cookie(rgv_consts.Cookies.USERLANG, "eng")
            if sid:
                await api_core.Login.HasTenant(sid)
                label_tbl = self.GetLabel()[ulang]
                self.render(rgv_consts.TPL_NAMES.APP_EM,
                            app_js_dir=settings.WEB['js_dir'],
                            app_css_dir=settings.WEB['css_dir'],
                            app_template_dir=settings.WEB['template_dir'],
                            title=self.GetTitle(),
                            sessionid=sid, user_lang=ulang, open_valve_label=label_tbl['open'],
                            close_valve_label=label_tbl['close'],
                            open_duration_label=label_tbl['open_duration_desc'],
                            switch_mode_label=label_tbl['switch_mode'],
                            sensor_mins_avg_log_url=rgv_consts.URLs.APP_SENSOR_MINS_AVG_LOG[1:],
                            switch_schedule_view_url=rgv_consts.URLs.VIEW_SWITCH_SCHEDULES[1:],
                            switch_schedule_view_label=label_tbl['switch_schedule_view'],
                            set_schedule_label=label_tbl['set_schedule'],
                            set_sensor_trigger_view_url=rgv_consts.URLs.APP_ADM_SENSOR_TRIGGER[1:],
                            set_sensor_trigger_view_url_label=label_tbl['set_cond_action_view'],
                            cameras_view_label=label_tbl['cameras_view'],
                            sensor_mins_avg_trend_url=rgv_consts.URLs.VIEW_SENSOR_MINS_AVG_TREND[1:],
                            sensor_mins_avg_data_url=rgv_consts.URLs.VIEW_SENSOR_MINS_AVG_DATA[1:],
                            sensor_recent_hours_plotting_url=rgv_consts.URLs.VIEW_RECENT_HOURS_SENSOR_DATA_PLOTTING[1:],
                            sensor_trend_url=rgv_consts.URLs.VIEW_SENSOR_TREND[1:],
                            cameras_view_url=rgv_consts.URLs.VIEW_CAMERAS[1:],
                            sensorid_for_log_view=rgv_consts.Cookies.SENSORID_FOR_LOG_VIEW,
                            hours_tbls=self.GetHoursTbls(),
                            mins_interval_tbls=self.GetMinsInterval())
            else:
                self.redirect(rgv_consts.URLs.APP_LOGIN)
        except rg_lib.RGError as rge:
            if models.ErrorTypes.TypeOfSessionExpired(rge):
                self.redirect(rgv_consts.URLs.APP_LOGIN)
            elif models.ErrorTypes.TypeOfAccessOverLimit(rge):
                self.finish(rgv_consts.WebContent.ACCESS_OVER_LIMIT)
            else:
                self.finish(rgv_consts.WebContent.SERVER_ERROR)
        except Exception:
            self.finish(rgv_consts.WebContent.SERVER_ERROR)


class AppAdmSysEEPROM(UIBase):
    async def async_get(self):
        try:
            await api_core.ReqLimit.CheckMinuteRate("AppAdmSysEEPROM", rg_lib.Cyclone.TryGetRealIp(self), 3)
            sid = self.get_cookie(rgv_consts.Cookies.TENANT)
            uid = self.get_cookie(rgv_consts.Cookies.USERID)
            if sid:
                await api_core.Login.CheckRight(sid, (rgv_consts.UserNo.ROOT,))
                self.render(rgv_consts.TPL_NAMES.APP_ADM_SYS_EEPROM,
                            app_js_dir=settings.WEB['js_dir'],
                            app_css_dir=settings.WEB['css_dir'],
                            app_template_dir=settings.WEB['template_dir'],
                            title="Config EEPROM",
                            sessionid=sid, userid=uid)
            else:
                self.redirect(rgv_consts.URLs.APP_ADM_LOGIN)
        except rg_lib.RGError as rgerr:
            if models.ErrorTypes.TypeOfAccessOverLimit(rgerr):
                self.finish(rgv_consts.WebContent.ACCESS_OVER_LIMIT)
            elif models.ErrorTypes.TypeOfNoRight(rgerr):
                self.redirect(rgv_consts.URLs.APP_ADM_LOGIN)
            elif models.ErrorTypes.TypeOfSessionExpired(rgerr):
                self.redirect(rgv_consts.URLs.APP_ADM_LOGIN)
            else:
                self.finish(rgv_consts.WebContent.SERVER_ERROR)


class AppMeasureSensor(UIBase):
    async def async_get(self):
        try:
            await api_core.ReqLimit.CheckMinuteRate("AppMeasureSensor", rg_lib.Cyclone.TryGetRealIp(self), 3)
            sid = self.get_cookie(rgv_consts.Cookies.TENANT)
            uid = self.get_cookie(rgv_consts.Cookies.USERID)
            sensorid = self.get_argument('a')
            if sid:
                await api_core.Login.CheckRight(sid, (rgv_consts.UserNo.ROOT,))
                self.render(rgv_consts.TPL_NAMES.APP_MEASURE_SENSOR,
                            app_js_dir=settings.WEB['js_dir'],
                            app_css_dir=settings.WEB['css_dir'],
                            app_template_dir=settings.WEB['template_dir'],
                            title="Measuring Sensor",
                            sessionid=sid, userid=uid, sensorid=sensorid)
            else:
                self.redirect(rgv_consts.URLs.APP_ADM_LOGIN)
        except rg_lib.RGError as rgerr:
            if models.ErrorTypes.TypeOfAccessOverLimit(rgerr):
                self.finish(rgv_consts.WebContent.ACCESS_OVER_LIMIT)
            elif models.ErrorTypes.TypeOfNoRight(rgerr):
                self.redirect(rgv_consts.URLs.APP_ADM_LOGIN)
            elif models.ErrorTypes.TypeOfSessionExpired(rgerr):
                self.redirect(rgv_consts.URLs.APP_ADM_LOGIN)
            else:
                self.finish(rgv_consts.WebContent.SERVER_ERROR)


class AppEditSensorTrigger(UIBase):
    def GetLabelTbl(self):
        return {
            "eng": {"sensor": "sensor", "switch": "switch",
                    'start_time': 'start', 'stop_time': 'stop',
                    'add_btn': 'add',
                    'remove_btn': 'remove',
                    'save_btn': 'save',
                    'check_interval': 'check interval(minute)',
                    'name': 'name'},
            "zho": {"sensor": "传感器", "switch": "阀门(开关)",
                    'start_time': '开始', 'stop_time': '结束',
                    'add_btn': '增加',
                    'remove_btn': '移除',
                    'save_btn': '保存',
                    'check_interval': '探测范围(分钟)',
                    'name': '名字'}
        }

    def GetCheckIntervalTbls(self):
        return [{'value': i, 'label': str(i)} for i in (0, 1, 3, 10, 30, 60, 90, 120, 150, 180)]

    async def GetSensorTbls(self, uid):
        sql_str = """select r1.id id, (COALESCE(r2.name||'-','')||r1.name) sensor_name
                     from rgv_sensor r1,
                          rgv_rggw r2,
                          rgv_user_group r3, 
                          rgv_group r4,
                          rgv_sensor_type r5
                     where r1.typeid=r5.id and r1.ownerid=r2.id and r2.groupid=r3.groupid
                           and r3.groupid=r4.id and r3.uid=? and r5.sensor_no<>? limit ?"""
        sql_args = (uid, rgv_consts.SensorNo.SWITCHES, rgv_consts.DbConsts.SEARCH_LIMIT)
        rows = await api_core.Sensor.Query([sql_str, sql_args])
        return [{'value': r['id'], 'label': r['sensor_name']} for r in rows]

    async def GetSwitchTbls(self, uid):
        sql_str = """select r1.id, 
                            (COALESCE(r2.name||'-','')||r1.name) switch_name
                     from rgv_switch r1,
                          rgv_rggw r2,
                          rgv_user_group r3, 
                          rgv_group r4
                    where r1.ownerid=r2.id and r2.groupid=r3.groupid
                    and r3.groupid=r4.id and r3.uid=? limit ?"""
        sql_args = (uid, rgv_consts.DbConsts.SEARCH_LIMIT)
        rows = await api_core.BizDB.Query([sql_str, sql_args])
        return [{'value': r['id'], 'label': r['switch_name']} for r in rows]

    async def async_get(self):
        try:
            await api_core.ReqLimit.CheckMinuteRate("AppEditSwitchActionTrigger", rg_lib.Cyclone.TryGetRealIp(self), 3)
            sid = GetToken(self)
            ulang = self.get_cookie(rgv_consts.Cookies.USERLANG, "eng")
            trigid = self.get_argument('triggerid', "0")
            if sid:
                user = await api_core.Login.HasTenant(sid)
                sensor_tbls = await self.GetSensorTbls(user['id'])
                switch_tbls = await self.GetSwitchTbls(user['id'])
                label_tbl = self.GetLabelTbl()[ulang]
                self.render(rgv_consts.TPL_NAMES.APP_EDIT_SENSOR_TRIGGER,
                            app_js_dir=settings.WEB['js_dir'],
                            app_css_dir=settings.WEB['css_dir'],
                            app_template_dir=settings.WEB['template_dir'],
                            user_lang=ulang,
                            title="Set Action Trigger", sessionid=sid,
                            sensor_tbls=sensor_tbls,
                            switch_tbls=switch_tbls,
                            check_interval_tbls=self.GetCheckIntervalTbls(),
                            sensor_label=label_tbl['sensor'],
                            switch_label=label_tbl['switch'],
                            check_interval_label=label_tbl['check_interval'],
                            start_time_label=label_tbl['start_time'],
                            stop_time_label=label_tbl['stop_time'],
                            name_label=label_tbl['name'],
                            add_btn=label_tbl['add_btn'],
                            remove_btn=label_tbl['remove_btn'],
                            save_btn=label_tbl['save_btn'],
                            triggerid=trigid)
            else:
                self.finish("please login")
        except rg_lib.RGError as err:
            if models.ErrorTypes.TypeOfAccessOverLimit(err):
                self.finish(rgv_consts.WebContent.ACCESS_OVER_LIMIT)
            elif models.ErrorTypes.TypeOfNoRight(err):
                self.redirect(rgv_consts.URLs.APP_ADM_LOGIN)
            else:
                self.finish(rgv_consts.WebContent.SERVER_ERROR)
        except cyclone_web.HTTPError:
            raise


class AppAdmSensorTrigger(UIBase):
    def GetTitle(self):
        return "Sensor Trigger Adm"

    def GetLabel(self):
        return {
            "eng": {"remove": "remove", "refresh": "refresh", 'add': 'add/edit'},
            "zho": {"remove": "删除", "refresh": "刷新", 'add': "新增/编辑"}
        }

    async def async_get(self):
        try:
            await api_core.ReqLimit.CheckMinuteRate("AppAdmSwitchActionTrigger", rg_lib.Cyclone.TryGetRealIp(self), 3)
            sid = GetToken(self)
            ulang = self.get_cookie(rgv_consts.Cookies.USERLANG, "eng")
            label_tbl = self.GetLabel()
            if sid:
                await api_core.Login.HasTenant(sid)
                self.render(rgv_consts.TPL_NAMES.APP_ADM_SENSOR_TRIGGER,
                            app_js_dir=settings.WEB['js_dir'],
                            app_css_dir=settings.WEB['css_dir'],
                            app_template_dir=settings.WEB['template_dir'],
                            title=self.GetTitle(), sessionid=sid,
                            user_lang=ulang,
                            refresh_label=label_tbl[ulang]['refresh'],
                            add_label=label_tbl[ulang]['add'],
                            remove_label=label_tbl[ulang]['remove'],
                            edit_action_url=rgv_consts.URLs.APP_EDIT_SENSOR_TRIGGER[1:],
                            examples_url="https://github.com/ygl-rg/greenhouse-open-api/wiki/How-to-set-notice-condition")
            else:
                login_url = rgv_consts.URLs.APP_LOGIN
                self.redirect(login_url)
        except rg_lib.RGError as err:
            if models.ErrorTypes.TypeOfAccessOverLimit(err):
                self.finish(rgv_consts.WebContent.ACCESS_OVER_LIMIT)
            elif models.ErrorTypes.TypeOfNoRight(err):
                self.redirect(rgv_consts.URLs.APP_LOGIN)
            else:
                self.finish(rgv_consts.WebContent.SERVER_ERROR)
        except cyclone_web.HTTPError:
            raise


class ViewCameras(UIBase):
    def GetTitle(self):
        return "Camera List"

    def GetLabel(self):
        return {
            "eng": {"goto": "Go to", "search": "Search", "add": "Add", "remove": "Remove"},
            "zho": {"goto": "前往", "search": "查找", "add": "新增", "remove": "删除"}
        }

    async def async_get(self):
        try:
            await api_core.ReqLimit.CheckMinuteRate("ViewNodes", rg_lib.Cyclone.TryGetRealIp(self), 3)
            sid = self.get_cookie(rgv_consts.Cookies.TENANT)
            ulang = self.get_cookie(rgv_consts.Cookies.USERLANG, u"eng")
            await api_core.Login.HasTenant(sid)
            label_tbl = self.GetLabel()[ulang]
            self.render(rgv_consts.TPL_NAMES.VIEW_CAMERAS,
                        app_js_dir=settings.WEB['js_dir'],
                        app_css_dir=settings.WEB['css_dir'],
                        app_template_dir=settings.WEB['template_dir'],
                        title=self.GetTitle(),
                        sessionid=sid,
                        user_lang=ulang,
                        goto_label=label_tbl['goto'],
                        search_label=label_tbl['search'],
                        add_label=label_tbl['add'],
                        remove_label=label_tbl['remove'],
                        view_edit_camera_url=rgv_consts.URLs.VIEW_EDIT_CAMERA[1:])
        except rg_lib.RGError as rge:
            if models.ErrorTypes.TypeOfSessionExpired(rge):
                self.redirect(rgv_consts.URLs.APP_LOGIN)
            elif models.ErrorTypes.TypeOfAccessOverLimit(rge):
                self.finish(rgv_consts.WebContent.ACCESS_OVER_LIMIT)
            else:
                self.finish(rgv_consts.WebContent.SERVER_ERROR)
        except Exception:
            self.finish(rgv_consts.WebContent.SERVER_ERROR)


class ViewEditCamera(UIBase):
    def GetTitle(self):
        return "Add Camera"

    def GetLabel(self):
        return {
            "eng": {"goto": "Go to"},
            "zho": {"goto": "前往"}
        }

    async def async_get(self):
        try:
            await api_core.ReqLimit.CheckMinuteRate("ViewNodes", rg_lib.Cyclone.TryGetRealIp(self), 3)
            sid = self.get_cookie(rgv_consts.Cookies.TENANT)
            ulang = self.get_cookie(rgv_consts.Cookies.USERLANG, "eng")
            await api_core.Login.HasTenant(sid)
            label_tbl = self.GetLabel()[ulang]
            self.render(rgv_consts.TPL_NAMES.VIEW_EDIT_CAMERA,
                        app_js_dir=settings.WEB['js_dir'],
                        app_css_dir=settings.WEB['css_dir'],
                        app_template_dir=settings.WEB['template_dir'],
                        title=self.GetTitle(),
                        sessionid=sid,
                        user_lang=ulang)
        except rg_lib.RGError as rge:
            if models.ErrorTypes.TypeOfSessionExpired(rge):
                self.redirect(rgv_consts.URLs.APP_LOGIN)
            elif models.ErrorTypes.TypeOfAccessOverLimit(rge):
                self.finish(rgv_consts.WebContent.ACCESS_OVER_LIMIT)
            else:
                self.finish(rgv_consts.WebContent.SERVER_ERROR)
        except Exception:
            self.finish(rgv_consts.WebContent.SERVER_ERROR)


class AppSysCfg(UIBase):
    def GetTimezoneOpts(self):
        import pytz
        asia_tzs = ['UTC']+[i for i in pytz.common_timezones if i.find('Asia') >= 0]
        return [{'label': i, 'value': i} for i in asia_tzs]

    async def async_get(self):
        try:
            await api_core.ReqLimit.CheckMinuteRate("AppSysCfg", rg_lib.Cyclone.TryGetRealIp(self), 3)
            sid = self.get_cookie(rgv_consts.Cookies.TENANT)
            if sid:
                await api_core.Login.CheckRight(sid, (rgv_consts.UserNo.ROOT,))
                self.render(rgv_consts.TPL_NAMES.APP_SYS_CFG,
                            app_js_dir=settings.WEB['js_dir'],
                            app_css_dir=settings.WEB['css_dir'],
                            app_template_dir=settings.WEB['template_dir'],
                            tz_options=self.GetTimezoneOpts(),
                            title="Sys Config", sessionid=sid)
            else:
                self.redirect(rgv_consts.URLs.APP_ADM_LOGIN)
        except rg_lib.RGError as err:
            if models.ErrorTypes.TypeOfAccessOverLimit(err):
                self.finish(rgv_consts.WebContent.ACCESS_OVER_LIMIT)
            elif models.ErrorTypes.TypeOfNoRight(err):
                self.redirect(rgv_consts.URLs.APP_ADM_LOGIN)
            else:
                self.finish(rgv_consts.WebContent.SERVER_ERROR)


class Logout(UIBase):
    async def __logout(self):
        sid = self.get_cookie(rgv_consts.Cookies.TENANT)
        if sid:
            await api_core.UserSession.Remove(sid)
        self.clear_cookie(rgv_consts.Cookies.TENANT)
        self.clear_cookie(rgv_consts.Cookies.USERID)
        self.finish("<h2>you are now logged out</h2>")

    async def async_get(self):
        try:
            await api_core.ReqLimit.CheckMinuteRate("logout", rg_lib.Cyclone.TryGetRealIp(self), 3)
            await self.__logout()
        except rg_lib.RGError as err_obj:
            if models.ErrorTypes.TypeOfAccessOverLimit(err_obj):
                self.finish(rgv_consts.WebContent.ACCESS_OVER_LIMIT)

    async def async_post(self):
        try:
            await api_core.ReqLimit.CheckMinuteRate("logout", rg_lib.Cyclone.TryGetRealIp(self), 3)
            await self.__logout()
        except rg_lib.RGError as err_obj:
            if models.ErrorTypes.TypeOfAccessOverLimit(err_obj):
                self.finish(rgv_consts.WebContent.ACCESS_OVER_LIMIT)
