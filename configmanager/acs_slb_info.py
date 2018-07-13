#!/usr/bin/env python
#coding=utf-8

from aliyunsdkcore import client
from aliyunsdkslb.request.v20140515 import DescribeLoadBalancersRequest
import json

clt = client.AcsClient('LTAI8oND4553ucVr','0zI2YXs2LKKPT57e7P4qVQ4Nzo1BhD','cn-hangzhou')

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
        slblist.append(slbdict)
    return slblist


if __name__=='__main__':
    slbinfo = query_slb_info(regionid='cn-hangzhou')
    print slbinfo

