FROM python:3.11
ADD ./jenkins_caller_operator.py /src/jenkins_caller_operator.py
RUN pip install kopf python-jenkins requests autogen
CMD kopf run /src/jenkins_caller_operator.py --verbose