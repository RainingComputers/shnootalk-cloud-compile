![](logo.png)

# Deploy ShnooTalk Cloud Compile on a k3s cluster in a Raspberry Pi

1. Install and setup loophole https://loophole.cloud/. This is optional, and is only needed if you want to expose you pi to the internet

2. Create loophole systemd service [OPTIONAL]
   ```
   sudo cp loophole.service /etc/systemd/system/loophole.service 
   sudo systemctl enable loophole
   sudo systemctl start loophole
   ```

3. Append `cgroup_memory=1 cgroup_enable=memory` to /boot/cmdline.txt
   ```
   vim /boot/config.txt
   ```

4. Install docker  https://docs.docker.com/engine/install/

5. Add current user to docker group
   ```
   sudo groupadd docker
   sudo usermod -aG docker $USER
   ```

6. Reboot
   ```
   sudo reboot
   ```

7. Install arkade https://github.com/alexellis/arkade

8. Install kubectl and kubectx and kubens
   ```
   arkade get kubectx kubectl kubens
   sudo mv /home/pi/.arkade/bin/kubectx /usr/local/bin/
   sudo mv /home/pi/.arkade/bin/kubectl /usr/local/bin/
   sudo mv /home/pi/.arkade/bin/kubens /usr/local/bin/
   ```

9. Install k3d https://k3d.io/v5.1.0/#installation

10. Create k3s cluster (or you can use other alternate ways to create a k3s cluster)
    ```
    k3d cluster create shnootalk-cloud-compile -p "8081:80@loadbalancer"
    ```

11. Create compile namespace
    ```
    kubectl create namespace compile
    ```

12. Install MongoDB URL secret in default namespace and compile namespace

    *Base64 encoded URL*
    ```
    echo -n '<your-hosted-mongodb-url>' | base64
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
