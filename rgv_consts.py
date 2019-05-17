# -*- coding: utf-8 -*-


class Timeout:
    COOKIE_INTERVAL = 3600*24*32
    ONLINE_TIMEOUT = 119


class GWProtocolIds:
    ECHO = "echo"
    RGGW = 'rggw'
    IDS = (ECHO, RGGW)


class DbConsts:
    SEARCH_LIMIT = 768


class Cookies:
    TENANT = "nbgis1_"
    RGSYS = "nbgis0_"
    USERID = "nbgisu_"
    USERLANG = "nbgislang_"
    SENSORID_FOR_LOG_VIEW = "sensorids_for_log_view"


class UserNo:
    TENANT = "tenant"
    ROOT = "root"
    OPERATOR = "operator"
    WATCHER = "watcher"

    @classmethod
    def All(cls):
        return (cls.TENANT, cls.ROOT, cls.OPERATOR, cls.WATCHER)


class SensorNo:
    GENERAL = "general"
    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"
    ACC = "acc"
    ANALOG_ENGINE = "analog_engine"
    ENGINE = "engine"
    BATTERY = "battery"
    LIQUID_LEVEL = "liquid_level"
    PH = "ph"
    EC = "ec"
    GSM = "gsm"
    SWITCHES = "switches"
    ILLUMINATION = "illumination"


class TrackerDataNo:
    IN = "in"
    OUT = "out"


class DefSensorFuncBody:
    BATTERY = """local val = tonumber(ARGV[1]);
                  local result = val * 0.01;
                  return tostring(result);
                  """

    TEMPERATURE = """
                  local i1 = tonumber(ARGV[1]);
                  local i2 = tonumber(ARGV[2]);
                  local is_minus = ((bit.rshift(i1,4) == 0x0F) and (bit.band(i1,0x08)==0x08));
                  local val = bit.bor(bit.lshift(i1,8),i2);
                  if is_minus then
                    return -0.0625*(bit.band(bit.bnot(val),0xFFFF)+1);
                  else
                    return val*0.0625;
                  end
    """


class RGGWOpModeNo:
    AUTO = "auto"
    MANUAL = "manual"


class URLs:
    INDEX = r"/index"
    APP_EDIT_GROUP = r"edit/group"
    APP_ADM_GROUP = r"adm/group"
    APP_EDIT_USER = r"edit/user"
    APP_ADM_USER = r"adm/user"
    APP_ADM_SYS_COMMAND = r"adm/sys/command"
    APP_ADM_SYS_EEPROM = r"adm/sys/eeprom"
    APP_TRACKER_RAW_LOG = r"adm/sys/tracker/rawlog"
    VIEW_Q06_LOG = r"v/q06"
    APP_LOGOUT = r"logout"
    APP_ADM_LOGIN = r"adm/login"
    APP_EDIT_RGGW = r"edit/rggw"
    APP_ADM_RGGW = r"adm/rggw"
    APP_EDIT_SWITCH = r"edit/switch"
    APP_ADM_SWITCH = r"adm/switch"
    APP_EDIT_SENSOR = r"edit/sensor"
    APP_ADM_SENSOR = r"adm/sensor"
    APP_LOGIN = r"login"
    APP_SENSOR_MINS_AVG_LOG = r"log/smal"
    APP_EDIT_SENSOR_TYPE = r"edit/sensortype"
    APP_ADM_SENSOR_TYPE = r"adm/sensortype"
    APP_MEASURE_SENSOR = r"measure/sensor"
    APP_SYS_CFG = r'cfg/sys'
    APP_EDIT_SENSOR_TRIGGER = r"edit/sensortrigger"
    APP_ADM_SENSOR_TRIGGER = r"adm/sensortrigger"
    VIEW_SWITCH_SCHEDULES = r"v/ss"
    VIEW_RECENT_HOURS_SENSOR_DATA = r"v/rhsd"
    VIEW_SENSOR_MINS_AVG_TREND = r"v/smat"
    VIEW_SENSOR_MINS_AVG_DATA = r"v/smad"
    VIEW_SENSOR_TREND = r"v/st"
    VIEW_RECENT_HOURS_SENSOR_DATA_PLOTTING = r'v/rhsdp'
    VIEW_ADM_COND_RELAY_SWITCH_ACTION = r'v/acrsa'
    VIEW_CAMERAS = r'v/cameras'
    VIEW_EDIT_CAMERA = r'v/editcamera'
    APP_EM = r"em"
    API_GROUP_ADM = r"api/groupadm"
    API_USER_ADM = r"api/useradm"
    API_RGGW_ADM = r"api/rggwadm"
    API_SWITCH_ADM = r"api/switchadm"
    API_SENSOR_ADM = r"api/sensoradm"
    API_BASIC_USER = r"api/basicuser"
    API_EM = r"api/em"
    API_SENSOR_TYPE_ADM = r"api/sensortypeadm"
    API_SENSOR_MEASUREMENT = r"api/sensormeasurement"
    API_NODE_QUERY = r"api/node/query"
    API_CAMERA = r"api/camera"
    API_SYS_CFG = r'api/syscfg'
    API_SENSOR_TRIGGER = r"api/sensortrigger"
    EXPORT_FMT = "export/{0}"


