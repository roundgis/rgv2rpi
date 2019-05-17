import rgv_consts
import api_core
import rg_lib


async def AddSensor(req_handler, sessionid, arg):
    """
    :param req_handler:
    :param sessionid:
    :param arg: {"sensor": sensor obj}
    :return:
    """
    try:
        await api_core.ReqLimit.CheckMinuteRate("AddSensor", rg_lib.Cyclone.TryGetRealIp(req_handler))
        await api_core.Login.CheckRight(sessionid, (rgv_consts.UserNo.ROOT,))
        sensorid = await api_core.Sensor.Add(arg['sensor'])
        return await api_core.Sensor.ById(sensorid)
    except Exception:
        rg_lib.Cyclone.HandleErrInException()


async def RemoveSensor(req_handler, sessionid, sensorids):
    try:
        await api_core.ReqLimit.CheckMinuteRate("RemoveSensor", rg_lib.Cyclone.TryGetRealIp(req_handler))
        await api_core.Login.CheckRight(sessionid, (rgv_consts.UserNo.ROOT,))
        await api_core.Sensor.Remove(sensorids)
        return "ok"
    except Exception:
        rg_lib.Cyclone.HandleErrInException()


async def SetSensor(req_handler, sessionid, arg):
    """
    :param req_handler:
    :param sessionid:
    :param arg: {"sensor": sensor obj}
    :return:
    """
    try:
        await api_core.ReqLimit.CheckMinuteRate("SetSensor", rg_lib.Cyclone.TryGetRealIp(req_handler))
        await api_core.Login.CheckRight(sessionid, (rgv_consts.UserNo.ROOT,))
        sensorid = await api_core.Sensor.Update(arg['sensor'])
        return await api_core.Sensor.ById(sensorid)
    except Exception:
        rg_lib.Cyclone.HandleErrInException()


async def GetSensor(req_handler, sessionid, sensorid):
    try:
        await api_core.ReqLimit.CheckMinuteRate("GetSensor", rg_lib.Cyclone.TryGetRealIp(req_handler))
        await api_core.Login.CheckRight(sessionid, (rgv_consts.UserNo.ROOT,))
        return await api_core.Sensor.ById(sensorid)
    except Exception:
        rg_lib.Cyclone.HandleErrInException()


async def SearchSensor(req_handler, sessionid, para):
    """
    :param req_handler:
    :param sessionid:
    :param para: {"name": xxx, "val": xxx}
    :return:
    """
    try:
        await api_core.ReqLimit.CheckMinuteRate("SearchSensor", rg_lib.Cyclone.TryGetRealIp(req_handler))
        await api_core.Login.CheckRight(sessionid, (rgv_consts.UserNo.ROOT,))
        return await api_core.Sensor.Search(para)
    except Exception as e:
        rg_lib.Cyclone.HandleErrInException()
