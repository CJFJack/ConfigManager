from jenkinsapi.jenkins import Jenkins


def get_Jenkins_Job_List(url, jobName, username=None, password=None):
    J = Jenkins(url, username, password)
    jobs = J.keys()
    return jobs


def getSCMInfroFromLatestGoodBuild(url, jobName, username=None, password=None):
    J = Jenkins(url, username, password)
    job = J[jobName]
    lgb = job.get_last_good_build()
    return lgb.get_number()


if __name__ == '__main__':
    print get_Jenkins_Job_List('http://jenkins.dev.com', 'test-hotel-third-hotelsuppliers', 'jack', 'cjf123')
    print getSCMInfroFromLatestGoodBuild('http://jenkins.dev.com', 'test-hotel-third-hotelsuppliers', 'jack', 'cjf123')