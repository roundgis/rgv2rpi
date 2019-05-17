import api_core
import rg_lib


async def AddCamera(req_handler, sessionid, arg):
    """
    :param req_handler:
    :param sessionid:
    :param arg: {"camera": user obj}
    :return:
    """
    try:
        await api_core.ReqLimit.CheckMinuteRate('AddCamera', rg_lib.Cyclone.TryGetRealIp(req_handler))
        user = await api_core.Login.HasTenant(sessionid)
        arg['camera']['uid'] = user['id']
        newid = await api_core.Camera.Add(arg['camera'])
        return await api_core.Camera.ById(newid)
    except Exception:
        rg_lib.Cyclone.HandleErrInException()


async def RemoveCamera(req_handler, sessionid, ids):
    try:
        await api_core.ReqLimit.CheckMinuteRate('RemoveCamera', rg_lib.Cyclone.TryGetRealIp(req_handler))
        await api_core.Login.HasTenant(sessionid)
        await api_core.Camera.Remove(ids)
        return "ok"
    except Exception:
        rg_lib.Cyclone.HandleErrInException()


async def GetCamera(req_handler, sessionid, nid):
    """
    :param req_handler:
    :param sessionid:
    :param nid: string
    :return: user obj
    """
    try:
        await api_core.ReqLimit.CheckMinuteRate('GetCamera', rg_lib.Cyclone.TryGetRealIp(req_handler), 3)
        await api_core.Login.HasTenant(sessionid)
        return await api_core.Camera.ById(nid)
    except Exception:
        rg_lib.Cyclone.HandleErrInException()


async def SearchCamera(req_handler, sessionid, arg):
    try:
        await api_core.ReqLimit.CheckMinuteRate('SearchCamera', rg_lib.Cyclone.TryGetRealIp(req_handler))
        user = await api_core.Login.HasTenant(sessionid)
        return await api_core.Camera.Search(user['id'], arg)
    except Exception:
        rg_lib.Cyclone.HandleErrInException()
