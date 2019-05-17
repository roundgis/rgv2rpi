import os.path as os_path
from twisted.internet import reactor, defer
from twisted.python import log, logfile
import rgv_consts
import echo_handler
import rgv_beat
import rggw_handler
import handle_rggw_msg
import web_app
import rggw_lib
import api_core
import settings


def InitWebService():
    reactor.listenTCP(settings.HTTP_PORT, web_app.App(settings.WEB['static_path'],
                                                      settings.WEB['export_path']))


def InitRGGW(listen_port):
    factory = rggw_lib.ConnFactory(protoid=rgv_consts.GWProtocolIds.RGGW)
    factory.port = listen_port
    factory.protocol = rggw_handler.WL_TcpHandler
    factory.conn_timeout = 240
    rggw_lib.FactoryAPI.Add(factory)
    try:
        reactor.listenTCP(listen_port, factory)
        reactor.callLater(1, lambda: defer.ensureDeferred(handle_rggw_msg.PollMsg()))
    except Exception:
        log.err()


def InitEcho(listen_port):
    factory = rggw_lib.ConnFactory(protoid=rgv_consts.GWProtocolIds.ECHO)
    factory.port = listen_port
    factory.conn_timeout = 240
    factory.protocol = echo_handler.TcpHandler
    rggw_lib.FactoryAPI.Add(factory)
    try:
        reactor.listenTCP(listen_port, factory)
    except Exception:
        log.err()


def InitGatewayNode():
    InitRGGW(settings.GW_PORT)
    InitEcho(settings.GW_ECHO_PORT)


def UpdateConsts():
    for k in rgv_consts.URLs.__dict__:
        if k.find('__') < 0:
            if k not in ('EXPORT_FMT', 'INDEX'):
                setattr(rgv_consts.URLs, k,
                        os_path.join(settings.URL_PREFIX, rgv_consts.URLs.__dict__[k]))

    for k in rgv_consts.Keys.__dict__:
        if k.find('__') < 0:
            temp = os_path.join(settings.URL_PREFIX, rgv_consts.Keys.__dict__[k])
            setattr(rgv_consts.Keys, k, temp.replace('/', '_'))

    for k in rgv_consts.Cookies.__dict__:
        if k.find('__') < 0:
            temp = os_path.join(settings.URL_PREFIX, rgv_consts.Cookies.__dict__[k])
            setattr(rgv_consts.Cookies, k, temp.replace('/', '_'))


async def Init():
    await api_core.BizDB.Init()
    await api_core.LogDB.Init()
    rgv_beat.Start()
    InitWebService()
    reactor.callLater(0.5, InitGatewayNode)


def main():
    try:
        UpdateConsts()
        log.startLogging(logfile.DailyLogFile.fromFullPath(settings.LOG_PATH + "/" +
                                                           "rgv" +''.join([i for i in settings.HOST if i != '.']) + "_log.txt"),
                         setStdout=False)
        reactor.callLater(1, defer.ensureDeferred, Init())
        reactor.addSystemEventTrigger('before', 'shutdown', api_core.BizDB.Close)
        reactor.addSystemEventTrigger('before', 'shutdown', api_core.LogDB.Close)
        reactor.addSystemEventTrigger('before', 'shutdown', rgv_beat.Close)
        reactor.run()
    except Exception:
        log.err()


if __name__ == "__main__":
    main()

