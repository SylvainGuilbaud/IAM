# export ISC_IAM_IMAGE=intersystems/iam:2.8.1.0-3
# export ISC_IRIS_URL=http://IAM:SYS@169.254.24.225:52773/api/iam/license

export ISC_IRIS_HOSTNAME=`hostname`
export ISC_IRIS_HOSTNAME=192.168.65.1
export ISC_IRIS_HOSTNAME=127.0.0.1
export ISC_IRIS_HOSTNAME=localhost
export ISC_IRIS_HOSTNAME=172.24.159.201
export ISC_IRIS_PORT=9092
export ISC_IRIS_PORT=9093
# export ISC_IRIS_PORT=80
export ISC_IRIS_USERNAME=IAM
export ISC_IRIS_PASSWORD=AAA
# export ISC_IRIS_PASSWORD=IAM
export ISC_IRIS_PREFIX=/iris

# export ISC_IAM_IMAGE=localhost/intersystems/iam-arm64:3.4
export ISC_IAM_IMAGE=localhost/intersystems/iam-arm64:3.10.0.2-15852

export ISC_IRIS_URL=http://${ISC_IRIS_USERNAME}:${ISC_IRIS_PASSWORD}@${ISC_IRIS_HOSTNAME}:${ISC_IRIS_PORT}/api/iam/license

# export ISC_IRIS_URL=http://${ISC_IRIS_USERNAME}:${ISC_IRIS_PASSWORD}@${ISC_IRIS_HOSTNAME}:${ISC_IRIS_PORT}${ISC_IRIS_PREFIX}/api/iam/license