class Google:
    GMAP_API_EN = "http://maps.googleapis.com/maps/api/js"
    GMAP_API_CH = "http://maps.google.cn/maps/api/js"


class TPL_NAMES:
    INDEX = r"index.html"
    APP_LOGIN = r"app_login_tpl.html"
    APP_ADM_LOGIN = r"app_adm_login_tpl.html"
    APP_SENSOR_MINS_AVG_LOG = r"app_sensor_mins_avg_log_tpl.html"
    APP_EDIT_GROUP = r"app_edit_group_tpl.html"
    APP_ADM_GROUP = r"app_adm_group_tpl.html"
    APP_EDIT_USER = r"app_edit_user_tpl.html"
    APP_ADM_USER = r"app_adm_user_tpl.html"
    APP_ADM_SYS_COMMAND = r"app_adm_sys_command_tpl.html"
    APP_ADM_SYS_EEPROM = r"app_adm_sys_eeprom_tpl.html"
    APP_EDIT_RGGW = r"app_edit_rggw_tpl.html"
    APP_ADM_RGGW = r"app_adm_rggw_tpl.html"
    APP_EDIT_SWITCH = r"app_edit_switch_tpl.html"
    APP_ADM_SWITCH = r"app_adm_switch_tpl.html"
    APP_EDIT_SENSOR = r"app_edit_sensor_tpl.html"
    APP_ADM_SENSOR = r"app_adm_sensor_tpl.html"
    APP_TRACKER_RAW_LOG = r"app_tracker_raw_log_tpl.html"
    VIEW_Q06_LOG = r"view_q06_log_tpl.html"
    VIEW_SWITCH_SCHEDULES = r"view_switch_schedules_tpl.html"
    VIEW_RECENT_HOURS_SENSOR_DATA = r"view_recent_hours_sensor_data_tpl.html"
    VIEW_SENSOR_MINS_AVG_TREND = r'view_sensors_mins_avg_trend_tpl.html'
    VIEW_SENSOR_MINS_AVG_DATA = r'view_sensors_mins_avg_data_tpl.html'
    VIEW_SENSOR_TREND = r'view_sensors_trend_tpl.html'
    APP_EM = r"app_em_tpl.html"
    APP_ADM_SENSOR_TYPE = r"app_adm_sensor_type_tpl.html"
    APP_EDIT_SENSOR_TYPE = r"app_edit_sensor_type_tpl.html"
    APP_MEASURE_SENSOR = r"app_measure_sensor_tpl.html"
    VIEW_CAMERAS = r"view_cameras_tpl.html"
    VIEW_EDIT_CAMERA = r"view_edit_camera_tpl.html"
    APP_SYS_CFG = r'app_sys_cfg_tpl.html'
    APP_EDIT_SENSOR_TRIGGER = r"app_edit_sensor_trigger_tpl.html"
    APP_ADM_SENSOR_TRIGGER = r"app_adm_sensor_trigger_tpl.html"


class Keys:
    MINUTE_RATE_FORMAT = "access_minute_rate:{0}_{1}_{2}" #prefix,key &ip
    USER_SESSION = 'user_session:{0}'
    SENSOR_TRIGGER_INTERVAL = 'sensor_trigger_interval:{0}'  # action rowid


class WebContent:
    ACCESS_OVER_LIMIT = "<h2>access over limit</h2>"
    SERVER_ERROR = "<h2>server error</h2>"
    PLEASE_LOGIN = "<h2>please login</h2>"


