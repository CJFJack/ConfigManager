#!/usr/bin/env python
#coding=utf-8

from aliyunsdkcore import client
from aliyunsdkslb.request.v20140515 import DescribeLoadBalancersRequest
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

def query_slb_info(regionid):
    # 设置参数
    request = DescribeLoadBalancersRequest.DescribeLoadBalancersRequest()
    request.set_accept_format('json')
    
    request.add_query_param('RegionId', 'cn-hangzhou')
    
    # 发起请求
    response = clt.do_action(request)
    LoadBalancers = json.loads(response)['LoadBalancers'] 
    LoadBalancer = LoadBalancers['LoadBalancer']
    slblist = []
    for slb in LoadBalancer:
        LoadBalancerId = slb['LoadBalancerId']
        try:
            LoadBalancerName = slb['LoadBalancerName']
        except:
            LoadBalancerName = ''
        try:
            NetworkType = slb['NetworkType']
        except:
            NetworkType = ''
        LoadBalancerStatus = slb['LoadBalancerStatus']
        Address = slb['Address']
        AddressType = slb['AddressType']
        CreateTime = slb['CreateTime']
        slbdict={}
        slbdict['LoadBalancerId'] = LoadBalancerId
        slbdict['LoadBalancerName'] = LoadBalancerName
        slbdict['LoadBalancerStatus'] = LoadBalancerStatus
        slbdict['Address'] = Address
        slbdict['AddressType'] = AddressType
        slbdict['CreateTime'] = CreateTime
        slbdict['NetworkType'] = NetworkType
        slblist.append(slbdict)
    return slblist


if __name__=='__main__':
    slbinfo = query_slb_info(regionid='cn-hangzhou')
    print slbinfo

