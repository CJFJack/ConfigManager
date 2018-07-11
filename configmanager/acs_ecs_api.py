#!/usr/bin/env python
#coding=utf-8

from aliyunsdkcore import client
from aliyunsdkcms.request.v20180308 import QueryMetricLastRequest
from datetime import datetime, timedelta
import json

clt = client.AcsClient('LTAI8oND4553ucVr','0zI2YXs2LKKPT57e7P4qVQ4Nzo1BhD','cn-hangzhou')
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
    dict=json.loads(response)
    data=dict['Datapoints'].encode('utf-8')
    ecs_info=json.loads(data)[0]
    return ecs_info

# 调用函数
if __name__=='__main__':
    result=query_ecs_api(instanceid="AY1407121019172066ee", metric="cpu_total")
    print result


