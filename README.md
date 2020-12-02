# OpenShift Python Crash Me

This repository provides a sample Python web application implemented using the Flask web framework. It is intended to be used to demonstrate deployment of Python web applications to OpenShift 3 or 4.

Original code from: https://github.com/OpenShiftDemos/os-sample-python

## Modifications

This sample has been modified to be a sample Python application with Kubernetes Liveness and Readiness probes.


## Deployment Steps

To deploy this sample Python web application from the OpenShift use the provided template.

Template parameters can be found here.  https://github.com/themoosman/ocp-python-crash-me/blob/master/.ocp/deployment.yaml#L155-L176


### The OCP Template Way
```
#Create the DEV project
oc new-project python-crash-me-dev

#To deploy the build components
oc process -f build.yaml -p NAMESPACE=python-crash-me-dev | oc create -f -

#Create the DEV deployment resources
oc process -f deployment.yaml -p NAMESPACE=python-crash-me-dev -p IMAGE_NAMESPACE=py-crash-me-dev -p ENVIRONMENT=dev | oc create -f -

#Start the build
oc start-build python-crash-me

#Rollout out the deployment
oc rollout latest dc/python-crash-me

#To simulate a rollout to QA
oc new-project python-crash-me-qa

#Create the QA deployment resources
oc process -f deployment.yaml -p NAMESPACE=python-crash-me-qa -p IMAGE_NAMESPACE=py-crash-me-dev -p ENVIRONMENT=qa | oc create -f -

#Tag the images from DEV to QA
oc tag python-crash-me-dev/py-crash-me:latest py-crash-me-qa/py-crash-me:latest

#Rollout to QA
oc rollout latest dc/python-crash-me

```

### The Helm Way
```
#Create the DEV project
oc new-project python-crash-me-dev

#To deploy the build and deployment components
helm install python-crash-me .helm/python-crash-me/ --namespace python-crash-me-dev --values .helm/python-crash-me/values.yaml

#Start the build
oc start-build python-crash-me

#Rollout out the deployment
oc rollout latest dc/python-crash-me

#To simulate a rollout to QA
oc new-project python-crash-me-qa

#Create the QA deployment resources
helm install python-crash-me .helm/python-crash-me/ --namespace python-crash-me-qa --values .helm/python-crash-me/values-qa.yaml

#Tag the images from DEV to QA
oc tag python-crash-me-dev/python-crash-me:latest python-crash-me-qa/python-crash-me:latest

#Rollout to QA
oc rollout latest dc/python-crash-me

```