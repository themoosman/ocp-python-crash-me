# OpenShift Python Crash Me

This repository provides a sample Python web application implemented using the Flask web framework and hosted using ``gunicorn``. It is intended to be used to demonstrate deployment of Python web applications to OpenShift 3.

Original code from: https://github.com/OpenShiftDemos/os-sample-python

## Modifications

This sample has been modified to be a sample Python application with Kubernetes Liveness and Readiness probes.


## Deployment Steps

To deploy this sample Python web application from the OpenShift use the provided template.

Template parameters can be found here.  https://github.com/themoosman/ocp-python-crash-me/blob/master/ocp/application-template.yaml#L178-L203

```
oc new-project ocp-demo

#To deploy the template using the defaults.
oc process -f application-template.yaml | oc create -f -

#Add any necessary `-p` arguments to the command below
#For example to override the default namespace and Red Hat repository.
oc process -f application-template.yaml -p NAMESPACE=my-demo -p EXTERNAL_IMAGE_REPO_URL=registry.example.com:5000 | oc create -f -

```
