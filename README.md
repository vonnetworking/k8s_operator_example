# Dev Setup

1. install python
2. install kubectl
3. install minikube
4. install make
5. install jenkins and get an instance running
6. setup a jenkins job at devops/caller_test that takes 2 string params msg and msg2
7. export 3 vars JENKINS_URL, JENKINS_USER, JENKINS_PASSWORD (obviously set them to values that will allow login to your local jenkins instance and run the sample job)
8. setup a virtual env
9. pip install -r requirements.txt
10. make create_dev_env - this does a lot of stuff
11. start the controller attached to the local minikube cluster "kopf run --verbose jenkins_caller_operator.py"
12. create the object - "kubectl apply -f test/k8s_obj/test_jenkins_caller_obj.yml" 
13. your jenkins job should kick off and there should be a new config map in the namespace "kubectl get configmaps -A" containing info about the jenkins job run.
