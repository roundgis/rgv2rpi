from twisted.internet import defer
import rgv_consts
import rg_lib
import api_core


async def AddGroup(req_handler, sessionid, arg):
    """
    :param req_handler:
    :param sessionid:
    :param arg: {"group": group obj}
    :return: group obj
    """
    try:
        await api_core.ReqLimit.CheckMinuteRate('AddGroup', rg_lib.Cyclone.TryGetRealIp(req_handler), 3)
        await api_core.Login.CheckRight(sessionid, (rgv_consts.UserNo.ROOT,))
        await api_core.Group.Add(arg['group'])
        return await api_core.Group.ById(arg['group']['id'])
    except Exception:
        rg_lib.Cyclone.HandleErrInException()


async def SetGroup(req_handler, sessionid, arg):
    """
    :param req_handler:
    :param sessionid:
    :param arg: {"group": group obj}
    :return: group obj
    """
    try:
        await api_core.ReqLimit.CheckMinuteRate('SetGroup', rg_lib.Cyclone.TryGetRealIp(req_handler), 3)
        await api_core.Login.CheckRight(sessionid, (rgv_consts.UserNo.ROOT,))
        await api_core.Group.Update(arg['group'])
        return await api_core.Group.ById(arg['group']['id'])
    except Exception:
        rg_lib.Cyclone.HandleErrInException()


async def GetGroup(req_handler, sessionid, groupid):
    """
    :param req_handler:
    :param sessionid:
    :param groupid: string
    :return: group obj
    """
    try:
        await api_core.ReqLimit.CheckMinuteRate('GetGroup', rg_lib.Cyclone.TryGetRealIp(req_handler), 3)
        await api_core.Login.CheckRight(sessionid, (rgv_consts.UserNo.ROOT,))
        return await api_core.Group.ById(groupid)
    except Exception:
        rg_lib.Cyclone.HandleErrInException()


async def RemoveGroup(req_handler, sessionid, groupids):
    try:
        await api_core.ReqLimit.CheckMinuteRate('RemoveGroup', rg_lib.Cyclone.TryGetRealIp(req_handler), 3)
        await api_core.Login.CheckRight(sessionid, (rgv_consts.UserNo.ROOT,))
        await api_core.Group.Remove(groupids)
        return "ok"
    except Exception:
        rg_lib.Cyclone.HandleErrInException()


async def SearchGroup(req_handler, sessionid, arg):
    """
    :param req_handler:
    :param sessionid:
    :param arg:
    :return:
    """
    try:
        await api_core.ReqLimit.CheckMinuteRate('SearchGroup', rg_lib.Cyclone.TryGetRealIp(req_handler), 3)
        await api_core.Login.CheckRight(sessionid, (rgv_consts.UserNo.ROOT,))
        return await api_core.Group.Search(arg)
    except Exception:
        rg_lib.Cyclone.HandleErrInException()


async def GetUserGroups(req_handler, sessionid):
    try:
        await api_core.ReqLimit.CheckMinuteRate("GetUserGroups", rg_lib.Cyclone.TryGetRealIp(req_handler))
        user = await api_core.Login.CheckRight(sessionid, rgv_consts.UserNo.All())
        return await api_core.User.GetGroups(user['id'])
    except Exception:
        rg_lib.Cyclone.HandleErrInException()
