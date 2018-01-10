Helm</br>
kubernetes package management tool

- [[Install Helm](https://github.com/kubernetes/helm/blob/master/docs/install.md)](#install-helmhttpsgithubcomkuberneteshelmblobmasterdocsinstallmd)
- [Installing Tiller](#installing-tiller)
- [Use helm to install package](#use-helm-to-install-package)


# [Install Helm](https://github.com/kubernetes/helm/blob/master/docs/install.md)
```
$ curl https://raw.githubusercontent.com/kubernetes/helm/master/scripts/get > get_helm.sh
$ chmod 700 get_helm.sh
$ ./get_helm.sh
```
# Installing Tiller
Tiller, the server portion of Helm, typically runs inside of your Kubernetes cluster. But for development, it can also be run locally, and configured to talk to a remote Kubernetes cluster.

The easiest way to install tiller into the cluster is simply to run `helm init`.

# Use helm to install package
```
$ helm search redis
$ helm install stable/redis
```
[possible issue](https://github.com/kubernetes/helm/issues/2224)</br>
After running helm init, helm list and helm install stable/nginx-ingress caused the following errors for me:
```
$ helm list
Error: configmaps is forbidden: User "system:serviceaccount:kube-system:default" cannot list configmaps in the namespace "kube-system"

$ helm install stable/nginx-ingress
Error: no available release name found
```
The following commands resolved the errors:
Give tiller the cluster-admin to avoid RBAC 
```
kubectl create serviceaccount --namespace kube-system tiller
kubectl create clusterrolebinding tiller-cluster-rule --clusterrole=cluster-admin --serviceaccount=kube-system:tiller
kubectl patch deploy --namespace kube-system tiller-deploy -p '{"spec":{"template":{"spec":{"serviceAccount":"tiller"}}}}'
```
