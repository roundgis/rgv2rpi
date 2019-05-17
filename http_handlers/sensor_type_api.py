from twisted.internet import defer
import rgv_consts
import api_core
import rg_lib


async def AddSensorType(req_handler, sessionid, arg):
    """
    :param req_handler:
    :param sessionid:
    :param arg: {"sensor_type": sensor type obj}
    :return:
    """
    try:
        await api_core.ReqLimit.CheckMinuteRate("AddSensorType", rg_lib.Cyclone.TryGetRealIp(req_handler))
        await api_core.Login.CheckRight(sessionid, (rgv_consts.UserNo.ROOT,))
        return await api_core.SensorType.ById(await api_core.SensorType.Add(arg['sensor_type']))
    except Exception:
        rg_lib.Cyclone.HandleErrInException()


async def RemoveSensorType(req_handler, sessionid, typeids):
    try:
        await api_core.ReqLimit.CheckMinuteRate("RemoveSensorType", rg_lib.Cyclone.TryGetRealIp(req_handler))
        await api_core.Login.CheckRight(sessionid, (rgv_consts.UserNo.ROOT,))
        await api_core.SensorType.Remove(typeids)
        return "ok"
    except Exception:
        rg_lib.Cyclone.HandleErrInException()


async def SetSensorType(req_handler, sessionid, arg):
    """
    :param req_handler:
    :param sessionid:
    :param arg: {"sensor_type": sensor type obj}
    :return:
    """
    try:
        await api_core.ReqLimit.CheckMinuteRate("SetSensorType", rg_lib.Cyclone.TryGetRealIp(req_handler))
        await api_core.Login.CheckRight(sessionid, (rgv_consts.UserNo.ROOT,))
        return await api_core.SensorType.ById(await api_core.SensorType.Update(arg['sensor_type']))
    except Exception:
        rg_lib.Cyclone.HandleErrInException()


async def GetSensorType(req_handler, sessionid, typeid):
    try:
        await api_core.ReqLimit.CheckMinuteRate("GetSensorType", rg_lib.Cyclone.TryGetRealIp(req_handler))
        await api_core.Login.CheckRight(sessionid, (rgv_consts.UserNo.ROOT,))
        return await api_core.SensorType.ById(typeid)
    except Exception:
        rg_lib.Cyclone.HandleErrInException()


async def SearchSensorType(req_handler, sessionid, para):
    """
    :param req_handler:
    :param sessionid:
    :param para: {"name": xxx, "val": xxx}
    :return:
    """
    try:
        await api_core.ReqLimit.CheckMinuteRate("SearchSensorType", rg_lib.Cyclone.TryGetRealIp(req_handler))
        await api_core.Login.CheckRight(sessionid, (rgv_consts.UserNo.ROOT,))
        return await api_core.SensorType.Search(para)
    except Exception as e:
        rg_lib.Cyclone.HandleErrInException()
