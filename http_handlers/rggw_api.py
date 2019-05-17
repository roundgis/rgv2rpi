from twisted.python import log
import rgv_consts
import models
import rggw_lib
import rg_lib
import api_core


async def __GetRGGW(deviceid):
    return await api_core.RGGW.Get(["""select r1.*, r2.name group_name from
                                                  rgv_rggw r1 left join rgv_group r2 on
                                                  r1.groupid=r2.id where r1.id=?""", (deviceid,)])


async def AddDevice(req_handler, sessionid, para):
    """
    :param sessionid:
    :param para: {"device"->device tbl}
    :return:
    """
    try:
        await api_core.ReqLimit.CheckMinuteRate("AddDevice", rg_lib.Cyclone.TryGetRealIp(req_handler))
        await api_core.Login.CheckRight(sessionid, (rgv_consts.UserNo.ROOT,))
        devid = await api_core.RGGW.Add(para['device'])
        return await __GetRGGW(devid)
    except Exception:
        rg_lib.Cyclone.HandleErrInException()


async def RemoveDevice(req_handler, sessionid, deviceids):
    try:
        await api_core.ReqLimit.CheckMinuteRate("RemoveDevice", rg_lib.Cyclone.TryGetRealIp(req_handler))
        await api_core.Login.CheckRight(sessionid, (rgv_consts.UserNo.ROOT,))
        await api_core.RGGW.Remove(deviceids)
        return "ok"
    except Exception:
        rg_lib.Cyclone.HandleErrInException()


async def SetDevice(req_handler, sessionid, para):
    try:
        await api_core.ReqLimit.CheckMinuteRate("SetDevice", rg_lib.Cyclone.TryGetRealIp(req_handler))
        await api_core.Login.CheckRight(sessionid, (rgv_consts.UserNo.ROOT,))
        devid = await api_core.RGGW.Update(para['device'])
        return await __GetRGGW(devid)
    except Exception:
        rg_lib.Cyclone.HandleErrInException()


async def GetDevice(req_handler, sessionid, deviceid):
    try:
        await api_core.ReqLimit.CheckMinuteRate("GetDevice", rg_lib.Cyclone.TryGetRealIp(req_handler))
        await api_core.Login.CheckRight(sessionid, (rgv_consts.UserNo.ROOT,))
        return await __GetRGGW(deviceid)
    except Exception:
        rg_lib.Cyclone.HandleErrInException()


async def SearchDevice(req_handler, sessionid, para):
    """
    :param req_handler:
    :param sessionid:
    :param para: {"name": xxx, "val": xxx}
    :return:
    """
    try:
        await api_core.ReqLimit.CheckMinuteRate("SearchDevice", rg_lib.Cyclone.TryGetRealIp(req_handler))
        await api_core.Login.CheckRight(sessionid, (rgv_consts.UserNo.ROOT,))
        return await api_core.RGGW.Search(para)
    except Exception as e:
        rg_lib.Cyclone.HandleErrInException()


async def SetGroup(req_handler, sessionid, para):
    """
    :param req_handler:
    :param sessionid:
    :param para: {"deviceids": [deviceid,...], "groupid": group id,
                  "is_add": true or false}
    :return:
    """
    try:
        await api_core.ReqLimit.CheckMinuteRate('SetGroup3', rg_lib.Cyclone.TryGetRealIp(req_handler), 3)
        await api_core.Login.CheckRight(sessionid, (rgv_consts.UserNo.ROOT,))
        grp_mdl = await api_core.Group.HasGroup(para['groupid'])
        grpid = para['groupid'] if para['is_add'] else ""
        await api_core.RGGW.SetGroupId(para['deviceids'], grpid)
        return grp_mdl
    except Exception:
        rg_lib.Cyclone.HandleErrInException()


def __convert_command(arg):
    if arg['is_binary']:
        command = rg_lib.String.BinaryTextToBytes(arg['command'])
    if arg['is_passthrough']:
        command = rggw_lib.Command.S15(rggw_lib.Consts.DEF_PWD,
                                        1 if arg['is_binary'] else 2, command)
    return command


async def SendCommand(req_handler, sessionid, para):
    """
    :param req_handler:
    :param sessionid:
    :param para: {'trackerid': tracker id, "is_binary": true or false, "is_passthrough": true or false, "command": string}
    :return:
    """
    try:
        await api_core.ReqLimit.CheckMinuteRate("SendCommand", rg_lib.Cyclone.TryGetRealIp(req_handler), 3)
        await api_core.Login.CheckRight(sessionid, (rgv_consts.UserNo.ROOT,))
        await api_core.RGGW.TwoWayCommand(models.TrackerCommand.make(para['trackerid'],
                                                                     __convert_command(para)))
        return "ok"
    except Exception:
        rg_lib.Cyclone.HandleErrInException()


async def SendRelay(req_handler, sessionid, arg):
    """
    :param req_handler:
    :param sessionid:
    :param arg: {"trackerid": "", "relayid": relay id, "on_off" 1 or 2}
    :return:
    """
    try:
        await api_core.ReqLimit.CheckMinuteRate("SendRelay", rg_lib.Cyclone.TryGetRealIp(req_handler), 5)
        await api_core.Login.CheckRight(sessionid, (rgv_consts.UserNo.ROOT,))
        command = models.Command.make(arg['trackerid'],
                                      rggw_lib.Command.S10(rggw_lib.Consts.DEF_PWD, arg['relayid'], arg['on_off']),
                                      False, False)
        await api_core.RGGW.TwoWayCommand(models.TrackerCommand.make(arg['trackerid'],
                                                                     __convert_command(command)))
        return "ok"
    except Exception:
        rg_lib.Cyclone.HandleErrInException()


