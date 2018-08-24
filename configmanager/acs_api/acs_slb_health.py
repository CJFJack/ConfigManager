#!/usr/bin/env python
#coding=utf-8

from aliyunsdkcore import client
from aliyunsdkslb.request.v20140515 import DescribeHealthStatusRequest
import json, os
import ConfigParser

# config = ConfigParser.RawConfigParser()
# currentdir = os.path.abspath('.')
# configFilePath = os.path.join(currentdir, 'configmanager', 'acs_config', 'acs_config.ini')
# print configFilePath
# config.read(configFilePath)
# AccessKeyId = config.get('acs', 'AccessKeyId')
# AccessKeySecret = config.get('acs', 'AccessKeySecret')
# RegionId = config.get('acs', 'RegionId')

clt = client.AcsClient('ZAL5Z3Ee8KhyZ2U1', 'afp7C6u1osEpCZSwVHcHkfcpJqoeEe', 'cn-hangzhou')


def query_slb_health(LoadBalancerId):
    # 设置参数
    request = DescribeHealthStatusRequest.DescribeHealthStatusRequest()
    request.set_accept_format('json')
    
    request.add_query_param('RegionId', 'cn-hangzhou')
    request.add_query_param('LoadBalancerId', LoadBalancerId)
    
    # 发起请求
    response = clt.do_action(request)
    if 'Message' in response:
        return json.loads(response)
    else:
        try:
            json.loads(response)['BackendServers']
        except:
            return {'success', 'False'}
        else:
            BackendServers = json.loads(response)['BackendServers']
            BackendServer = BackendServers['BackendServer']
            return BackendServer



if __name__=='__main__':
    result = query_slb_health(LoadBalancerId='155a56d1c0a-cn-hangzhou-dg-a011')
    print result



