#!/usr/bin/env python
#coding=utf-8

from aliyunsdkcore import client
from aliyunsdkcms.request.v20180308 import QueryMetricLastRequest


clt = client.AcsClient('ZAL5Z3Ee8KhyZ2U1', 'afp7C6u1osEpCZSwVHcHkfcpJqoeEe', 'cn-hangzhou')

def query_rds_monitor(instanceId):
    # 设置参数
    request = QueryMetricLastRequest.QueryMetricLastRequest()
    request.set_accept_format('json')

    request.add_query_param('Project', 'acs_rds_dashboard')
    request.add_query_param('Metric', 'CpuUsage')
    request.add_query_param('Dimensions', {'instanceId':instanceId})
    request.add_query_param('Period', '300')

    # 发起请求
    response = clt.do_action(request)
    return response


# 调用函数
if __name__=='__main__':
    result = query_rds_monitor(instanceId="rdsmaqvrzazju6n")
    print result