async def SetEEPROM(req_handler, sessionid, arg):
    """
    :param req_handler:
    :param sessionid:
    :param arg: {"deviceid": string, "start_addr": integer, "ints": [val,]}
    :return:
    """
    try:
        await api_core.ReqLimit.CheckMinuteRate("SetEEPROM", rg_lib.Cyclone.TryGetRealIp(req_handler), 5)
        await api_core.Login.CheckRight(sessionid, (rgv_consts.UserNo.ROOT,))
        device_mdl = await api_core.RGGW.Get(["select ownerid, nid from rgv_rggw where id=?", (arg['deviceid'],)])
        if device_mdl:
            op_str = rggw_lib.Command.S9(rggw_lib.Consts.DEF_PWD, device_mdl['nid'],
                                         arg['start_addr'],
                                         arg['data'])
            log.msg(op_str)
            res = await api_core.RGGW.TwoWayCommand(models.TrackerCommand.make(device_mdl['ownerid'], op_str))
            if res:
                if rggw_lib.IsError(res):
                    raise rg_lib.RGError(models.ErrorTypes.RGGWMsgError())
                else:
                    return "ok"
            else:
                raise rg_lib.RGError(models.ErrorTypes.OpFail())
        else:
            raise rg_lib.RGError(models.ErrorTypes.NoSerialDevice())
    except Exception:
        rg_lib.Cyclone.HandleErrInException()


async def GetEEPROM(req_handler, sessionid, arg):
    """
    :param req_handler:
    :param sessionid:
    :param arg: {"deviceid": string, "start_addr": integer, "count": number of bytes}
    :return:
    """
    try:
        await api_core.ReqLimit.CheckMinuteRate("GetEEPROM", rg_lib.Cyclone.TryGetRealIp(req_handler), 5)
        await api_core.Login.CheckRight(sessionid, (rgv_consts.UserNo.ROOT,))
        device_mdl = await api_core.RGGW.Get(["select ownerid, nid from rgv_rggw where id=?",
                                              (arg['deviceid'],)])
        if device_mdl:
            op_str = rggw_lib.Command.G5(rggw_lib.Consts.DEF_PWD, device_mdl['nid'],
                                          arg['start_addr'], arg['count'] if arg['count'] > 1 else 1)
            res = await api_core.RGGW.TwoWayCommand(models.TrackerCommand.make(device_mdl['ownerid'], op_str))
            if rggw_lib.IsError(res):
                raise rg_lib.RGError(models.ErrorTypes.RGGWMsgError())
            else:
                return res
        else:
            raise rg_lib.RGError(models.ErrorTypes.NoSerialDevice())
    except Exception:
        rg_lib.Cyclone.HandleErrInException()


async def GetRecentTrackerRawLog(req_handler, sessionid, trackerid, count):
    try:
        await api_core.ReqLimit.CheckMinuteRate("GetRecentTrackerRawLog", rg_lib.Cyclone.TryGetRealIp(req_handler), 3)
        await api_core.Login.CheckRight(sessionid, (rgv_consts.UserNo.ROOT,))
        result = await api_core.RGGWRawData.GetLatest(trackerid, count)
        return [models.RGGWRawData.tojson(i) for i in result]
    except Exception:
        rg_lib.Cyclone.HandleErrInException()


async def FindTrackerRawLog(req_handler, sessionid, arg):
    """
    :param req_handler:
    :param sessionid:
    :param arg: {"trackerid": trackerid, "start_ts": start timestamp, "stop_ts": stop timestamp}
    :return:
    """
    try:
        await api_core.ReqLimit.CheckMinuteRate("FindTrackerRawLog", rg_lib.Cyclone.TryGetRealIp(req_handler), 3)
        await api_core.Login.CheckRight(sessionid, (rgv_consts.UserNo.ROOT,))
        result = await api_core.RGGWRawData.RangeQuery(arg['trackerid'], arg['start_ts'], arg['stop_ts'], 10000)
        return [models.RGGWRawData.tojson(i) for i in result]
    except Exception:
        rg_lib.Cyclone.HandleErrInException()


async def GetRecentQ06(req_handler, sessionid, arg):
    """
    :param req_handler:
    :param sessionid:
    :param arg: {"trackerid": trackerid, "count": count}
    :return:
    """
    try:
        await api_core.ReqLimit.CheckMinuteRate("GetRecentQ06", rg_lib.Cyclone.TryGetRealIp(req_handler), 3)
        await api_core.Login.CheckRight(sessionid, (rgv_consts.UserNo.ROOT,))
        return await api_core.RGGWMsg.GetRecentQ06(rg_lib.DateTime.utc(), arg['trackerid'], arg['count'])
    except Exception:
        rg_lib.Cyclone.HandleErrInException()


async def FindQ06(req_handler, sessionid, arg):
    """
    :param req_handler:
    :param sessionid:
    :param arg: {"trackerid": trackerid, "start_ts": start timestamp, "stop_ts": stop timestamp}
    :return:
    """
    try:
        await api_core.ReqLimit.CheckMinuteRate("FindQ06", rg_lib.Cyclone.TryGetRealIp(req_handler), 3)
        await api_core.Login.CheckRight(sessionid, (rgv_consts.UserNo.ROOT,))
        return await api_core.RGGWMsg.RangeQueryQ06(arg['trackerid'], arg['start_ts'], arg['stop_ts'], 10000)
    except Exception:
        rg_lib.Cyclone.HandleErrInException()
