#!/usr/bin/env python
#coding=utf-8

from aliyunsdkcore import client
from aliyunsdkslb.request.v20140515 import DescribeHealthStatusRequest
import json

clt = client.AcsClient('LTAI8oND4553ucVr','0zI2YXs2LKKPT57e7P4qVQ4Nzo1BhD','cn-hangzhou')


def query_slb_health(LoadBalancerId):
    # 设置参数
    request = DescribeHealthStatusRequest.DescribeHealthStatusRequest()
    request.set_accept_format('json')
    
    request.add_query_param('RegionId', 'cn-hangzhou')
    request.add_query_param('LoadBalancerId', LoadBalancerId)
    
    # 发起请求
    response = clt.do_action(request)
    BackendServers = json.loads(response)['BackendServers']
    BackendServer = BackendServers['BackendServer']
    return BackendServer



if __name__=='__main__':
    result = query_slb_health(LoadBalancerId='155a56d1c0a-cn-hangzhou-dg-a01')
    for r in result:
        print r['ServerId'], r['ServerHealthStatus']
