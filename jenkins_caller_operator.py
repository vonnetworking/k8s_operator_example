import os
import kopf
import kubernetes
import time
import yaml
import jenkins

JENKINS_URL = os.getenv("JENKINS_URL")
JENKINS_USERNAME = os.getenv("JENKINS_USERNAME")
JENKINS_PASSWORD = os.getenv("JENKINS_PASSWORD`")

class DevOpsJenkins:
    def __init__(self, logger):
        self.jenkins_server = jenkins.Jenkins(JENKINS_URL, username=JENKINS_USERNAME, password=JENKINS_PASSWORD)
        user = self.jenkins_server.get_whoami()
        version = self.jenkins_server.get_version()
        self.logger = logger
        self.logger.info(f"Jenkins Version: {version}")
        self.logger.info(f"Jenkins User: {user['id']}")

    def build_job(self, name, wait=False, parameters=None, token=None):
        next_build_number = self.jenkins_server.get_job_info(name)['nextBuildNumber']
        self.jenkins_server.build_job(name, parameters=parameters, token=token)
        
        while True:
            try:
                build_info = self.jenkins_server.get_build_info(name, next_build_number)
                break
            except:
                pass

        if wait:
            while True:
                time.sleep(20)
                build_info = self.jenkins_server.get_build_info(name, next_build_number)
                if build_info['building'] == False:
                    if build_info['result'] == "SUCCESS":
                        return build_info
                    else:
                        self.logger.error("Resource Failed to build")
                        return build_info
                else:
                    self.logger.info("Waiting for build to complete...")

        return build_info

@kopf.on.create('jenkinscallers')
@kopf.on.update('jenkinscallers')
def create_and_update_fn(spec, status, namespace, logger, **kwargs):
    jobname = spec.get('jobname')
    if not jobname:
        raise kopf.PermanentError(f"Jobname must be supplied in the jobname key under spec")
    params = spec.get('jobparams')
    if not params:
        raise kopf.PermanentError(f"Params must be supplied in the jobparams key under spec")
    appid = spec.get('appid')
    if not appid:
        raise kopf.PermanentError(f"Appid must be supplied in the appid key under spec")
    component = spec.get('component')
    if not component:
        raise kopf.PermanentError(f"component must be supplied in the component key under spec")

    jenkins_conn = DevOpsJenkins(logger)
    logger.info(f"EAF Job: {jobname} called with these params: {params}")
    jenkins_conn.build_job(jobname, parameters=params)

    data = { "metadata": 
                {"name": f"{appid.lower()}-{component.lower()}-config-map"}, 
             "data": {"key": "value"}}
    api = kubernetes.client.CoreV1Api()
    obj = api.create_namespaced_config_map(
        namespace=namespace,
        body=data
    )

    return {"finished": True, "status": "RUNNING", "success": True}