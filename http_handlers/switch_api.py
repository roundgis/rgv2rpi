import api_core
import models
import rgv_consts
import rg_lib


async def AddSwitch(req_handler, sessionid, arg):
    """
    :param req_handler:
    :param sessionid:
    :param arg: {"switch": switch obj}
    :return:
    """
    try:
        await api_core.ReqLimit.CheckMinuteRate("AddSwitch", rg_lib.Cyclone.TryGetRealIp(req_handler))
        await api_core.Login.CheckRight(sessionid, (rgv_consts.UserNo.ROOT,))
        await api_core.RGGW.HasRGGW(arg['switch']['ownerid'])
        sql_str = """select r1.id from rgv_sensor r1, rgv_sensor_type r2
                      where r1.typeid=r2.id and r1.ownerid=? and r2.sensor_no=? limit 1"""
        sql_args = [arg['switch']['ownerid'], rgv_consts.SensorNo.SWITCHES]
        rec = await api_core.Sensor.Get([sql_str, sql_args])
        if rec is None:
            raise rg_lib.RGError(models.ErrorTypes.NoSensor('No Switches Sensor Installed'))
        switchid = await api_core.Switch.Add(arg['switch'])
        return await api_core.Switch.ById(switchid)
    except Exception:
        rg_lib.Cyclone.HandleErrInException()


async def RemoveSwitch(req_handler, sessionid, switchids):
    try:
        await api_core.ReqLimit.CheckMinuteRate("RemoveSwitch", rg_lib.Cyclone.TryGetRealIp(req_handler))
        await api_core.Login.CheckRight(sessionid, (rgv_consts.UserNo.ROOT,))
        await api_core.Switch.Remove(switchids)
        return "ok"
    except Exception:
        rg_lib.Cyclone.HandleErrInException()


async def SetSwitch(req_handler, sessionid, arg):
    """
    :param req_handler:
    :param sessionid:
    :param arg: {"switch": switch obj}
    :return:
    """
    try:
        await api_core.ReqLimit.CheckMinuteRate("SetSwitch", rg_lib.Cyclone.TryGetRealIp(req_handler))
        await api_core.Login.CheckRight(sessionid, (rgv_consts.UserNo.ROOT,))
        switchid = await api_core.Switch.Update(arg['switch'])
        return await api_core.Switch.ById(switchid)
    except Exception:
        rg_lib.Cyclone.HandleErrInException()


async def GetSwitch(req_handler, sessionid, switchid):
    try:
        await api_core.ReqLimit.CheckMinuteRate("GetSwitch", rg_lib.Cyclone.TryGetRealIp(req_handler))
        await api_core.Login.CheckRight(sessionid, (rgv_consts.UserNo.ROOT,))
        return await api_core.Switch.ById(switchid)
    except Exception:
        rg_lib.Cyclone.HandleErrInException()


async def SearchSwitch(req_handler, sessionid, para):
    """
    :param req_handler:
    :param sessionid:
    :param para: {"name": xxx, "val": xxx}
    :return:
    """
    try:
        await api_core.ReqLimit.CheckMinuteRate("SearchSwitch", rg_lib.Cyclone.TryGetRealIp(req_handler))
        await api_core.Login.CheckRight(sessionid, (rgv_consts.UserNo.ROOT,))
        return await api_core.Switch.Search(para)
    except Exception as e:
        rg_lib.Cyclone.HandleErrInException()
