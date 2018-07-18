#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.test import TestCase

# Create your tests here.

from acs_slb_backendserver_add import add_backendserver
LoadBalancerId = '155a56d1c0a-cn-hangzhou-dg-a01'
BackendServers = "[{u'ServerId':u'AY1407121019172066ee',u'Weight':u'100'}]"
result = add_backendserver(LoadBalancerId=LoadBalancerId, BackendServers=BackendServers)
print result
