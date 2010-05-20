
import os
import sys, sha, random
from twisted.trial import unittest
import time
from twisted.web import server, resource, static, http, client
from twisted.words.protocols.jabber import jid
from twisted.internet import defer, protocol, reactor
from twisted.application import internet, service
from twisted.words.xish import domish, xpath

from twisted.python import log

from punjab.httpb import HttpbService
from punjab.xmpp import server as xmppserver
from punjab import httpb_client

import test_basic

class SharedTestCase(test_basic.TestCase):
    """Shared BOSH tests
    """


    def testShareSession(self):
        """
        """
        
        def _testSessionCreate(res):
            self.failUnless(res[0].name=='body', 'Wrong element')            
            self.failUnless(res[0].hasAttribute('sid'), 'Not session id')
            self.failUnless(res[0].getAttribute('shared:result') == 'created')
            
        def _error(e):
            # This fails on DNS 
            log.err(e)
            

        BOSH_XML = """<body content='text/xml; charset=utf-8'
      hold='1'
      rid='1573741820'
      to='localhost'
      secure='true'
      ver='1.6'
      wait='60'
      ack='1'
      shared:key='3c1d69981b65bfbd641dcb64c82bb613'
      xmlns:shared='urn:xmpp:tmp:shared-bosh:0'
      xml:lang='en'
      xmlns='http://jabber.org/protocol/httpbind'/>
 """

        d = self.proxy.connect(BOSH_XML).addCallback(_testSessionCreate)
        d.addErrback(_error)
        return d


