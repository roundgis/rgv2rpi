from twisted.python import log
import api_core
import models
import rg_lib


def RunTask(schedule_mdl, dt_obj):
    return MakeAction(schedule_mdl, dt_obj)


async def MakeAction(schedule_mdl, dt_obj):
    sql_str = rg_lib.Sqlite.GenInSql("select id,ownerid from rgv_switch where id in ", schedule_mdl['switchids'])
    switches = await api_core.BizDB.Query([sql_str, schedule_mdl['switchids']])
    tbl = models.Switch.PivotTbls(switches)
    for devid in tbl:
        if len(tbl[devid]) > 0:
            new_actionid = models.SwitchAction.GenId()
            action_mdls = []
            for switch in tbl[devid]:
                action_mdl = models.SwitchAction.make(switch['id'], new_actionid,
                                                      devid, schedule_mdl['id'],
                                                      models.SwitchAction.ON,
                                                      rg_lib.DateTime.dt2ts(dt_obj),
                                                      rg_lib.DateTime.dt2ts(dt_obj) + schedule_mdl['working_seconds'])
                action_mdls.append(action_mdl)
            await api_core.SwitchAction.Add(action_mdls)
    ts_tbl = models.SwitchSchedule.ComputeNextRunTs(schedule_mdl)
    sql_row = models.SwitchSchedule.PartialUpdate(ts_tbl, ['id'])
    sql_row[0] += "id=?"
    sql_row[1].append(schedule_mdl['id'])
    return await api_core.BizDB.Interaction([sql_row])

