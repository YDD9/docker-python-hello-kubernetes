To use latest technology:
  * Debian9.3 stretch Linux
  * Docker17.03.0-ce
  * Kubernetes(solution Kubeadmv1.9)

Work based on host PC Win10 and VirtualBox, with different VirtualBox network settings: NAT and Bridge

* First part:
    prepare a simply Python Flask web app for Docker.
* Second part:
    deploy the app in Kubernetes Cluster(one master, one work node).

**A Docker Hello World! APP written in Python Flask deployed by kubernetes**

- [Environment](#environment)
- [List out used Python packages in requirements.txt](#list-out-used-python-packages-in-requirementstxt)
- [Dockerfile](#dockerfile)
- [Build Docker image](#build-docker-image)
- [Run app in Docker](#run-app-in-docker)
- [Verify the app in a browser](#verify-the-app-in-a-browser)
- [(Optional) Verify further the app](#optional-verify-further-the-app)
- [Push Docker image to dockerhub for easy download and reuse](#push-docker-image-to-dockerhub-for-easy-download-and-reuse)
- [(Optional) Save Docker image locally and import for use](#optional-save-docker-image-locally-and-import-for-use)
- [Use kubeadm to setup Kubernetes cluster](#use-kubeadm-to-setup-kubernetes-cluster)
- [Prepare deployment.yml and deploy app with kubectl](#prepare-deploymentyml-and-deploy-app-with-kubectl)
- [Check deployment status and troubleshot](#check-deployment-status-and-troubleshot)
        - [Once deployment created, check the process status](#once-deployment-created-check-the-process-status)
        - [Why deployment is unavailable, check deployed pods](#why-deployment-is-unavailable-check-deployed-pods)
        - [Why FailedCreatePodSandBox](#why-failedcreatepodsandbox)
        - [Why kube-flannel CrashLoopBackOff and kube-dns keep ContainerCreating...](#why-kube-flannel-crashloopbackoff-and-kube-dns-keep-containercreating)
- [kube-dns still failing and needs to be deleted](#kube-dns-still-failing-and-needs-to-be-deleted)
        - [retry with Flannel with hard coded IP range 10.244.0.0/16 and kube-dns works](#retry-with-flannel-with-hard-coded-ip-range-102440016-and-kube-dns-works)
- [Kubectl Autocomplete](#kubectl-autocomplete)
- [Deploy again the app](#deploy-again-the-app)

# Environment
host: Win10
      VirtualBox5.2 (network setting: NAT at beginning, later switch to Bridge):
          guest: Debian9.3 stretch Linux
                 Python2.7(extra package Flask and pipreqs)
                 Docker17.03.0-ce: run inside Debian Linux
                 Kubeadm1.9
                 Kubectl
                 Kubelet


**Almost all steps are done inside the guest Debian unless specified.**

# List out used Python packages in requirements.txt 
Generate a packages list based on import, ignore other not used ones.
But better to use `pip freeze` when you have a Python virtual env for dedicated projects.
```
$ pip install pipreqs
$ pipreqs --force 'C:\Users\ydd9\Documents\PythonHelloDockerK8s'
```


# Dockerfile
open dockerhub website to find a Linux image with python and follow the Dockerfile template there.
Dockerfile is used to build an image for you


# Build Docker image
```
$ cd PythonHelloDockerK8s
$ docker build ./ -t ydd9/python-hello
```


# Run app in Docker
if you execute app.py inside Debian, you will fail, because flask not installed and the goal is to run in Docker.
```
$ python app.py
missing module flask
```
when you lauch your Docker, flask will be installed inside and app.py will be executed.
```
$ cd PythonHelloDockerK8s
$ docker run -p 8888:8080 ydd9/python-hello
* Running on http://0.0.0.0:8080/ (Press CTRL+C to quit)
```


# Verify the app in a browser
open another terminal use `docker ps` to find ContainerID df573987753e of the image ydd9/python-hello,
you also notice docker container is using port 8888 and listen incoming traffic at port 8080,
just as command `docker run -p 8888:8080 ydd9/python-hello` specifies.

then use `docker inspect <ContainerID>` to find the exposed "IPAddress": "172.17.0.2" of the container

think through the scenario this way:
docker container itself will use localhost 127.0.0.1:8888 to execute the job, but inside the guest Debian, Docker app expose port 8080, so it is seen as 172.17.0.2:8080, just type `172.17.0.2:8080` in web browser inside Debian, "Hello World!" should display.

further more, if you want to see this display in host win10 web browser, what should be configured ?
VirtualBox Network settings by default use NAT, now config a port forwarding, set guest port is 8888 and any free host port we like, let's say 1234, so `127.0.0.1:1234` load the page correctly. VirtualBox route the output of docker container from port 8888 to port 1234

```
$ docker ps
CONTAINER ID        IMAGE
             COMMAND                  CREATED             STATUS              PORTS                     NAMES
df573987753e        ydd9/python-hello
             "python ./app.py"        47 seconds ago      Up 46 seconds       0.0.0.0:8888->8080/tcp   happy_lewin
4bcf36896861        gcr.io/google_containers/k8s-dns-sidecar-amd64@sha256:f80f5f9328107dc516d67f7b70054354b9367d31d4946a3bffd3383d83d7efe8         "/sidecar --v=2 --..."   5 hours ago         Up 5 hours                                    k8s_sidecar_kube-dns-6f4fd4bdf-txj26_kube-system_edd99c09-ebf4-11e7-a191-080027f0e96d_0
...

$ docker inspect df573987753e
...
"Ports": {
                "8080/tcp": null
            },
            "SandboxKey": "/var/run/docker/netns/39b487507165",
            "SecondaryIPAddresses": null,
            "SecondaryIPv6Addresses": null,
            "EndpointID": "a15143d9f57406a07b695d666158d7c64511d800113f79e77c4240c68c9d22f2",
            "Gateway": "172.17.0.1",
            "GlobalIPv6Address": "",
            "GlobalIPv6PrefixLen": 0,
            "IPAddress": "172.17.0.2",
            "IPPrefixLen": 16,
            "IPv6Gateway": "",
...

```


# (Optional) Verify further the app
With below Docker run, the app will run at port X auto chosen by Docker and you can check in Debian the display "Hello World!" at port X.
But in win10, port forwarding needs to reconfig to port X too.
```
$ docker run -p 8080 ydd9/python-hello

# find out port X
$ docker ps
```

if docker run -p publish a wrong port such as 8081, inside debian still work for `172.17.0.2:8080` but not 8081.
I think because docker run publish automatically the same port as app.py, as `docker run ydd9/python-hello` works too. inside win10 will not work, the miss match of tcp port.
```
$ docker run -p 8888:8081 ydd9/python-hello
$ docker ps | grep hello
37ef88012ba8        ydd9/python-hello
             "python ./app.py"        42 seconds ago      Up 41 seconds       8080/tcp, 0.0.0.0:8888->8081/tcp   elastic_fermat
```

If now you want all colleagues access your website, you switch to use Bridge network settings in VirtualBox
You should then `$ docker run --network=host ydd9/python-hello`, next is to find Debian VM IP address 192.168.0.39 via `$ ip a` So now from your host win10, your guest Debian and your colleagues system, open website `192.168.0.39:8080` should display the "Hello, world!"  https://forums.docker.com/t/how-to-access-docker-container-from-another-machine-on-local-network/4737/11


# Push Docker image to dockerhub for easy download and reuse
https://docs.docker.com/docker-cloud/builds/push-images/
```
$ export DOCKER_ID_USER="username"
$ docker login
$ docker tag my_image $DOCKER_ID_USER/my_image
$ docker push $DOCKER_ID_USER/my_image
# verify in docker hub
```


# (Optional) Save Docker image locally and import for use
```
$ docker save my_image > my_image.tar

$ docker load --input my_image.tar
```


- [Environment](#environment)
- [requirements.txt list out all used Python packages](#requirementstxt-list-out-all-used-python-packages)
- [Dockerfile](#dockerfile)
- [build your image](#build-your-image)
- [run your app in Docker](#run-your-app-in-docker)
- [verify the app in a browser](#verify-the-app-in-a-browser)
- [Further verify the app in browser](#further-verify-the-app-in-browser)
- [push docker images to dockerhub for easy usages on other PCs](#push-docker-images-to-dockerhub-for-easy-usages-on-other-pcs)
- [save docker images locally and import for use](#save-docker-images-locally-and-import-for-use)
- [deploy with kubectl and yml](#deploy-with-kubectl-and-yml)
- [check deployment status and troubleshot](#check-deployment-status-and-troubleshot)
        - [Once deployment created, check the process status](#once-deployment-created-check-the-process-status)
        - [Why 2 unavailable, check deployed pods](#why-2-unavailable-check-deployed-pods)
        - [Why FailedCreatePodSandBox](#why-failedcreatepodsandbox)
        - [Why kube-flannel CrashLoopBackOff and kube-dns keep Creating...](#why-kube-flannel-crashloopbackoff-and-kube-dns-keep-creating)
- [kube-dns still failing and needs to be deleted](#kube-dns-still-failing-and-needs-to-be-deleted)
        - [retry with Flannel with given IP range 10.244.0.0/16 NO change and kube-dns works](#retry-with-flannel-with-given-ip-range-102440016-no-change-and-kube-dns-works)
- [Kubectl Autocomplete](#kubectl-autocomplete)


**Deploy this app with Kubernetes(K8s)**

# Use kubeadm to setup Kubernetes cluster
Official guid is very clear, but you may encounter different problems, you can check problems I had via [this link](https://github.com/YDD9/YDD9.github.io/blob/master/_posts/2017-12-21-Docker-Kubernetes.md#kubeadm-install)

You can also deploy K8s cluster manually, this hard way is good for people who want to understand all and
admin the process. https://github.com/kelseyhightower/kubernetes-the-hard-way or the official guide.


# Prepare deployment.yml and deploy app with kubectl
template found https://kubernetes.io/docs/tasks/run-application/run-stateless-application-deployment/
```
$ kubectl apply -f https://github.com/YDD9/docker-app-hello/blob/master/deployment.yml
error: yaml: line 2: mapping values are not allowed in this context
# this githube link is not able to give a pure .yml file, but you click button raw, then the link should work
# https://raw.githubusercontent.com/YDD9/docker-app-hello/master/deployment.yml

# if don't have github, you can put the file on cluster master locally
$ kubectl apply -f /media/share/deployment.yml
deployment "python-hello-deployment" created
```

# Check deployment status and troubleshot
### Once deployment created, check the process status
```
$ kubectl describe deployment python-hello-deployment
Name:                   python-hello-deployment
Namespace:              default
CreationTimestamp:      Sat, 30 Dec 2017 12:15:46 -0500
Labels:                 app=python-hello
Annotations:            deployment.kubernetes.io/revision=1
                        kubectl.kubernetes.io/last-applied-configuration={"apiVersion":"apps/v1beta2","kind":"Deployment","metadata":{"annotations":{},"name":"python-hello-deployment","namespace":"default"},"spec":{"replicas...
Selector:               app=python-hello
Replicas:               2 desired | 2 updated | 2 total | 0 available | 2 unavailable
StrategyType:           RollingUpdate
MinReadySeconds:        0
RollingUpdateStrategy:  25% max unavailable, 25% max surge
Pod Template:
  Labels:  app=python-hello
  Containers:
   python-hello:
    Image:        ydd9/python-hello
    Port:         8080/TCP
    Environment:  <none>
    Mounts:       <none>
  Volumes:        <none>
Conditions:
  Type           Status  Reason
  ----           ------  ------
  Available      False   MinimumReplicasUnavailable
  Progressing    False   ProgressDeadlineExceeded
OldReplicaSets:  <none>
NewReplicaSet:   python-hello-deployment-6b69b45664 (2/2 replicas created)
Events:
  Type    Reason             Age   From                   Message
  ----    ------             ----  ----                   -------
  Normal  ScalingReplicaSet  12m   deployment-controller  Scaled up replica set python-hello-deployment-6b69b45664 to 2
```

### Why deployment is unavailable, check deployed pods
```
$ kubectl describe pods python-hello-deployment
Name:           python-hello-deployment-6b69b45664-54898
Namespace:      default
Node:           kubemaster/192.168.0.39
Start Time:     Sat, 30 Dec 2017 12:15:47 -0500
Labels:         app=python-hello
                pod-template-hash=2625601220
Annotations:    <none>
Status:         Pending
IP:
Controlled By:  ReplicaSet/python-hello-deployment-6b69b45664
Containers:
  python-hello:
    Container ID:
    Image:          ydd9/python-hello
    Image ID:
    Port:           8080/TCP
    State:          Waiting
      Reason:       ContainerCreating
    Ready:          False
    Restart Count:  0
    Environment:    <none>
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from default-token-jtvxk (ro)
Conditions:
  Type           Status
  Initialized    True
  Ready          False
  PodScheduled   True
Volumes:
  default-token-jtvxk:
    Type:        Secret (a volume populated by a Secret)
    SecretName:  default-token-jtvxk
    Optional:    false
QoS Class:       BestEffort
Node-Selectors:  <none>
Tolerations:     node.kubernetes.io/not-ready:NoExecute for 300s
                 node.kubernetes.io/unreachable:NoExecute for 300s
Events:
  Type     Reason                  Age                 From                 Message
  ----     ------                  ----                ----                 -------
  Normal   Scheduled               13m                 default-scheduler    Successfully assigned python-hello-deployment-6b69b45664-54898 to kubemaster
  Normal   SuccessfulMountVolume   13m                 kubelet, kubemaster  MountVolume.SetUp succeeded for volume "default-token-jtvxk"
  Warning  FailedCreatePodSandBox  13m (x12 over 13m)  kubelet, kubemaster  Failed create pod sandbox.
  Normal   SandboxChanged          3m (x531 over 13m)  kubelet, kubemaster  Pod sandbox changed, it will be killed and re-created.

Name:           python-hello-deployment-6b69b45664-vqj57
Namespace:      default
Node:           kubemaster/192.168.0.39
Start Time:     Sat, 30 Dec 2017 12:15:47 -0500
Labels:         app=python-hello
                pod-template-hash=2625601220
Annotations:    <none>
Status:         Pending
IP:
Controlled By:  ReplicaSet/python-hello-deployment-6b69b45664
Containers:
  python-hello:
    Container ID:
    Image:          ydd9/python-hello
    Image ID:
    Port:           8080/TCP
    State:          Waiting
      Reason:       ContainerCreating
    Ready:          False
    Restart Count:  0
    Environment:    <none>
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from default-token-jtvxk (ro)
Conditions:
  Type           Status
  Initialized    True
  Ready          False
  PodScheduled   True
Volumes:
  default-token-jtvxk:
    Type:        Secret (a volume populated by a Secret)
    SecretName:  default-token-jtvxk
    Optional:    false
QoS Class:       BestEffort
Node-Selectors:  <none>
Tolerations:     node.kubernetes.io/not-ready:NoExecute for 300s
                 node.kubernetes.io/unreachable:NoExecute for 300s
Events:
  Type     Reason                  Age                 From                 Message
  ----     ------                  ----                ----                 -------
  Normal   Scheduled               13m                 default-scheduler    Successfully assigned python-hello-deployment-6b69b45664-vqj57 to kubemaster
  Normal   SuccessfulMountVolume   13m                 kubelet, kubemaster  MountVolume.SetUp succeeded for volume "default-token-jtvxk"
  Warning  FailedCreatePodSandBox  8m (x272 over 13m)  kubelet, kubemaster  Failed create pod sandbox.
  Normal   SandboxChanged          3m (x535 over 13m)  kubelet, kubemaster  Pod sandbox changed, it will be killed and re-created.
```

### Why FailedCreatePodSandBox
```
$ kubectl get pods --all-namespaces
NAMESPACE     NAME                                       READY     STATUS              RESTARTS   AGE
default       python-hello-deployment-6b69b45664-54898   0/1       ContainerCreating   0          15m
default       python-hello-deployment-6b69b45664-vqj57   0/1       ContainerCreating   0          15m
kube-system   etcd-kubeslave1                            1/1       Running             0          33m
kube-system   kube-apiserver-kubeslave1                  1/1       Running             0          33m
kube-system   kube-controller-manager-kubeslave1         1/1       Running             0          33m
kube-system   kube-dns-6f4fd4bdf-sxhhd                   0/3       ContainerCreating   0          34m
kube-system   kube-flannel-ds-b67hx                      1/2       CrashLoopBackOff    11         33m
kube-system   kube-flannel-ds-v9dp5                      1/2       CrashLoopBackOff    8          20m
kube-system   kube-proxy-4q2pw                           1/1       Running             0          20m
kube-system   kube-proxy-9nfq7                           1/1       Running             0          34m
kube-system   kube-scheduler-kubeslave1                  1/1       Running             0          33m
```

### Why kube-flannel CrashLoopBackOff and kube-dns keep ContainerCreating...
https://github.com/kubernetes/kubeadm/issues/578
check journalctl on master and on nodes
check kubelet status on master and on nodes
check `kubectl describe pods python-hello-deployment`

work on each errors, normally the kube-dns is troublesome, install different CNI is one option
```
$ journalctl -u kubelet
$ journalctl -xe

$ systemctl status kubelet -l
● kubelet.service - kubelet: The Kubernetes Node Agent
   Loaded: loaded (/lib/systemd/system/kubelet.service; enabled; vendor preset: enabled)
  Drop-In: /etc/systemd/system/kubelet.service.d
           └─10-kubeadm.conf
   Active: active (running) since Sat 2017-12-30 17:32:35 EST; 45min ago
     Docs: http://kubernetes.io/docs/
 Main PID: 1337 (kubelet)
    Tasks: 18 (limit: 4915)
   Memory: 53.6M
      CPU: 1min 39.860s
   CGroup: /system.slice/kubelet.service
           └─1337 /usr/bin/kubelet --bootstrap-kubeconfig=/etc/kubernetes/bootstrap-kubelet.conf --kubeconfig=/etc/kubernetes/ku

Dec 30 18:10:04 kubeslave1 kubelet[1337]: W1230 18:10:04.407499    1337 reflector.go:341] k8s.io/kubernetes/pkg/kubelet/config/aDec 30 18:15:41 kubeslave1 kubelet[1337]: W1230 18:15:41.698709    1337 raw.go:87] Error while processing event ("/sys/fs/cgroupDec 30 18:15:41 kubeslave1 kubelet[1337]: W1230 18:15:41.703225    1337 raw.go:87] Error while processing event ("/sys/fs/cgroupDec 30 18:15:41 kubeslave1 kubelet[1337]: W1230 18:15:41.703284    1337 raw.go:87] Error while processing event ("/sys/fs/cgroupDec 30 18:15:41 kubeslave1 kubelet[1337]: W1230 18:15:41.703315    1337 raw.go:87] Error while processing event
```

swap must not be used.
https://serverfault.com/questions/684771/best-way-to-disable-swap-in-linux

1. run swapoff -a : this will immediately disable swap.
2. remove/comment any swap entry from /etc/fstab.
3. reboot the system. If the swap is gone, good. If, for some reason, it is still here, you had to remove the swap partition. Repeat steps 1 and 2 and, after that, use fdisk or parted to remove the (now unused) swap partition. ...
4. reboot.

Most probably not relevant here but keep an eye: https://github.com/kubernetes/kubernetes/pull/50377
add flag --fail-swap-on=false to .../hack/local-up-cluster.sh

# kube-dns still failing and needs to be deleted
Before I used Flannel CNI network plugin, now I `kubeadm reset` and use Calico the same issue.
```
kubectl get pods --all-namespaces
NAMESPACE     NAME                                     READY     STATUS    RESTARTS   AGE
kube-system   calico-etcd-tv9mk                        1/1       Running   0          22m
kube-system   calico-kube-controllers-d6c6b9b8-zvk9k   1/1       Running   0          22m
kube-system   calico-node-d4lzq                        2/2       Running   0          22m
kube-system   etcd-kubeslave1                          1/1       Running   0          23m
kube-system   kube-apiserver-kubeslave1                1/1       Running   0          23m
kube-system   kube-controller-manager-kubeslave1       1/1       Running   0          24m
kube-system   kube-dns-6f4fd4bdf-xb9xr                 0/3       Pending   0          24m
...

# https://stackoverflow.com/questions/38263252/how-to-delete-kubernetes-pods-and-other-resources-in-the-system-namespace
# delete a kube-dns pod from kube-system
$ kubectl get deployment --namespace=kube-system
NAME                       DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
calico-kube-controllers    1         1         1            1           24m
calico-policy-controller   0         0         0            0           24m
kube-dns                   1         1         1            0           26m

$ kubectl delete deployment kube-dns --namespace=kube-system
deployment "kube-dns" deleted

# deploy again the kube-dns
$ kubectl apply -f https://raw.githubusercontent.com/kelseyhightower/kubernetes-the-hard-way/master/deployments/kube-dns.yaml
```

```
# delete a node from cluster
$ kubectl delete node <node_name1> <node_name2>
```

### retry with Flannel with hard coded IP range 10.244.0.0/16 and kube-dns works
Now the issue is one step further, but my newly added node never Ready, so I think my image is really
not good, so I clone the master image and make sure new MAC, new IP to generate a new VM, and everything
works now
```
root@node40$ kubeadm init --pod-network-cidr=10.244.0.0/16

root@node40:~# kubectl get pods --all-namespaces
NAMESPACE     NAME                             READY     STATUS    RESTARTS   AGE
kube-system   etcd-node40                      1/1       Running   0          10m
kube-system   kube-apiserver-node40            1/1       Running   0          10m
kube-system   kube-controller-manager-node40   1/1       Running   0          10m
kube-system   kube-dns-6f4fd4bdf-b6bgb         3/3       Running   0          11m
kube-system   kube-flannel-ds-9h5vg            1/1       Running   0          9m
kube-system   kube-flannel-ds-c6gvc            1/1       Running   0          9m
kube-system   kube-proxy-j4bzd                 1/1       Running   0          11m
kube-system   kube-proxy-qgh7c                 1/1       Running   0          10m
kube-system   kube-scheduler-node40            1/1       Running   0          10m

root@node40:~# kubectl get nodes
NAME      STATUS    ROLES     AGE       VERSION
node40    Ready     master    12m       v1.9.0
node42    Ready     <none>    10m       v1.9.0
```

```
root@node42$ kubeadm join --token 962fce.ef1baf1602f7e1ab 192.168.0.40:6443 --discovery-token-ca-cert-hash sha256:d552ce6f4ac8523fc76f7bf24b244ea2a51b7d70188d1a566babc4cd23e8d65c
```

# Kubectl Autocomplete
```
$ apt-get install bash-completion
$ source <(kubectl completion bash) # setup autocomplete in bash, bash-completion package should be installed first.
```

# Deploy again the app
```
$ kubectl apply -f https://raw.githubusercontent.com/YDD9/docker-app-hello/master/deployment.yml

$ kubectl get pods --all-namespaces
NAMESPACE     NAME                                       READY     STATUS              RESTARTS   AGE
default       python-hello-deployment-6b69b45664-744h8   0/1       ContainerCreating   0          6m
default       python-hello-deployment-6b69b45664-nqxw4   0/1       ContainerCreating   0          6m
kube-system   etcd-node40                                1/1       Running             0          1h
kube-system   kube-apiserver-node40                      1/1       Running             0          1h
kube-system   kube-controller-manager-node40             1/1       Running             0          1h
kube-system   kube-dns-6f4fd4bdf-b6bgb                   3/3       Running             0          1h
kube-system   kube-flannel-ds-9h5vg                      1/1       Running             0          1h
kube-system   kube-flannel-ds-c6gvc                      1/1       Running             0          1h
kube-system   kube-proxy-j4bzd                           1/1       Running             0          1h
kube-system   kube-proxy-qgh7c                           1/1       Running             0          1h
kube-system   kube-scheduler-node40                      1/1       Running             0          1h
```




