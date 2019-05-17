from twisted.internet import defer
from twisted.python import log
import api_core
import rg_lib
from bkg_tasks import handle_switch_action
from bkg_tasks import handle_switch_schedule
from bkg_tasks import remove_ttl_record


async def DoSwitchAction():
    try:
        curr = rg_lib.DateTime.utc()
        actions = await api_core.SwitchAction.GetValidDueActions(curr)
        defer_objs = []
        for action_mdl in actions:
            d_obj = defer.ensureDeferred(handle_switch_action.RunTask(action_mdl, curr))
            defer_objs.append(d_obj)
        for d_obj in defer_objs:
            try:
                await d_obj
            except rg_lib.RGError:
                pass
        failed_actions = await api_core.SwitchAction.GetOverdueActions(curr)
        if len(failed_actions) > 0:
            await api_core.SwitchAction.Remove([r['actionid'] for r in failed_actions])
    except Exception:
        log.err()


async def DoSwitchSchedule():
    try:
        curr = rg_lib.DateTime.utc()
        schedules = await api_core.SwitchSchedule.GetDueSchedules(curr)
        defer_objs = []
        for schedule_mdl in schedules:
            d_obj = defer.ensureDeferred(handle_switch_schedule.RunTask(schedule_mdl, curr))
            defer_objs.append(d_obj)
        for d_obj in defer_objs:
            try:
                await d_obj
            except rg_lib.RGError:
                pass
    except Exception:
        log.err()


async def RemoveTtlRecord():
    try:
        await remove_ttl_record.RemoveTtlRecord()
    except Exception:
        log.err()



