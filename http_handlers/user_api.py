import rgv_consts
import api_core
import rg_lib


async def AddUser(req_handler, sessionid, arg):
    """
    :param req_handler:
    :param sessionid:
    :param arg: {"user": user obj}
    :return:
    """
    try:
        await api_core.ReqLimit.CheckMinuteRate('AddUser', rg_lib.Cyclone.TryGetRealIp(req_handler))
        await api_core.Login.CheckRight(sessionid, (rgv_consts.UserNo.ROOT,))
        await api_core.User.Add(arg['user'])
        return await api_core.User.ById(arg['user']['id'])
    except Exception:
        rg_lib.Cyclone.HandleErrInException()


async def SetUser(req_handler, sessionid, arg):
    """
    :param req_handler:
    :param sessionid:
    :param arg: {'user': user obj}
    :return:
    """
    try:
        await api_core.ReqLimit.CheckMinuteRate('SetUser', rg_lib.Cyclone.TryGetRealIp(req_handler))
        await api_core.Login.CheckRight(sessionid, (rgv_consts.UserNo.ROOT,))
        await api_core.User.Update(arg['user'])
        return await api_core.User.ById(arg['user']['id'])
    except Exception:
        rg_lib.Cyclone.HandleErrInException()


async def RemoveUser(req_handler, sessionid, userid):
    try:
        await api_core.ReqLimit.CheckMinuteRate('RemoveUser', rg_lib.Cyclone.TryGetRealIp(req_handler))
        await api_core.Login.CheckRight(sessionid, (rgv_consts.UserNo.ROOT,))
        await api_core.User.Remove(userid)
        return "ok"
    except Exception:
        rg_lib.Cyclone.HandleErrInException()


async def SetUserGroup(req_handler, sessionid, arg):
    """
    :param req_handler:
    :param sessionid:
    :param arg: {"groupid": group id, "userids": [], "is_add": boolean}
    :return:
    """
    try:
        await api_core.ReqLimit.CheckMinuteRate('SetUserGroup', rg_lib.Cyclone.TryGetRealIp(req_handler))
        await api_core.Login.CheckRight(sessionid, (rgv_consts.UserNo.ROOT,))
        await api_core.Group.HasGroup(arg['groupid'])
        await api_core.User.SetGroupId(arg['userids'], arg['groupid'], arg['is_add'])
        sql_str = rg_lib.Sqlite.GenInSql("""select * from rgv_user where id in """, arg['userids'])
        rows = await api_core.BizDB.Query([sql_str, arg['userids']])
        for row in rows:
            row['groups'] = await api_core.User.GetGroups(row['id'])
        return rows
    except Exception:
        rg_lib.Cyclone.HandleErrInException()


async def GetUser(req_handler, sessionid, userid):
    """
    :param req_handler:
    :param sessionid:
    :param userid: string
    :return: user obj
    """
    try:
        await api_core.ReqLimit.CheckMinuteRate('GetUser', rg_lib.Cyclone.TryGetRealIp(req_handler), 3)
        await api_core.Login.CheckRight(sessionid, (rgv_consts.UserNo.ROOT,))
        return await api_core.User.ById(userid)
    except Exception:
        rg_lib.Cyclone.HandleErrInException()


async def SearchUser(req_handler, sessionid, arg):
    try:
        await api_core.ReqLimit.CheckMinuteRate('SearchUser', rg_lib.Cyclone.TryGetRealIp(req_handler))
        await api_core.Login.CheckRight(sessionid, (rgv_consts.UserNo.ROOT,))
        tbls = await api_core.User.Search(arg)
        for rec in tbls:
            rec['groups'] = await api_core.User.GetGroups(rec['id'])
        return tbls
    except Exception:
        rg_lib.Cyclone.HandleErrInException()


async def SetUserPassword(req_handler, sessionid, new_pwd):
    try:
        await api_core.ReqLimit.CheckMinuteRate("SetUserPassword", rg_lib.Cyclone.TryGetRealIp(req_handler))
        user = await api_core.Login.HasTenant(sessionid)
        await api_core.User.SetPwd(user['id'], new_pwd)
        return "ok"
    except Exception:
        rg_lib.Cyclone.HandleErrInException()
