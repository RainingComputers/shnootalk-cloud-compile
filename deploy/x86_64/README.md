![](logo.png)

# Deploy ShnooTalk Cloud Compile

1. Install [MongoDB Community Operator](https://github.com/mongodb/mongodb-kubernetes-operator)

3. Create compile namespace
    ```
    kubectl create namespace compile
    ```

2. Install MongoDB password secret

    *Base64 encoded password*
    ```
    echo -n '<password>' | base64
    ```

    *shnootalk-cloud-compile-mongodb-password.yml*
    ```yaml
    apiVersion: v1
    kind: Secret
    metadata:
      name: shnootalk-cloud-compile-mongodb-password
    type: Opaque
    data:
      password: <base64-encoded-password>
    ```

    *Apply*

    ```
    kubens default
    kubectl apply -f shnootalk-cloud-compile-mongodb-password.yml
    ```

3. Create MongoDB replica set
    
    *Apply*
    ```
    kubens default
    kubectl apply -f shnootalk-cloud-compile-mongodb.yml
    ```

    *Wait for three MongoDB pods to be up*
    ```
    kubens default
    watch 'kubectl get pods'
    ```

4. Install MongoDB URL secret in default namespace and compile namespace

    *Base64 encoded URL*
    ```
    PASSWORD=<password>
    URL="mongodb://shtkcc-user:${PASSWORD}@shnootalk-cloud-compile-mongodb-0.shnootalk-cloud-compile-mongodb-svc.default.svc.cluster.local:27017,shnootalk-cloud-compile-mongodb-1.shnootalk-cloud-compile-mongodb-svc.default.svc.cluster.local:27017,shnootalk-cloud-compile-mongodb-2.shnootalk-cloud-compile-mongodb-svc.default.svc.cluster.local:27017/?authSource=admin&authMechanism=SCRAM-SHA-256"
    echo -n $URL | base64
    ```

    *shnootalk-cloud-compile-mongodb-url.yml*
    ```yaml
    apiVersion: v1
    kind: Secret
    metadata:
      name: shnootalk-cloud-compile-mongodb-url
    type: Opaque
    data:
      connectionString: |
        <base-64-encoded-url>
    ```

    *Apply*
    ```
    kubens default
    kubectl apply -f shnootalk-cloud-compile-mongodb-url.yml
    kubens compile
    kubectl apply -f shnootalk-cloud-compile-mongodb-url.yml
    ```

6. Deploy Cloud Compile server
    ```
    kubens default
    kubectl apply -f shnootalk-cloud-compile-server.yml
    ```

7. Add cronjob to cleanup completed jobs
    ```
    kubens compile
    kubectl apply -f shnootalk-cloud-compile-job-cleanup-cron.yml
    ```
