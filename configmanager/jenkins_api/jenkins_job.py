from jenkinsapi.jenkins import Jenkins
from jenkinsapi.build import Build


def get_Jenkins_Job_List(url, username=None, password=None):
    J = Jenkins(url, username, password)
    jobs = J.keys()
    return jobs


def getSCMInfroFromLatestGoodBuild(url, jobName, username=None, password=None):
    J = Jenkins(url, username, password)
    job = J[jobName]
    try:
        lgb = job.get_last_good_build().get_number()
    except:
        lgb = 0
    return lgb


def build_job(url, job, username=None, password=None):
    J = Jenkins(url, username, password)
    result = J.build_job(job)
    queue_info = J.get_queue_info()
    print queue_info
    return result


if __name__ == '__main__':
    print get_Jenkins_Job_List('http://jenkins.dev.com', 'jack', 'cjf123')
    print getSCMInfroFromLatestGoodBuild('http://jenkins.dev.com', 'dev3-email-rpc-build', 'jack', 'cjf123')
    print build_job('http://jenkins.dev.com', 'dev3-email-rpc-build', 'jack', 'cjf123')