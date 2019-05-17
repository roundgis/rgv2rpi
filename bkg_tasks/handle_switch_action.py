from twisted.python import log
import api_core
import models


async def RunTask(action_mdl, dt_obj):
    if action_mdl['action_no'] == models.SwitchAction.ON:
        op_succ = await api_core.SwitchAction.HandleActionOn(action_mdl, dt_obj)
    elif action_mdl['action_no'] == models.SwitchAction.OFF:
        op_succ = await api_core.SwitchAction.HandleActionOff(action_mdl, dt_obj)
    else:
        raise ValueError("incorrect action no.")
    if not op_succ:
        await api_core.SwitchAction.HandleRetries(action_mdl)

