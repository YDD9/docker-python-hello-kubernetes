
**Python-hello is a stateless app deployment**
**mysql is a stateful app deployment which run only one pod and should not scale**

- [Spot the deployment order](#spot-the-deployment-order)
- [Update deployement or image](#update-deployement-or-image)
- [Roll back deployment](#roll-back-deployment)
- [Scale out, autosacle based on CPU usage](#scale-out-autosacle-based-on-cpu-usage)
- [Deployment pause and resume](#deployment-pause-and-resume)
- [Writing a Deployment Spec](#writing-a-deployment-spec)
- [Alternative to Deployments](#alternative-to-deployments)
- [Explorer kubectl commands](#explorer-kubectl-commands)
- [Expose pods](#expose-pods)
- [Label one of the app pods as test](#label-one-of-the-app-pods-as-test)
- [Expose Pod Information to Containers Through Files](#expose-pod-information-to-containers-through-files)
- [Switch to local as PersistentVolume, StorageClass is only supported when using cloud volume](#switch-to-local-as-persistentvolume-storageclass-is-only-supported-when-using-cloud-volume)
- [Switch to hostpath PV](#switch-to-hostpath-pv)
- [connect to mysql via a client](#connect-to-mysql-via-a-client)

# Spot the deployment order
Look at the hash name after the python-hello-deployment, it's added one after another:
deployment
replicas set
pods
```
root@node40:~# kubectl get deploy && kubectl get rs && kubectl get po
NAME                      DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
python-hello-deployment   1         1         1            1           14h
NAME                                 DESIRED   CURRENT   READY     AGE
python-hello-deployment-6b69b45664   1         1         1         14h
NAME                                       READY     STATUS    RESTARTS   AGE
python-hello-deployment-6b69b45664-kwnlz   1/1       Running   1          14h
```

# Update deployement or image
```
$ kubectl edit deployment/nginx-deployment
# then edit the file in vi mode, :wq! save quit or :q! quit without save
# .spec.template.spec.containers[0].image from nginx:1.7.9 to nginx:1.9.1

# or with command
$ kubectl set image deployment/nginx-deployment nginx=nginx:1.9.1
```
If selector.label is updated, you risk to orphane the old replicas, better don't change. Or delete old and then deploy new ones:
* Selector additions require the pod template labels in the Deployment spec to be updated with the new label too, otherwise a validation error is returned. This change is a non-overlapping one, meaning that the new selector does not select ReplicaSets and Pods created with the old selector, resulting in orphaning all old ReplicaSets and creating a new ReplicaSet.
* Selector updates – that is, changing the existing value in a selector key – result in the same behavior as additions.
* Selector removals – that is, removing an existing key from the Deployment selector – do not require any changes in the pod template labels. No existing ReplicaSet is orphaned, and a new ReplicaSet is not created, but note that the removed label still exists in any existing Pods and ReplicaSets.

# Roll back deployment
```
$ kubectl rollout undo deployment/nginx-deployment

$ kubectl rollout history deployment/nginx-deployment
$ kubectl rollout undo deployment/nginx-deployment --to-revision=2

$ kubectl rollout status deployment/nginx-deployment
```

# Scale out, autosacle based on CPU usage
```
$ kubectl scale deployment nginx-deployment --replicas=10
$ kubectl autoscale deployment nginx-deployment --min=10 --max=15 --cpu-percent=80
```

# Deployment pause and resume
During applying fixes/changes fot the app, pause new deployment of app, once changes done, resume to deploy.
```
$ kubectl rollout pause deployment/nginx-deployment

$ kubectl set image deploy/nginx-deployment nginx=nginx:1.9.1
$ kubectl set resources deployment nginx-deployment -c=nginx --limits=cpu=200m,memory=512Mi

$ kubectl rollout resume deploy/nginx-deployment
```

# Writing a Deployment Spec
As with all other Kubernetes configs, a Deployment needs apiVersion, kind, and metadata fields. For general
information about working with config files, see deploying applications, configuring containers, and using
kubectl to manage resources documents. A Deployment also needs a .spec section. Much more details in official
doc.

# Alternative to Deployments
kubectl rolling update
Kubectl rolling update updates Pods and ReplicationControllers in a similar fashion. But Deployments are
recommended, since they are declarative, server side, and have additional features, such as rolling back to
any previous revision even after the rolling update is done.

# Explorer kubectl commands
https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#delete

# Expose pods
Pod, cluster and node do not have routable IPs, to access pod from node,
an easy way is to expose pod via a NodePort, all tracffic to NodeIP:NodePort route to podIP:--target-port.
For me the --port is only for mapping purpose inside pod and another abstraction, need to understand more.

Open a web browser in one of nodes, type any podIP:8080, you will see the web. (inside cluster access)
Open a web browser in one of nodes, type any NodeIP:NodePort, you will see the web as well. (outside cluster access)
```
root@node40:~# kubectl expose deployment python-hello-deployment --port=80 --target-port=8080 --type=NodePort
service "python-hello-deployment" exposed

root@node40:~# kubectl describe po python | grep ip -i | awk '{print $2"\t"$1}'
10.244.1.14     IP:
10.244.1.12     IP:
10.244.1.13     IP:
```

Behind the scene there's a service created to expose the container/pod at NodePod 30555/TCP
```
root@node40:~# kubectl describe services python
Name:                     python-hello-deployment
Namespace:                default
Labels:                   app=python-hello
Annotations:              <none>
Selector:                 app=python-hello
Type:                     NodePort
IP:                       10.102.41.191
Port:                     <unset>  80/TCP
TargetPort:               8080/TCP
NodePort:                 <unset>  30555/TCP
Endpoints:                10.244.1.12:8080,10.244.1.13:8080,10.244.1.14:8080
Session Affinity:         None
External Traffic Policy:  Cluster
Events:                   <none>

root@node40:~# curl http://192.168.0.40:30555/
Hello World!
root@node40:~# curl http://192.168.0.42:30555/
Hello World!

# Above traffic will be route to any of below pods, load-balancing integrated.

root@node40:~# curl http://10.244.1.12:8080
Hello World!
root@node40:~# curl http://10.244.1.13:8080
Hello World!
root@node40:~# curl http://10.244.1.14:8080
Hello World!
```
Better way to handle this can be create a service
http://alesnosek.com/blog/2017/02/14/accessing-kubernetes-pods-from-outside-of-the-cluster/

# Label one of the app pods as test
Take out one pod from current app to be used for test purpose,
but it will then not manage by python-hello-deployment, needs to be deleted manually.
https://www.mirantis.com/blog/kubernetes-replication-controller-replica-set-and-deployments-understanding-replication-options/
```
root@node40:~# kubectl get pods -l app=python-hello
NAME                                       READY     STATUS    RESTARTS   AGE
python-hello-deployment-6b69b45664-cq22l   1/1       Running   0          1h
python-hello-deployment-6b69b45664-kwnlz   1/1       Running   2          18h
python-hello-deployment-6b69b45664-msvzd   1/1       Running   0          1h

root@node40:~# kubectl label pods python-hello-deployment-6b69b45664-msvzd test=true
pod "python-hello-deployment-6b69b45664-msvzd" labeled

root@node40:~# kubectl get pods -l test=true
NAME                                       READY     STATUS    RESTARTS   AGE
python-hello-deployment-6b69b45664-msvzd   1/1       Running   0          1h

# take this test pod out of the app
root@node40:~# kubectl label pods python-hello-deployment-6b69b45664-msvzd app=test-python-hello --overwrite
pod "python-hello-deployment-6b69b45664-msvzd" labeled

# new pod python-hello-deployment-6b69b45664-dqf64 created in app
root@node40:~# kubectl get pods -l app=python-hello
NAME                                       READY     STATUS    RESTARTS   AGE
python-hello-deployment-6b69b45664-cq22l   1/1       Running   0          1h
python-hello-deployment-6b69b45664-dqf64   1/1       Running   0          44s
python-hello-deployment-6b69b45664-kwnlz   1/1       Running   2          18h

root@node40:~# kubectl get pods -l app=test-python-hello
NAME                                       READY     STATUS    RESTARTS   AGE
python-hello-deployment-6b69b45664-msvzd   1/1       Running   0          1h
root@node40:~# kubectl get pods -l test=true
NAME                                       READY     STATUS    RESTARTS   AGE
python-hello-deployment-6b69b45664-msvzd   1/1       Running   0          1h
```

# Expose Pod Information to Containers Through Files
https://kubernetes.io/docs/tasks/inject-data-application/downward-api-volume-expose-pod-information/


**mysql stateful app deployment**
Since kubeamd cluster doesn't create default StorageClass, following  https://kubernetes.io/docs/tasks/run-application/run-single-instance-stateful-application/ to deploy will fail.
```
$ kubectl create -f https://k8s.io/docs/tasks/run-application/mysql-deployment.yaml
service "mysql" created
persistentvolumeclaim "mysql-pv-claim" created
deployment "mysql" created

$ kubectl get pvc
...
Events:
  Type    Reason         Age               From                         Message
  ----    ------         ----              ----                         -------
  Normal  FailedBinding  12s (x7 over 1m)  persistentvolume-controller  no persistent volumes available for this claim and no storage class is set

root@node42:~# journalctl -ex | less
332 desired_state_of_world_populator.go:273] Error processing volume "mysql-persistent-storage" for pod "mysql-544bbdcd6f-lzzhk_default(ab777c8e-ef34-11e7-8bf0-0800274f1ac0)": error processing PVC "default"/"mysql-pv-claim": PVC default/mysql-pv-claim has non-bound phase ("Pending") or empty pvc.Spec.VolumeName ("")

# It is true that no StorageClass exists
root@node40:/media/share# kubectl get sc
No resources found.
```
The promotion of Dynamic Provisioning and Storage Classes catches me http://blog.kubernetes.io/2017/03/dynamic-provisioning-and-storage-classes-kubernetes.html and I would like to try with creation https://kubernetes.io/docs/concepts/storage/dynamic-provisioning/

DynamicSC.yaml to create SC fast for SSD
```
---
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast
provisioner: kubernetes.io/gce-pd
parameters:
  type: pd-ssd
```

DynamicPVC.yaml used to create PVC fast
```
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mysql-pv-claim
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: fast
  resources:
    requests:
      storage: 1Gi
  VolumeName: mysql-persistent-storage
```

Check after deploy
```
root@node40:/media/share# kubectl apply -f DynamicSC.yaml
storageclass "fast" created
root@node40:/media/share# kubectl get sc
NAME      PROVISIONER            AGE
fast      kubernetes.io/gce-pd   2s

# make the StorageClass fast as default SC "true"
root@node40:/media/share# kubectl patch storageclass fast -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"true"}}}'
storageclass "fast" patched
root@node40:/media/share# kubectl get sc
NAME             PROVISIONER            AGE
fast (default)   kubernetes.io/gce-pd   1m

# create PVC but always pending
root@node40:/media/share# kubectl apply -f DynamicPVC.yaml
persistentvolumeclaim "mysql-pv-claim" created
root@node40:/media/share# kubectl get pvc
NAME             STATUS    VOLUME    CAPACITY   ACCESS MODES   STORAGECLASS   AGE
mysql-pv-claim   Pending                                       fast           31s

root@node40:/media/share# kubectl describe pvc
Name:          mysql-pv-claim
...
Events:
  Type     Reason              Age   From                         Message
  ----     ------              ----  ----                         -------
  Warning  ProvisioningFailed  12s   persistentvolume-controller  Failed to provision volume with StorageClass "fast": Failed to get GCE GCECloudProvider with error <nil>

# check SC yml provisioner: kubernetes.io/gce-pd is wrong, this is for google cloud storage

# Dynamic StorageClass is by default automatically deleted when PVC is deleted
root@node40:/media/share# kubectl delete pvc mysql-pv-claim
persistentvolumeclaim "mysql-pv-claim" deleted
root@node40:/media/share# kubectl get rc
No resources found.
```

# Switch to local as PersistentVolume, StorageClass is only supported when using cloud volume
https://kubernetes.io/docs/concepts/storage/volumes/#local
https://stackoverflow.com/questions/34282704/can-a-pvc-be-bound-to-a-specific-pv

Change metadata.annotations...values to your node name
Change spec.local.path to your node dir
It doesn't work as Alpha feature needs some hack
https://github.com/kubernetes/website/issues/6141
```
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv0001
  annotations:
        "volume.alpha.kubernetes.io/node-affinity": '{
            "requiredDuringSchedulingIgnoredDuringExecution": {
                "nodeSelectorTerms": [
                    { "matchExpressions": [
                        { "key": "kubernetes.io/hostname",
                          "operator": "In",
                          "values": ["node42"]
                        }
                    ]}
                 ]}
              }'
spec:
    capacity:
      storage: 1Gi
    accessModes:
    - ReadWriteOnce
    persistentVolumeReclaimPolicy: Delete
    # storageClassName: local-storage
    local:
      path: /mnt/disks/ssd1
```

```
kind: PersistentVolume
apiVersion: v1
metadata:
  name: task-pv-volume
  labels:
    type: local
spec:
  storageClassName: manual
  capacity:
    storage: 10Gi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: "/tmp/data"
```

# Switch to hostpath PV
https://kubernetes.io/docs/tasks/configure-pod-container/configure-persistent-volume-storage/
Kubernetes supports hostPath for development and testing on a single-node cluster. But mine is two nodes: one master, one node, still worth trying.

change metadata.name to a random name pv0001
change spec.hostPath.path to an existing node dir
comment spec.sotragecClassName to avoid PVC to use Dynamic mode.
```
kind: PersistentVolume
apiVersion: v1
metadata:
  name: pv0001
  labels:
    type: local
spec:
  # storageClassName: manual
  capacity:
    storage: 1Gi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: "/mnt/disks/ssd1"
```

SVC, PVC, Deployment
```
apiVersion: v1
kind: Service
metadata:
  name: mysql
spec:
  ports:
  - port: 3306
  selector:
    app: mysql
  clusterIP: None
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mysql-pv-claim
spec:
  accessModes:
    - ReadWriteOnce
#  storageClassName: fast
  resources:
    requests:
      storage: 1Gi
---
apiVersion: apps/v1beta2 # for versions before 1.8.0 use apps/v1beta1
kind: Deployment
metadata:
  name: mysql
spec:
  selector:
    matchLabels:
      app: mysql
  strategy:
    type: Recreate
  template:
    metadata:
      labels:
        app: mysql
    spec:
      containers:
      - image: mysql:5.6
        name: mysql
        env:
          # Use secret in real usage
        - name: MYSQL_ROOT_PASSWORD
          value: password
        ports:
        - containerPort: 3306
          name: mysql
        volumeMounts:
        - name: mysql-persistent-storage
          mountPath: /var/lib/mysql
      volumes:
      - name: mysql-persistent-storage
        persistentVolumeClaim:
          claimName: mysql-pv-claim
```

Now this works, it takes less than one minute.
```
root@node40:/media/share# kubectl get pv
NAME      CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS    CLAIM                    STORAGECLASS   REASON    AGE
pv0001    1Gi        RWO            Retain           Bound     default/mysql-pv-claim                            3m
root@node40:/media/share# kubectl get pvc
NAME             STATUS    VOLUME    CAPACITY   ACCESS MODES   STORAGECLASS   AGE
mysql-pv-claim   Bound     pv0001    1Gi        RWO                           41s
root@node40:/media/share# kubectl get svc
NAME         TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)    AGE
kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP    1d
mysql        ClusterIP   None         <none>        3306/TCP   59s
root@node40:/media/share# kubectl get deploy
NAME      DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
mysql     1         1         1            1           1m
root@node40:/media/share# kubectl get po
NAME                     READY     STATUS    RESTARTS   AGE
mysql-544bbdcd6f-msssf   1/1       Running   0          1m
```

To gain better understanding of Volume is to check youtube
![Volume](https://raw.githubusercontent.com/YDD9/docker-app-hello/master/images/Volume.png)

# connect to mysql via a client
```
root@node40:/media/share# kubectl run -it --rm --image=mysql:5.6 --restart=Never mysql-client -- mysql -h mysql -ppassword
If you don't see a command prompt, try pressing enter.

mysql> create database test;
mysql> use test;
mysql> create table  pet (name VARCHAR(20), owner VARCHAR(20), species VARCHAR(20), sex CHAR(1), birth DATE, death DATE);
Query OK, 0 rows affected (0.04 sec)
```