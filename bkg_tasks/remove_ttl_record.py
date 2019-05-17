from twisted.python import log
import api_core
import rg_lib
import settings


async def RemoveTtlRecord():
    try:
        curr_ts = rg_lib.DateTime.ts()
        await api_core.RGGWRawData.RemoveTtl(curr_ts - settings.LOG_DB['ttl'])
        await api_core.RGGWMsg.RemoveTTL(curr_ts - settings.LOG_DB['ttl'])
        await api_core.SensorData.RemoveTTL(curr_ts - settings.LOG_DB['ttl'])
        await api_core.SwitchSchedule.RemoveTTL(curr_ts - 3600)  # keep 60 minutes data only
    except Exception:
        log.err()



