#!/usr/bin/env python
#coding=utf-8

from aliyunsdkcore import client
from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest

clt = client.AcsClient('LTAISjDUed4nEdBs','BoiXvuZp9Qz2c5tQnFvlrWNgIdmUYo','cn-huhehaote')

# 设置参数
request = DescribeInstancesRequest.DescribeInstancesRequest()
request.set_accept_format('json')

request.add_query_param('RegionId', 'cn-huhehaote')

# 发起请求
response = clt.do_action(request)

print response