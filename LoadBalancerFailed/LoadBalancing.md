Load Balancing

- [L4 Load Balancing](#l4-load-balancing)
- [L7 Load Balancing](#l7-load-balancing)
- [resolve domain to your local IP](#resolve-domain-to-your-local-ip)
- [deploy controller via helm](#deploy-controller-via-helm)
- [deploy controller via image](#deploy-controller-via-image)
- [another example](#another-example)
- [config file:](#config-file)

# L4 Load Balancing
At TCP/UDP L4 level Load Balancing, this is supported out of box by kubernetes.
When you test your access to 2 replicas of web servers with the same IP:port in kubernetes, you will notice you are redirected to one of them. Load Balancing is working already.

# L7 Load Balancing
At HTTP L7 level Load Balancing, this tailored Load Balancing with HTTP address myweb.com/dev; myweb.com/test; myweb.com/prod can be achieved with helps from other apps, such HAProxy, nginx or relatively young project traefik. Here we talk only about nginx. [complete example](https://github.com/nginxinc/kubernetes-ingress/tree/master/examples/complete-example)

Kubernetes provides built‑in HTTP load balancing to route external traffic to the services in the cluster with Ingress. [NGINX and NGINX Plus](https://www.nginx.com/blog/nginx-plus-ingress-controller-kubernetes-load-balancing/) integrate with Kubernetes load balancing, fully supporting Ingress features and also providing extensions to support extended load‑balancing requirements.

Both Nginx and Kubernetes have ingress-controller, it's so confusing. I first start to use nginx-ingress-controller, then switch to ingress-nginx from k8s.

For a good understanding, please watch [nginx2016](https://youtu.be/L7JZdyJ8qJQ) and [nginx2017](https://youtu.be/K-1mVPCT7SM) conf video.

kubernetes resources Ingress can be considered purely the rules in your router/firewall. To have it work, you need to get your router/firewall device and for us here is software Ingress-controller nginx(use `kubectl apply -f ingres-controller.yml` to deploy a nginx).

nginx is also called reverse-proxy, which works in the opposite direction compared to the company proxy we normally use(forward proxy). From inside the company network we need a proxy to go on the internet, it protects and hides our IPs, etc. When a outsite client want to access website hosted in pod(internally), reverse-proxy redirects traffic to website in pod and hide the pod.
![nginx connections](https://raw.githubusercontent.com/YDD9/docker-app-hello/master/images/nginx.png)

# resolve domain to your local IP
http://xip.io/ sites gives freeDNS
```
10.0.0.1.xip.io   resolves to   10.0.0.1
www.10.0.0.1.xip.io   resolves to   10.0.0.1
mysite.10.0.0.1.xip.io   resolves to   10.0.0.1
foo.bar.10.0.0.1.xip.io   resolves to   10.0.0.1
```

# deploy controller via helm
https://medium.com/utinity/deploying-nginx-ingress-with-lets-encrypt-on-kubernetes-using-helm-a2a3b76a2e3e

# deploy controller via image
https://medium.com/@gokulc/setting-up-nginx-ingress-on-kubernetes-2b733d8d2f45

# another example
https://blogs.technet.microsoft.com/livedevopsinjapan/2017/02/28/configure-nginx-ingress-controller-for-tls-termination-on-kubernetes-on-azure-2/


# config file:
secret.yml
default-server-secret.yml

ingress.yml</br>
ingres-controller.yml

app-dev.yml
app-prod.yml

https://github.com/kubernetes/ingress-nginx#conventions

Anytime we reference a tls secret, we mean (x509, pem encoded, RSA 2048, etc). You can generate such a certificate with:
```
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout ${KEY_FILE} -out ${CERT_FILE} -subj "/CN=${HOST}/O=${HOST}"
```
and create the kubernetes.io/tls type secret via
```
kubectl create secret tls ${CERT_NAME} --key ${KEY_FILE} --cert ${CERT_FILE}
```

[A concrete example](https://github.com/kubernetes/contrib/tree/master/ingress/controllers/nginx/examples/tls#tls-certificate-termination)
```
$ openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /tmp/tls.key -out /tmp/tls.crt -subj "/CN=test.com"
$ kubectl create secret tls test-secret --key /tmp/tls.key --cert /tmp/tls.crt

$kubectl get secrets
NAME                    TYPE                                  DATA      AGE
default-server-secret   kubernetes.io/tls                     2         24m
default-token-t98hc     kubernetes.io/service-account-token   3         1d
test-secret             kubernetes.io/tls                     2         3s
```
to be continue...