from twisted.internet import defer
from twisted.python import log
import api_core
import rg_lib


async def SetCfg(req_handler, para):
    """
    :param req_handler:
    :param para: {"cfg": {}, "token"}
    :return:
    """
    try:
        await api_core.ReqLimit.CheckMinuteRate("SetCfg", rg_lib.Cyclone.TryGetRealIp(req_handler))
        await api_core.Login.HasTenant(para['token'])
        await api_core.SysCfg.Set(para['cfg'])
        return "ok"
    except Exception:
        rg_lib.Cyclone.HandleErrInException()


async def GetCfg(req_handler, para):
    """
    :param req_handler:
    :param para: {token}
    :return:
    """
    try:
        await api_core.ReqLimit.CheckMinuteRate("GetCfg", rg_lib.Cyclone.TryGetRealIp(req_handler))
        await api_core.Login.HasTenant(para['token'])
        return await api_core.SysCfg.Get(["select * from rgv_sys_cfg", tuple()])
    except Exception:
        rg_lib.Cyclone.HandleErrInException()

