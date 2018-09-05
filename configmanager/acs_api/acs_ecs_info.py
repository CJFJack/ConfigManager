#!/usr/bin/env python
#coding=utf-8

from aliyunsdkcore import client
from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest
import json, os
from django.conf import settings

AccessKeyId = settings.ACCESS_KEY_ID
AccessKeySecret = settings.ACCESS_KEY_SECRET
clt = client.AcsClient(AccessKeyId, AccessKeySecret, 'cn-hangzhou')


def query_ecs_info(instanceids):
    # 设置参数
    request = DescribeInstancesRequest.DescribeInstancesRequest()
    request.set_accept_format('json')
    request.add_query_param('RegionId', 'cn-hangzhou')
    request.add_query_param('InstanceIds', instanceids)

    # 发起请求
    response = clt.do_action(request)
    json_response = json.loads(response)
    print json_response
    
    # 获取实例区域
    RegionId = json_response['Instances']['Instance'][0]['RegionId']
    # 获取过期时间
    ExpiredTime = json_response['Instances']['Instance'][0]['ExpiredTime']
    # 获取内存大小
    Memory = json_response['Instances']['Instance'][0]['Memory']
    # 获取系统类型
    OSType = json_response['Instances']['Instance'][0]['OSType']
    # 获取实例状态
    Status = json_response['Instances']['Instance'][0]['Status']
    # 获取网络类型
    NetworkType = json_response['Instances']['Instance'][0]['InstanceNetworkType']
    # 获取内网IP
    InnerIpAddress = json_response['Instances']['Instance'][0]['InnerIpAddress']['IpAddress'][0]
    # 获取实例名称
    InstanceName = json_response['Instances']['Instance'][0]['InstanceName']
    # 获取CPU核数
    Cpu = json_response['Instances']['Instance'][0]['Cpu']
    # 获取公网IP
    try:
        PublicIpAddress = json_response['Instances']['Instance'][0]['PublicIpAddress']['IpAddress'][0]
    except:
        PublicIpAddress = ''
    # 获取操作系统版本
    OSName = json_response['Instances']['Instance'][0]['OSName']

    # 存入字典
    dict = {}
    dict['RegionId'] = RegionId
    dict['ExpiredTime'] = ExpiredTime.replace("Z", "").replace("T", " ")
    dict['Memory'] = Memory
    dict['OSType'] = OSType
    dict['Status'] = Status
    dict['NetworkType'] = NetworkType
    dict['InnerIpAddress'] = InnerIpAddress
    dict['InstanceName'] = InstanceName
    dict['Cpu'] = Cpu
    dict['PublicIpAddress'] = PublicIpAddress
    dict['OSName'] = OSName
    
    return dict
    
    
# 调用函数
if __name__=='__main__':
    result = query_ecs_info(instanceids=["AY140507114807874a62"])
    print result
