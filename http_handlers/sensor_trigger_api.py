import rg_lib
import models
import api_core
import rgv_consts


def __SearchSensorTrigger(uid, para):
    sql_str = """select * from rgv_sensor_trigger 
                 where id in (select r1.id 
                              from rgv_sensor_trigger r1,
                                   rgv_sensor_trigger_sensor r2,
                                   rgv_sensor r3,
                                   rgv_rggw r4,
                                   rgv_user_group r5
                              where r1.id=r2.triggerid and r2.sensorid=r3.id
                              and r3.ownerid=r4.id
                              and r4.groupid=r5.groupid and r5.uid=?)"""
    if para['name'] == "name":
        sql_str += " and name like ? limit ?"
    else:
        raise rg_lib.RGError(models.ErrorTypes.UnsupportedOp())
    sql_args = (uid, "{0}%".format(para['val']), rgv_consts.DbConsts.SEARCH_LIMIT)
    return api_core.BizDB.Query([sql_str, sql_args])


async def FindTrigger(req_handler, para):
    """
    :param req_handler:
    :param para: {"name": xxx, "val": xxx, "token"}
    :return: user notice expr rows
    """
    try:
        await api_core.ReqLimit.CheckMinuteRate('FindTrigger', rg_lib.Cyclone.TryGetRealIp(req_handler))
        user = await api_core.Login.HasTenant(para['token'])
        return await __SearchSensorTrigger(user['id'], para)
    except Exception:
        rg_lib.Cyclone.HandleErrInException()


async def SetTrigger(req_handler, arg):
    """
    :param req_handler:
    :param arg: {"action_trigger", "token"}
    :return: conditional action
    """
    try:
        await api_core.ReqLimit.CheckMinuteRate('SetTrigger', rg_lib.Cyclone.TryGetRealIp(req_handler))
        await api_core.Login.HasTenant(arg['token'])
        return await api_core.SensorTrigger.Upsert(arg['trigger'])
    except Exception:
        rg_lib.Cyclone.HandleErrInException()


async def RemoveTrigger(req_handler, arg):
    """
    :param req_handler:
    :param arg: {"token", "triggerids"}
    :return: string
    """
    try:
        await api_core.ReqLimit.CheckMinuteRate('RemoveTrigger', rg_lib.Cyclone.TryGetRealIp(req_handler))
        await api_core.Login.HasTenant(arg['token'])
        await api_core.SensorTrigger.Remove(arg['triggerids'])
        return "ok"
    except Exception:
        rg_lib.Cyclone.HandleErrInException()


async def GetTrigger(req_handler, arg):
    """
    :param req_handler:
    :param arg: {token, triggerid}
    :return:
    """
    try:
        await api_core.ReqLimit.CheckMinuteRate('GetActionTrigger', rg_lib.Cyclone.TryGetRealIp(req_handler))
        await api_core.Login.HasTenant(arg['token'])
        return await api_core.SensorTrigger.GetMdl(arg['triggerid'])
    except Exception:
        rg_lib.Cyclone.HandleErrInException()

