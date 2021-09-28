# ShnooTalk Cloud Compile

Backend and infrastructure to compile and execute ShnooTalk programs on the cloud.
Primary use case is for users to try the language in the browser.

The project is made up of two sub-projects, the job and the server. The server
has endpoints to dispatch programs (start compile and run jobs on a kubernetes cluster)
and query status of execution. The job does the actual compilation and execution.

Both the server and the job use MongoDB to keep track of the execution status.

## Running on local for development

+ Install [K3D](https://k3d.io/v4.4.8/) or [Minikube](https://minikube.sigs.k8s.io/docs/start/) or [MicroK8s](https://microk8s.io/)
+ Create a kubernetes cluster
+ Find out your LAN IP address using `ifconfig` or `ipconfig`
+ Deploy the following secret
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: shnootalk-cloud-compile-mongodb-url
type: Opaque
stringData:
  connectionString: mongodb://root:example@<YOUR-LAN-IP>:27017
```
+ Start MongoDB

```
docker-compose -f server/test-services.yml up
```
+ Start server
```
cd server
pipenv shell
pipenv install --dev
KUBE_CONTEXT=<YOUR-CLUSTER> COMPILE_JOB_NAMESPACE=default make rundev
```
+ Dispatch a program by making a POST request
```
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"main.shtk": "fn main() -> int { println(\"Hello world\") return 0 }"}' \
  http://127.0.0.1:5000/shnootalk/compile/api/v1/dispatch
```
+ You will get back a response with reference id
```
{"_id":"61533f96d541934ade6525d1"}
```
+ Track execution status by watching the status endpoint
```
watch 'curl -s --request GET http://127.0.0.1:5000/shnootalk/compile/api/v1/status/61533f96d541934ade6525d1'
```
+ You will get back status response
```
{"_id":"61533f96d541934ade6525d1","status":"SCHEDULED"}
```
+ Once the execution is complete, you will get this response
```
{"_id":"61533f96d541934ade6525d1","output":"Hello world\n","status":"SUCCESS"}
```

## Env variables


### Server env variables

| Name                  | Description    
|-----------------------|-------------
| USE_INCLUSTER_CONFIG  | `"true"` or `"false"`. If server is deployed in a kubernetes cluster, setting this to `"true"` will tell the server to deploy jobs in the cluster it is running in.
| KUBE_CONTEXT          | Only applicable if USE_INCLUSTER_CONFIG is set to `"false"`. It will get cluster details from kubernetes context available on the machine it is running in.
| COMPILE_JOB_NAMESPACE | The namespace in which compile jobs will be deployed.
| MONGO_URL             | MongoDB connection string 
| MONGO_DATABASE        | Name of the database to use
| MONGO_COLLECTION      | Name of the collection to use
| MONGO_URL_SECRET_NAME | Name of the secret in which MongoDB connection string is present. This secret will be used by jobs to connect to the database, and should be deployed in COMPILE_JOB_NAMESPACE
| MONGO_URL_SECRET_KEY  | The key in which the connection string is present in the above secret MONGO_URL_SECRET_NAME

### Job env variables (controlled by server)

| Name              | Description 
|-------------------|-------------
| TIMEOUT           | Timeout for program execution and compilation (both separately)
| MONGO_URL         | MongoDB connection string 
| MONGO_DATABASE    | Name of the database to use
| MONGO_COLLECTION  | Name of the collection to use

## TODO

+ [ ] Make server control MONGO_DATABASE and MONGO_COLLECTION for the job (right now the README is a lie)
+ [ ] Add architecture diagram