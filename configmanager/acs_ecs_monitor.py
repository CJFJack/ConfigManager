#!/usr/bin/env python
#coding=utf-8

from aliyunsdkcore import client
from aliyunsdkcms.request.v20180308 import QueryMetricLastRequest
from datetime import datetime, timedelta
import json, os
import ConfigParser

# config = ConfigParser.RawConfigParser()
# currentdir = os.path.abspath('.')
# print currentdir
# configFilePath = os.path.join(currentdir, 'configmanager', 'acs_config', 'acs_config.ini')
# print configFilePath
# config.read(configFilePath)
# AccessKeyId = config.get('acs', 'AccessKeyId')
# AccessKeySecret = config.get('acs', 'AccessKeySecret')
# RegionId = config.get('acs', 'RegionId')

clt = client.AcsClient('ZAL5Z3Ee8KhyZ2U1', 'afp7C6u1osEpCZSwVHcHkfcpJqoeEe', 'cn-hangzhou')

now=datetime.now()
starttime=str(now+timedelta(minutes = -5))
endtime=str(now)


def query_ecs_api(instanceid, metric):
    # 设置参数
    request = QueryMetricLastRequest.QueryMetricLastRequest()
    request.set_accept_format('json')
    request.add_query_param('Project', 'acs_ecs_dashboard')
    request.add_query_param('Metric', metric)
    request.add_query_param('Period', '60')
    request.add_query_param('Dimensions', {'instanceId':instanceid})
    request.add_query_param('StartTime', starttime)
    request.add_query_param('EndTime', endtime)
    # 发起请求
    response = clt.do_action(request)
    # json转dict
    ecsdict=json.loads(response)
    #print ecsdict
    #print ecsdict['Datapoints']
    data=ecsdict['Datapoints'].encode('utf-8')
    ecs_info=json.loads(data)[0]
    return ecs_info

# 调用函数
if __name__=='__main__':
    result=query_ecs_api(instanceid="i-bp11iujuip9pks1n1ue4", metric="memory_usedutilization")
    print result


