import functools
from . import em_api
from . import group_api
from . import switch_api
from . import sensor_api
from . import sensor_type_api
from . import rggw_api
from . import user_api
from . import sys_cfg_api
from . import sensor_trigger_api as cond_api
from http_handlers import camera_api
import rg_lib


class Base(rg_lib.AsyncDynFuncHandler):
    def initialize(self, **kwargs):
        self.FUNC_TBL = {}

    def GetFunc(self, func_name):
        return self.FUNC_TBL[func_name] if func_name in self.FUNC_TBL else None


class GroupAdm(Base):
    def initialize(self, **kwargs):
        self.FUNC_TBL = {"AddGroup": functools.partial(group_api.AddGroup, self),
                         "SetGroup": functools.partial(group_api.SetGroup, self),
                         "GetGroup": functools.partial(group_api.GetGroup, self),
                         'RemoveGroup': functools.partial(group_api.RemoveGroup, self),
                         'SearchGroup': functools.partial(group_api.SearchGroup, self)}


class UserAdm(Base):
    def initialize(self, **kwargs):
        self.FUNC_TBL = {"AddUser": functools.partial(user_api.AddUser, self),
                         "SetUser": functools.partial(user_api.SetUser, self),
                         "GetUser": functools.partial(user_api.GetUser, self),
                         'RemoveUser': functools.partial(user_api.RemoveUser, self),
                         'SearchUser': functools.partial(user_api.SearchUser, self),
                         'SetUserGroup': functools.partial(user_api.SetUserGroup, self)}


class RGGWAdm(Base):
    def initialize(self, **kwargs):
        self.FUNC_TBL = {"AddDevice": functools.partial(rggw_api.AddDevice, self),
                         "SetDevice": functools.partial(rggw_api.SetDevice, self),
                         "GetDevice": functools.partial(rggw_api.GetDevice, self),
                         'RemoveDevice': functools.partial(rggw_api.RemoveDevice, self),
                         'SearchDevice': functools.partial(rggw_api.SearchDevice, self),
                         'SetGroup': functools.partial(rggw_api.SetGroup, self),
                         'GetRecentQ06': functools.partial(rggw_api.GetRecentQ06, self),
                         'FindQ06': functools.partial(rggw_api.FindQ06, self),
                         "GetRecentTrackerRawLog": functools.partial(rggw_api.GetRecentTrackerRawLog, self),
                         'FindTrackerRawLog': functools.partial(rggw_api.FindTrackerRawLog, self),
                         'SetEEPROM': functools.partial(rggw_api.SetEEPROM, self),
                         'GetEEPROM': functools.partial(rggw_api.GetEEPROM, self),
                         'SendCommand': functools.partial(rggw_api.SendCommand, self),
                         'SendRelay': functools.partial(rggw_api.SendRelay, self),
                         }


class SwitchAdm(Base):
    def initialize(self, **kwargs):
        self.FUNC_TBL = {"AddSwitch": functools.partial(switch_api.AddSwitch, self),
                         "SetSwitch": functools.partial(switch_api.SetSwitch, self),
                         "GetSwitch": functools.partial(switch_api.GetSwitch, self),
                         'RemoveSwitch': functools.partial(switch_api.RemoveSwitch, self),
                         'SearchSwitch': functools.partial(switch_api.SearchSwitch, self)}


class SensorAdm(Base):
    def initialize(self, **kwargs):
        self.FUNC_TBL = {"AddSensor": functools.partial(sensor_api.AddSensor, self),
                         "SetSensor": functools.partial(sensor_api.SetSensor, self),
                         "GetSensor": functools.partial(sensor_api.GetSensor, self),
                         'RemoveSensor': functools.partial(sensor_api.RemoveSensor, self),
                         'SearchSensor': functools.partial(sensor_api.SearchSensor, self)}


class SensorTypeAdm(Base):
    def initialize(self, **kwargs):
        self.FUNC_TBL = {"AddSensorType": functools.partial(sensor_type_api.AddSensorType, self),
                         "SetSensorType": functools.partial(sensor_type_api.SetSensorType, self),
                         "GetSensorType": functools.partial(sensor_type_api.GetSensorType, self),
                         'RemoveSensorType': functools.partial(sensor_type_api.RemoveSensorType, self),
                         'SearchSensorType': functools.partial(sensor_type_api.SearchSensorType, self)}


class BasicUser(Base):
    def initialize(self, **kwargs):
        self.FUNC_TBL = {"SetPassword": functools.partial(user_api.SetUserPassword, self),
                         }


class EM(Base):
    def initialize(self, **kwargs):
        self.FUNC_TBL = {"GetGroupInfo": functools.partial(group_api.GetUserGroups, self),
                         "OpenRelaySwitch": functools.partial(em_api.OpenRelaySwitch, self),
                         "CloseRelaySwitch": functools.partial(em_api.CloseRelaySwitch, self),
                         "GetRGGWByGroup": functools.partial(em_api.GetRGGWByGroup, self),
                         "FindSwitch": functools.partial(em_api.FindSwitch, self),
                         "FindSensor": functools.partial(em_api.FindSensor, self),
                         'SwitchRGGWMode': functools.partial(em_api.SwitchRGGWMode, self),
                         'FindSensorMinsAvgLog': functools.partial(em_api.FindSensorMinsAvgLog, self),
                         'ExportSensorMinsAvgLog': functools.partial(em_api.ExportSensorMinsAvgLog, self),
                         'FindSensorRecentHourAvgLog': functools.partial(em_api.FindSensorRecentHourAvgLog, self),
                         'FindSensorLog': functools.partial(em_api.FindSensorLog, self),
                         'AddSchedule': functools.partial(em_api.AddSchedule, self),
                         'GetUserSchedules': functools.partial(em_api.GetUserSchedules, self),
                         'RemoveSchedule': functools.partial(em_api.RemoveSchedule, self)}


class CameraAdm(Base):
    def initialize(self, **kwargs):
        self.FUNC_TBL = {"SearchCamera": functools.partial(camera_api.SearchCamera, self),
                         'RemoveCamera': functools.partial(camera_api.RemoveCamera, self),
                         'AddCamera': functools.partial(camera_api.AddCamera, self)
                         }


class SysCfg(Base):
    def initialize(self, **kwargs):
        self.FUNC_TBL = {"SetCfg": functools.partial(sys_cfg_api.SetCfg, self),
                         "GetCfg": functools.partial(sys_cfg_api.GetCfg, self)}


class SensorTriggerAdm(Base):
    def initialize(self, **kwargs):
        self.FUNC_TBL = {"FindTrigger": functools.partial(cond_api.FindTrigger, self),
                         'RemoveTrigger': functools.partial(cond_api.RemoveTrigger, self),
                         'SetTrigger': functools.partial(cond_api.SetTrigger, self),
                         'GetTrigger': functools.partial(cond_api.GetTrigger, self)
                         }
