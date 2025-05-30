# export ISC_IAM_IMAGE=intersystems/iam:2.8.1.0-3
# export ISC_IRIS_URL=http://IAM:SYS@169.254.24.225:52773/api/iam/license

export ISC_IRIS_HOSTNAME=`hostname`
# export ISC_IRIS_HOSTNAME=192.168.65.1
export ISC_IRIS_PORT=9092
export ISC_IRIS_USERNAME=IAM
export ISC_IRIS_PASSWORD=AAA

export ISC_IAM_IMAGE=localhost/intersystems/iam-arm64:3.4

export ISC_IRIS_URL=http://${ISC_IRIS_USERNAME}:${ISC_IRIS_PASSWORD}@${ISC_IRIS_HOSTNAME}:${ISC_IRIS_PORT}/api/iam/license
