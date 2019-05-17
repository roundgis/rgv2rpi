import os.path as os_path
import cyclone.web as cyclone_web
import http_handlers.static_tpl as static_tpl_handlers
import http_handlers.ui as ui_handlers
import http_handlers.internal_api as api_handlers
import http_handlers.plotting as plotting_handlers
import rgv_consts
import rg_lib
import settings


def GetStaticHandlers(static_path, export_path):
    return [(rg_lib.Cyclone.Dir2Url('v/imgs'), rg_lib.TempFileHandler, {"path": os_path.join(static_path, 'imgs')}),
            (rg_lib.Cyclone.Dir2Url('v/jslib'), rg_lib.TempFileHandler, {"path": os_path.join(static_path, 'jslib')}),
            (rg_lib.Cyclone.Dir2Url('v/js'), rg_lib.TempFileHandler, {"path": os_path.join(static_path, 'js')}),
            (rg_lib.Cyclone.Dir2Url('v/css'), rg_lib.TempFileHandler, {"path": os_path.join(static_path, 'css')}),
            (rg_lib.Cyclone.Dir2Url('v/export'), rg_lib.ExcelFileHandler, {"path": export_path})]


def GetStaticTplHandlers():
    return [
        (rg_lib.Cyclone.Dir2Url(settings.WEB['js_dir']), static_tpl_handlers.JsHandler),
        (rg_lib.Cyclone.Dir2Url(settings.WEB['css_dir']), static_tpl_handlers.CssHandler),
        (rg_lib.Cyclone.Dir2Url(settings.WEB['template_dir']), static_tpl_handlers.DojoTplHandler)
    ]


def GetBasicApi():
    return [(rgv_consts.URLs.API_GROUP_ADM, api_handlers.GroupAdm),
            (rgv_consts.URLs.API_USER_ADM, api_handlers.UserAdm),
            (rgv_consts.URLs.API_RGGW_ADM, api_handlers.RGGWAdm),
            (rgv_consts.URLs.API_SWITCH_ADM, api_handlers.SwitchAdm),
            (rgv_consts.URLs.API_SENSOR_ADM, api_handlers.SensorAdm),
            (rgv_consts.URLs.API_BASIC_USER, api_handlers.BasicUser),
            (rgv_consts.URLs.API_SENSOR_TYPE_ADM, api_handlers.SensorTypeAdm),
            (rgv_consts.URLs.API_CAMERA, api_handlers.CameraAdm),
            (rgv_consts.URLs.API_SYS_CFG, api_handlers.SysCfg),
            (rgv_consts.URLs.API_SENSOR_TRIGGER, api_handlers.SensorTriggerAdm)
            ]


def GetProApi():
    return [
        (rgv_consts.URLs.API_EM, api_handlers.EM)
    ]


def GetBasicAPP():
    return [
        (rgv_consts.URLs.APP_ADM_LOGIN, ui_handlers.AppAdmLogin),
        (rgv_consts.URLs.APP_LOGOUT, ui_handlers.Logout),
        (rgv_consts.URLs.APP_ADM_GROUP, ui_handlers.AppGroupAdm),
        (rgv_consts.URLs.APP_EDIT_GROUP, ui_handlers.AppEditGroup),
        (rgv_consts.URLs.APP_ADM_USER, ui_handlers.AppUserAdm),
        (rgv_consts.URLs.APP_EDIT_USER, ui_handlers.AppEditUser),
        (rgv_consts.URLs.APP_ADM_SYS_COMMAND, ui_handlers.AppAdmSysCommand),
        (rgv_consts.URLs.APP_ADM_SYS_EEPROM, ui_handlers.AppAdmSysEEPROM),
        (rgv_consts.URLs.APP_TRACKER_RAW_LOG, ui_handlers.AppAdmTrackerRawLog),
        (rgv_consts.URLs.APP_EDIT_RGGW, ui_handlers.AppEditRGGW),
        (rgv_consts.URLs.APP_ADM_RGGW, ui_handlers.AppAdmRGGW),
        (rgv_consts.URLs.APP_EDIT_SWITCH, ui_handlers.AppEditSwitch),
        (rgv_consts.URLs.APP_ADM_SWITCH, ui_handlers.AppSwitchAdm),
        (rgv_consts.URLs.APP_EDIT_SENSOR, ui_handlers.AppEditSensor),
        (rgv_consts.URLs.APP_ADM_SENSOR, ui_handlers.AppSensorAdm),
        (rgv_consts.URLs.APP_EDIT_SENSOR_TYPE, ui_handlers.AppEditSensorType),
        (rgv_consts.URLs.APP_ADM_SENSOR_TYPE, ui_handlers.AppSensorTypeAdm),
        (rgv_consts.URLs.APP_MEASURE_SENSOR, ui_handlers.AppMeasureSensor),
        (rgv_consts.URLs.APP_SYS_CFG, ui_handlers.AppSysCfg),
        (rgv_consts.URLs.APP_EDIT_SENSOR_TRIGGER, ui_handlers.AppEditSensorTrigger),
        (rgv_consts.URLs.APP_ADM_SENSOR_TRIGGER, ui_handlers.AppAdmSensorTrigger)
    ]


def GetProApp():
    return [
        (rgv_consts.URLs.INDEX, ui_handlers.Index),
        (rgv_consts.URLs.APP_LOGIN, ui_handlers.EmLogin),
        (rgv_consts.URLs.APP_SENSOR_MINS_AVG_LOG, ui_handlers.AppSensorMinsAvgLog),
        (rgv_consts.URLs.APP_EM, ui_handlers.AppEm)
    ]


def GetReportHandlers():
    return [
    ]


def GetViewHandlers():
    return [
        (rgv_consts.URLs.VIEW_SWITCH_SCHEDULES, ui_handlers.ViewSwitchSchedule),
        (rgv_consts.URLs.VIEW_Q06_LOG, ui_handlers.ViewQ06Log),
        (rgv_consts.URLs.VIEW_RECENT_HOURS_SENSOR_DATA, ui_handlers.ViewRecentHoursSensorData),
        (rgv_consts.URLs.VIEW_SENSOR_MINS_AVG_TREND, ui_handlers.ViewSensorMinsAvgTrend),
        (rgv_consts.URLs.VIEW_SENSOR_MINS_AVG_DATA, ui_handlers.ViewSensorMinsAvgData),
        (rgv_consts.URLs.VIEW_RECENT_HOURS_SENSOR_DATA_PLOTTING, plotting_handlers.SensorHourlyLogHandler),
        (rgv_consts.URLs.VIEW_CAMERAS, ui_handlers.ViewCameras),
        (rgv_consts.URLs.VIEW_EDIT_CAMERA, ui_handlers.ViewEditCamera),
        (rgv_consts.URLs.VIEW_SENSOR_TREND, ui_handlers.ViewSensorTrend)
    ]


class App(cyclone_web.Application):
    def __init__(self, static_path, export_path):
        handlers = GetStaticHandlers(static_path, export_path) + GetBasicApi() + GetProApi() + GetProApp() + \
                   GetBasicAPP()+GetReportHandlers()+GetViewHandlers() + GetStaticTplHandlers()
        cyclone_web.Application.__init__(self, handlers, gzip=True,
                                         template_path=os_path.join(settings.WEB['static_path'],
                                                                    settings.WEB['tpl_dir']))
