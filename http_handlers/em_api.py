from twisted.internet import threads
import bson
import os.path as os_path
import rgv_consts
import api_core
import api_em
from reports import sensor_log as sensor_log_report
import rg_lib
import settings


async def GetRGGWByGroup(req_handler, sessionid, arg_tbl):
    """
    :param req_handler:
    :param sessionid:
    :param arg_tbl: {"groupids": [groupid,]}
    :return:
    """
    try:
        await api_core.ReqLimit.CheckMinuteRate("GetRGGWByGroup", rg_lib.Cyclone.TryGetRealIp(req_handler), 30)
        await api_core.Login.HasTenant(sessionid)
        return await api_em.GetRGGWByGroup(arg_tbl)
    except Exception:
        rg_lib.Cyclone.HandleErrInException()


async def FindSwitch(req_handler, sessionid, arg):
    """
    :param req_handler: http request
    :param sessionid: string
    :param arg: {"gwids": [id,], "status_only": boolean}
    :return: {"switches": [relay_switch,...], 'gws': [serial_device, ...]}
    """
    try:
        await api_core.ReqLimit.CheckMinuteRate("FindSwitch", rg_lib.Cyclone.TryGetRealIp(req_handler), 30)
        await api_core.Login.HasTenant(sessionid)
        return await api_em.FindSwitch(arg)
    except Exception:
        rg_lib.Cyclone.HandleErrInException()


async def OpenRelaySwitch(req_handler, sessionid, para):
    """
    :param sessionid:
    :param para: {"switchids": [], "working_seconds": 0}
    :return:
    """
    try:
        await api_core.ReqLimit.CheckMinuteRate("OpenRelaySwitch", rg_lib.Cyclone.TryGetRealIp(req_handler))
        user = await api_core.Login.CheckRight(sessionid, (rgv_consts.UserNo.OPERATOR, rgv_consts.UserNo.ROOT))
        para['uid'] = user['id']
        return await api_em.OpenRelaySwitch(para)
    except Exception:
        rg_lib.Cyclone.HandleErrInException()


async def CloseRelaySwitch(req_handler, sessionid, para):
    """
    :param req_handler:
    :param sessionid:
    :param para: {"switchids"}
    :return:
    """
    try:
        await api_core.ReqLimit.CheckMinuteRate("CloseRelaySwitch", rg_lib.Cyclone.TryGetRealIp(req_handler))
        await api_core.Login.CheckRight(sessionid, (rgv_consts.UserNo.OPERATOR, rgv_consts.UserNo.ROOT))
        return await api_em.CloseRelaySwitch(para)
    except Exception:
        rg_lib.Cyclone.HandleErrInException()


async def FindSensor(req_handler, sessionid, para):
    """
    :param req_handler:
    :param sessionid:
    :param para: {"ownerids": [ownerid,]}
    :return: {ownerids: [ownerid,...], data_tbl: {ownerid->[sensor data]}}
    """
    try:
        await api_core.ReqLimit.CheckMinuteRate("FindLatestSensorData", rg_lib.Cyclone.TryGetRealIp(req_handler), 30)
        await api_core.Login.HasTenant(sessionid)
        return await api_em.FindSensor(para)
    except Exception:
        rg_lib.Cyclone.HandleErrInException()


async def FindSensorMinsAvgLog(req_handler, sessionid, para):
    """
    :param req_handler: RequestHandler
    :param sessionid: unicode
    :param para: {"sensorids":[], "start_ts": timestamp, "stop_ts": timestamp,
                  "mins_interval": integer}
                  or {"sensorids":[], "hours": hours range, "mins_interval": integer}
    :return: {"sensorids":[], "log_tbl": {sensorid->[mins data,...]},
              "sensor_tbl": {sensorid->sensor tbl}, "ts_series": [series of timestamp]}
    """
    try:
        await api_core.ReqLimit.CheckMinuteRate("FindSensorMinsAvgLog", rg_lib.Cyclone.TryGetRealIp(req_handler))
        await api_core.Login.HasTenant(sessionid)
        return await api_em.FindSensorMinsAvgLog(para)
    except Exception:
        rg_lib.Cyclone.HandleErrInException()


async def FindSensorRecentHourAvgLog(req_handler, sessionid, para):
    """
    :param req_handler: RequestHandler
    :param sessionid: unicode
    :param para: {"sensorids":[], "hours": integer, "ts": timestamp}
    :return: {"sensorids":[], "log_tbl": {sensorid->[hours data,...]},
              'sensor_tbl': {sensorid->sensor tbl}}
    """
    try:
        await api_core.ReqLimit.CheckMinuteRate("FindSensorRecentHourAvgLog", rg_lib.Cyclone.TryGetRealIp(req_handler))
        await api_core.Login.HasTenant(sessionid)
        return await api_em.FindSensorRecentHourAvgLog(para)
    except Exception:
        rg_lib.Cyclone.HandleErrInException()


