from twisted.internet import defer
from twisted.internet import reactor
from twisted.python import log
import rgv_consts
import rg_lib
import rggw_lib
import api_core
import handle_rggw_msg


class TcpHandler(rggw_lib.ConnBase):
    def dataReceived(self, data):
        self.curr_time = rg_lib.DateTime.utc()
        try:
            parser = rggw_lib.Parser(data)
            parser.Parse()
            self.AfterParse(parser)
        except Exception:
            log.err()

    def HandleAck_(self, msgs):
        needv, need_alarm = False, False
        t76 = b''
        for item in msgs:
            if rggw_lib.IsQ06(item):
                t76 = rggw_lib.Command.T76V2(self.curr_time, item['payload']['count'])
            elif rggw_lib.IsV(item):
                needv = True
        if t76 != b'':
            self.transport.write(t76)
        bytes_objs = []
        if needv:
            bytes_objs.append(rggw_lib.Consts.RESPONSE_V)
        if need_alarm:
            bytes_objs.append(rggw_lib.Consts.RESPONSE_ALARM)
        if bytes_objs:
            reactor.callLater(0.5, self.transport.write, b'\r\n'.join(bytes_objs))

    def AfterParse(self, parser):
        """
        :param parser:  rggwlib.Parser
        :return:
        """
        raise NotImplementedError()


class WL_TcpHandler(TcpHandler):
    def AssignTrackerId(self, gw_msg):
        if gw_msg['index']['type_no'] in ('#GET', '#SET'):
            gw_msg['index']['trackerid'] = self.trackerid

    @defer.inlineCallbacks
    def AfterParse(self, parser):
        msgs = parser.GetMsgs()
        if self.trackerid:
            yield defer.ensureDeferred(api_core.RGGWRawData.Add(self.curr_time, self.trackerid,
                                                                rgv_consts.TrackerDataNo.IN,
                                                                parser.bytes_obj))
        if len(msgs) > 0:
            self.resetTimeout()
            if parser.trackerid:
                self.trackerid = parser.trackerid
            self.factory.SetConn(self.trackerid, self)
            for item in msgs:
                self.AssignTrackerId(item)
            self.HandleAck_(msgs)
            handle_rggw_msg.AddMsgs(msgs)


