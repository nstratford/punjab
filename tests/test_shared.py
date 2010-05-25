
from twisted.internet import defer, reactor

from twisted.python import log


import test_basic

class SharedTestCase(test_basic.TestCase):
    """Shared BOSH tests
    """


    @defer.inlineCallbacks
    def testCreateShareSession(self):
        """
        """
        BOSH_XML = """<body content='text/xml; charset=utf-8'
      hold='1'
      rid='1573741820'
      to='localhost'
      secure='true'
      ver='1.6'
      wait='60'
      ack='1'
      xmlns:shared='urn:xmpp:tmp:shared-bosh:0'
      shared:key='3c1d69981b65bfbd641dcb64c82bb613'
      xml:lang='en'
      xmlns='http://jabber.org/protocol/httpbind'/>
 """

        res = yield self.proxy.connect(BOSH_XML)
        
        self.failUnless(res[0].name=='body', 'Wrong element')            
        self.failUnless(res[0].hasAttribute('sid'), 'Not session id')
        self.failUnless(res[0].getAttribute(('urn:xmpp:tmp:shared-bosh:0', 'result')) == 'created')


    @defer.inlineCallbacks
    def testSessionAttach(self):
        """
        """
        

        BOSH_XML = """<body content='text/xml; charset=utf-8'
      hold='1'
      rid='1573741820'
      to='localhost'
      secure='true'
      ver='1.6'
      wait='60'
      ack='1'
      xmlns:shared='urn:xmpp:tmp:shared-bosh:0'
      shared:key='3c1d69981b65bfbd641dcb64c82bb613'
      xml:lang='en'
      xmlns='http://jabber.org/protocol/httpbind'/>
 """
        
        r = yield self.proxy.connect(BOSH_XML)
        
    
        BOSH_XML = """<body content='text/xml; charset=utf-8'
      hold='1'
      rid='12345'
      to='localhost'
      secure='true'
      ver='1.6'
      wait='60'
      ack='1'
      xmlns:shared='urn:xmpp:tmp:shared-bosh:0'
      shared:key='3c1d69981b65bfbd641dcb64c82bb613'
      xml:lang='en'
      xmlns='http://jabber.org/protocol/httpbind'/>
 """    
        
        

        res = yield self.proxy.connect(BOSH_XML)
        
        self.failUnless(res[0].name=='body', 'Wrong element')            
        self.failUnless(res[0].hasAttribute('sid'), 'Not session id')
        self.failUnless(res[0].getAttribute(('urn:xmpp:tmp:shared-bosh:0', 'result')) == 'attached')



    @defer.inlineCallbacks
    def testSessionRID(self):
        """
        """
        

        BOSH_XML = """<body content='text/xml; charset=utf-8'
      hold='1'
      rid='1573741820'
      to='localhost'
      secure='true'
      ver='1.6'
      wait='3'
      ack='1'
      xmlns:shared='urn:xmpp:tmp:shared-bosh:0'
      shared:key='3c1d69981b65bfbd641dcb64c82bb613'
      xml:lang='en'
      xmlns='http://jabber.org/protocol/httpbind'/>
 """
        
        r = yield self.proxy.connect(BOSH_XML)
        
    
        BOSH_XML = """<body content='text/xml; charset=utf-8'
      hold='1'
      rid='%d'
      to='localhost'
      secure='true'
      ver='1.6'
      wait='3'
      ack='1'
      xmlns:shared='urn:xmpp:tmp:shared-bosh:0'
      shared:key='3c1d69981b65bfbd641dcb64c82bb613'
      xml:lang='en'
      xmlns='http://jabber.org/protocol/httpbind'/>
 """    
        
        

        res = yield self.proxy.connect(BOSH_XML % (self.rid, ))
        
        self.failUnless(res[0].name=='body', 'Wrong element')            
        self.failUnless(res[0].hasAttribute('sid'), 'Not session id')
        self.failUnless(res[0].getAttribute(('urn:xmpp:tmp:shared-bosh:0', 'result')) == 'attached')

        self.server_factory.protocol.delay_features = 5

        sid = res[0]['sid']
        rid = self.rid
        reactor.callLater(2, self.server_protocol.triggerChallenge)
        for i in range(6):
            res = yield self.send("<auth xmlns='urn:ietf:params:xml:ns:xmpp-sasl' mechanism='DIGEST-MD5'/>", sid=sid, rid=rid+i)
            self.failUnless(res[0].name=='body', 'Wrong element')            
