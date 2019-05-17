import twisted.internet.threads as threads
from twisted.internet import defer
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers import interval
from apscheduler.triggers.cron import CronTrigger
from twisted.internet import reactor

from bkg_tasks import beat_tasks

scheduler_obj = BackgroundScheduler()


def Start():
    secs1_trigger = interval.IntervalTrigger(seconds=1)
    scheduler_obj.add_job(threads.blockingCallFromThread, secs1_trigger,
                          args=(reactor, lambda: defer.ensureDeferred(beat_tasks.DoSwitchAction())),
                          replace_existing=True, id="do_switch_action")
    scheduler_obj.add_job(threads.blockingCallFromThread, secs1_trigger,
                          args=(reactor, lambda: defer.ensureDeferred(beat_tasks.DoSwitchSchedule())),
                          replace_existing=True, id="do_switch_schedule")

    daily_trigger = CronTrigger(second=1)
    scheduler_obj.add_job(threads.blockingCallFromThread, daily_trigger,
                          args=(reactor, beat_tasks.RemoveTtlRecord),
                          replace_existing=True, id='remove_ttl')

    scheduler_obj.start()


def Close():
    scheduler_obj.shutdown(False)
