# OpenShift Python Crash Me

This repository provides a sample Python web application implemented using the Flask web framework and hosted using `gunicorn`. It is intended to be used to demonstrate deployment of Python web applications to OpenShift 3 or 4.

Original code from: https://github.com/OpenShiftDemos/os-sample-python

## Modifications

This sample has been modified to be a sample Python application with Kubernetes Liveness and Readiness probes.


## Deployment Steps

To deploy this sample Python web application from the OpenShift use the provided template.

Template parameters can be found here.  https://github.com/themoosman/ocp-python-crash-me/blob/master/ocp/deployment.yaml#L155-L176

```
#Create the DEV project
oc new-project py-crash-me-dev

#To deploy the build components
oc process -f build.yaml -p NAMESPACE=py-crash-me-dev | oc create -f -

#Create the DEV deployment resources
oc process -f deployment.yaml -p NAMESPACE=py-crash-me-dev -p IMAGE_NAMESPACE=py-crash-me-dev | oc create -f -

#Start the build
oc start-build py-crash-me

#Rollout out the deployment
oc rollout latest dc/py-crash-me

#To simulate a rollout to QA
oc new-project py-crash-me-qa

#Create the QA deployment resources
oc process -f deployment.yaml -p NAMESPACE=py-crash-me-qa -p IMAGE_NAMESPACE=py-crash-me-dev | oc create -f -

#Tag the images from DEV to QA
oc tag py-crash-me-dev/py-crash-me:latest py-crash-me-qa/py-crash-me:latest

#Rollout to QA
oc rollout latest dc/py-crash-me

```
