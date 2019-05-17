from twisted.python import log
import rg_lib
import rggw_lib


class TcpHandler(rggw_lib.ConnBase):
    def connectionMade(self):
        rggw_lib.ConnBase.connectionMade(self)
        log.msg("echo connected")

    def dataReceived(self, data):
        self.curr_time = rg_lib.DateTime.utc()
        log.msg("get %d bytes %s" % (len(data), rg_lib.String.PrettyBinary(data)))
        self.transport.write(data)

    def connectionLost(self, reason):
        rggw_lib.ConnBase.connectionLost(self, reason)
        log.msg("echo conn lost")

