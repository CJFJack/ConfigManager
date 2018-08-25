# coding:utf-8

from configmanager.acs_api import acs_rds_info
from configmanager.acs_api import acs_rds_monitor
from .models import RDS, RDS_Usage_Record


def save_rds_info():
    result = acs_rds_info.query_rds_list(RegionId="cn-hangzhou")
    if RDS.objects.filter(instance_id=result['DBInstanceId']).count() == 0:
        rds = RDS(instance_id=result['DBInstanceId'], network_type=result['InstanceNetworkType'], engine=result['Engine'],
                  engine_version=result['EngineVersion'], status=result['DBInstanceStatus'],
                  expire_time=result['ExpireTime'])
        rds.save()


def get_rds_monitor():
    for rds in RDS.objects.all():
        print rds.instance_id
        cpu_usage = acs_rds_monitor.query_rds_monitor(instanceId="rdsmaqvrzazju6n", metric="CpuUsage")
        io_usage = acs_rds_monitor.query_rds_monitor(instanceId="rdsmaqvrzazju6n", metric="IOPSUsage")
        disk_usage = acs_rds_monitor.query_rds_monitor(instanceId="rdsmaqvrzazju6n", metric="DiskUsage")
        print cpu_usage, io_usage, disk_usage
        rds_usage_record = RDS_Usage_Record(cpu_usage=cpu_usage, io_usage=io_usage, disk_usage=disk_usage, rds_id=rds.id)
        rds_usage_record.save()


