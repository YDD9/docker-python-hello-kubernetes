Nginx Ingress Controller steps
http://rahmonov.me/posts/nginx-ingress-controller/

In above example cluster is in cloud, you can have a public IP for your
ingress-nginx-controller service, so `type: LoadBalancer` is used. But mine are based in VMs and not possible to have public IP, so create service with `--type=NodePort`, but still no IP:
```
root@node3: kubectl expose deploy nginx-ingress-controller -n ingress-nginx --target-port=80 --type=NodePort

root@node3:/media# kubectl get svc --namespace=ingress-nginx
NAME                       TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)                      AGE
default-http-backend       ClusterIP   10.111.36.0      <none>        80/TCP                       1d
nginx-ingress-controller   NodePort    10.107.152.204   <none>        80:30692/TCP,443:30672/TCP   23s

# here IP is your work node IP where controller runs
root@node3: curl -v 192.168.0.45:30692

```

To solve this IP issue, you can give a fake IP 192.168.0.250 for example,
and force it as external IP. https://github.com/kubernetes/kube-deploy/issues/220
```
kind: Service
apiVersion: v1
metadata:
  name: ingress-nginx
  namespace: ingress-nginx
  labels:
    app: ingress-nginx
spec:
  externalTrafficPolicy: Local
  type: LoadBalancer
  externalIPs:
  - 192.168.0.250
  selector:
    app: ingress-nginx
  ports:
  - name: http
    port: 80
    targetPort: http
  - name: https
    port: 443
    targetPort: https
```

After apply this svc, you can see
```
root@node3:/media# kubectl get svc --namespace=ingress-nginx
NAME                   TYPE           CLUSTER-IP      EXTERNAL-IP     PORT(S)                      AGE
default-http-backend   ClusterIP      10.111.36.0     <none>          80/TCP                       2d
ingress-nginx          LoadBalancer   10.99.174.227   192.168.0.250   80:31614/TCP,443:31153/TCP   14m
```

Enter your site address with ip in C:\Windows\System32\drivers\etc\hosts file for win10
```
192.168.0.250	test.com
```

Get into the pod of ingress-nginx-controller to check nginx config, flush current DNS `ipconfig /flushdns`
```
 ## start server 192.168.0.45.xip.io
    server {
        server_name 192.168.0.45.xip.io ;

        listen 80;

        listen [::]:80;

        set $proxy_upstream_name "-";

        listen 443  ssl http2;

        listen [::]:443  ssl http2;

        ...
    location /prod {

                set $proxy_upstream_name "";

                set $namespace      "default";
                set $ingress_name   "test";
                set $service_name   "prod-svc";
        ...
    location /dev {

            set $proxy_upstream_name "";

            set $namespace      "default";
            set $ingress_name   "test";
            set $service_name   "dev-svc";

            # enforce ssl on server side
            if ($pass_access_scheme = http)
        ...
```

win10

ingress service type choose
http://www.devoperandi.com/load-balancing-in-kubernetes/
External –

Services can also act as external load balancers if you wish through a NodePort or LoadBalancer type.

NodePort will expose a high level port externally on every node in the cluster. By default somewhere between 30000-32767. When scaling this up to 100 or more nodes, it becomes less than stellar. Its also not great because who hits an application over high level ports like this? So now you need another external load balancer to do the port translation for you. Not optimal.

LoadBalancer helps with this somewhat by creating an external load balancer for you if running Kubernetes in GCE, AWS or another supported cloud provider. The pods get exposed on a high range external port and the load balancer routes directly to the pods. This bypasses the concept of a service in Kubernetes, still requires high range ports to be exposed, allows for no segregation of duties, requires all nodes in the cluster to be externally routable (at minimum) and will end up causing real issues if you have more than X number of applications to expose where X is the range created for this task.

Because services were not the long-term answer for external routing, some contributors came out with Ingress and Ingress Controllers. This in my mind is the future of external load balancing in Kubernetes. It removes most, if not all, the issues with NodePort and Loadbalancer, is quite scalable and utilizes some technologies we already know and love like HAproxy, Nginx or Vulcan. So lets take a high level look at what this thing does.

Using Kubernetes Ingress Controller from scratch
https://medium.com/@samwalker505/using-kubernetes-ingress-controller-from-scratch-35faeee8eca



http://alesnosek.com/blog/2017/02/14/accessing-kubernetes-pods-from-outside-of-the-cluster/

https://medium.com/@gokulc/setting-up-nginx-ingress-on-kubernetes-2b733d8d2f45

https://blogs.technet.microsoft.com/livedevopsinjapan/2017/02/28/configure-nginx-ingress-controller-for-tls-termination-on-kubernetes-on-azure-2/

http://blog.wercker.com/troubleshooting-ingress-kubernetes
