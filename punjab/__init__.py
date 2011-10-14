"""
Punjab - multiple http interfaces to jabber.

"""
from OpenSSL import SSL

from twisted.application import service
from twisted.internet import ssl
from twisted.python import log

import patches



# Override DefaultOpenSSLContextFactory to call ctx.use_certificate_chain_file
# instead of ctx.use_certificate_file, to allow certificate chains to be loaded.
class OpenSSLContextFactoryChaining(ssl.DefaultOpenSSLContextFactory):
    def __init__(self, *args, **kwargs):
        ssl.DefaultOpenSSLContextFactory.__init__(self, *args, **kwargs)

    def cacheContext(self):
        ctx = self._contextFactory(self.sslmethod)
        ctx.set_options(SSL.OP_NO_SSLv2)
        ctx.use_certificate_chain_file(self.certificateFileName)
        ctx.use_privatekey_file(self.privateKeyFileName)
        self._context = ctx


def uriCheck(elem, uri):
    """
    This is a hack for older versions of twisted words, we need to get rid of it.
    """
    if str(elem.toXml()).find('xmlns') == -1:
        elem['xmlns'] = uri


class PunjabService(service.MultiService):
    """Punjab parent service"""

    httpb = None

    def startService(self):
        return service.MultiService.startService(self)

    def stopService(self):
        def cb(result):
            return service.MultiService.stopService(self)

        d = self.httpb.stopService()
        d.addCallback(cb).addErrback(log.err)
        return d

class Service(service.Service):
    """
    Punjab generice service
    """
    def error(self, failure, body = None):
        """
        A Punjab error has occurred
        """
        # need a better way to trap this
        if failure.getErrorMessage() != 'remote-stream-error':
            log.msg('Punjab Error: ')
            log.msg(failure.printBriefTraceback())
            log.msg(body)
        failure.raiseException()

    def success(self, result, body = None):
        """
        If success we log it and return result
        """
        log.msg(body)
        return result



def makeService(config):
    """
    Create a punjab service to run
    """
    from twisted.web import  server, resource, static
    from twisted.application import internet

    import httpb

    serviceCollection = PunjabService()

    if config['html_dir']:
        r = static.File(config['html_dir'])
    else:
        print "The html directory is needed."
        return

    if config['redirect']:
        httpb.HttpbService.redirect = config['redirect']

    if config['white_list']:
        httpb.HttpbService.white_list = config['white_list'].split(',')

    if config['black_list']:
        httpb.HttpbService.black_list = config['black_list'].split(',')

    if config['httpb']:
        b = httpb.HttpbService(config['verbose'], config['polling'])
        if config['httpb'] == '':
            r.putChild('http-bind', resource.IResource(b))
        else:
            r.putChild(config['httpb'], resource.IResource(b))

    site  = server.Site(r)

    if config['ssl']:
        ssl_context = OpenSSLContextFactoryChaining(config['ssl_privkey'],
                                                       config['ssl_cert'],
                                                       SSL.SSLv23_METHOD,)
        sm = internet.SSLServer(int(config['port']),
                                site,
                                ssl_context,
                                backlog = int(config['verbose']))
        sm.setServiceParent(serviceCollection)
    else:
        sm = internet.TCPServer(int(config['port']), site)

        sm.setServiceParent(serviceCollection)

    serviceCollection.httpb = b

    return serviceCollection

