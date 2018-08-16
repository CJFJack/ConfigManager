#!/usr/bin/env python
#coding=utf-8

from aliyunsdkcore import client
from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest
import json, os
import ConfigParser

# config = ConfigParser.RawConfigParser()
# currentdir = os.path.abspath('.')
# configFilePath = os.path.join(currentdir, 'configmanager', 'acs_config', 'acs_config.ini')
# config.read(configFilePath)
# AccessKeyId = config.get('acs', 'AccessKeyId')
# AccessKeySecret = config.get('acs', 'AccessKeySecret')
# RegionId = config.get('acs', 'RegionId')
#
# clt = client.AcsClient(AccessKeyId, AccessKeySecret, RegionId)
clt = client.AcsClient('ZAL5Z3Ee8KhyZ2U1', 'afp7C6u1osEpCZSwVHcHkfcpJqoeEe', 'cn-hangzhou')


def query_all_ecs(RegionId):
    # 设置参数
    request = DescribeInstancesRequest.DescribeInstancesRequest()
    request.set_accept_format('json')
    
    request.add_query_param('RegionId', RegionId)
    request.add_query_param('PageSize', 100)
    
    # 发起请求
    response = clt.do_action(request)
    
    data = json.loads(response)
    instances = data['Instances']['Instance']
    list = []
    for instance in instances:
        list.append(instance['InstanceId'])
    return list

# if __name__=='__main__':
#     result = query_all_ecs(RegionId='cn-hangzhou')
#     print result