async def FindSensorLog(req_handler, sessionid, para):
    """
    :param req_handler: RequestHandler
    :param sessionid: unicode
    :param para: {"sensorids":[], start_ts, stop_ts}
    :return: {"sensorids":[], "log_tbl": {sensorid->[hours data,...]},
              'sensor_tbl': {sensorid->sensor tbl}}
    """
    try:
        await api_core.ReqLimit.CheckMinuteRate("FindSensorLog", rg_lib.Cyclone.TryGetRealIp(req_handler))
        await api_core.Login.HasTenant(sessionid)
        return await api_em.FindSensorLog(para)
    except Exception:
        rg_lib.Cyclone.HandleErrInException()


async def SwitchRGGWMode(req_handler, sessionid, para):
    """
    :param req_handler:
    :param sessionid:
    :param para: {deviceid, mode}
    :return:
    """
    try:
        await api_core.ReqLimit.CheckMinuteRate("SwitchRGGWMode", rg_lib.Cyclone.TryGetRealIp(req_handler))
        await api_core.Login.CheckRight(sessionid, (rgv_consts.UserNo.OPERATOR, rgv_consts.UserNo.ROOT))
        return await api_em.SwitchRGGWMode(para)
    except Exception:
        rg_lib.Cyclone.HandleErrInException()


async def AddSchedule(req_handler, sessionid, para):
    """
    :param req_handler:
    :param sessionid:
    :param para: {"schedule": schedule tbl}
    :return:
    """
    try:
        await api_core.ReqLimit.CheckMinuteRate("AddSchedule", rg_lib.Cyclone.TryGetRealIp(req_handler))
        user = await api_core.Login.CheckRight(sessionid, (rgv_consts.UserNo.OPERATOR, rgv_consts.UserNo.ROOT))
        para['uid'] = user['id']
        return await api_em.AddSchedule(para)
    except Exception:
        rg_lib.Cyclone.HandleErrInException()


async def RemoveSchedule(req_handler, sessionid, para):
    """
    :param req_handler:
    :param sessionid:
    :param para: {"scheduleids": [id,...]}
    :return:
    """
    try:
        await api_core.ReqLimit.CheckMinuteRate("RemoveSchedules", rg_lib.Cyclone.TryGetRealIp(req_handler))
        await api_core.Login.CheckRight(sessionid, (rgv_consts.UserNo.OPERATOR, rgv_consts.UserNo.ROOT))
        return await api_em.RemoveSchedule(para)
    except Exception:
        rg_lib.Cyclone.HandleErrInException()


async def GetUserSchedules(req_handler, sessionid, para):
    """
    :param req_handler:
    :param sessionid:
    :param para: {}
    :return: [schedule obj,...]
    """
    try:
        await api_core.ReqLimit.CheckMinuteRate("GetUserSchedules", rg_lib.Cyclone.TryGetRealIp(req_handler))
        user = await api_core.Login.CheckRight(sessionid, (rgv_consts.UserNo.OPERATOR, rgv_consts.UserNo.ROOT))
        para['user'] = user
        return await api_em.GetUserSchedules(para)
    except Exception:
        rg_lib.Cyclone.HandleErrInException()


async def ExportSensorMinsAvgLog(req_handler, sessionid, para):
    """
    :param req_handler: 
    :param sessionid: 
    :param para: {"sensorids":[], "start_ts": timestamp, "stop_ts": timestamp,
                  "mins_interval": integer, 'tz_offset': integer}
                  or {"sensorids":[], "hours": hours range, "mins_interval": integer,
                  'tz_offset': integer}
    :return: URL
    """
    try:
        await api_core.ReqLimit.CheckMinuteRate("ExportSensorMinsAvgLog", rg_lib.Cyclone.TryGetRealIp(req_handler))
        await api_core.Login.HasTenant(sessionid)
        result = await api_core.DataLog.SensorMinsAvg2(para)
        result['tz_offset'] = para['tz_offset']
        file_name = "{0}.xlsx".format(bson.ObjectId())
        file_path = os_path.join(settings.WEB['export_path'], file_name)
        await threads.deferToThread(sensor_log_report.Make, file_path, result)
        return os_path.join('/', rgv_consts.URLs.EXPORT_FMT.format(file_name))
    except Exception:
        rg_lib.Cyclone.HandleErrInException()
