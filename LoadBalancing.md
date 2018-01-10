Load Balancing

- [L4 Load Balancing](#l4-load-balancing)
- [L7 Load Balancing](#l7-load-balancing)
- [config file:](#config-file)

# L4 Load Balancing
At TCP/UDP L4 level Load Balancing, this is supported out of box by kubernetes.
When you test your access to 2 replicas of web servers with the same IP:port in kubernetes, you will notice you are redirected to one of them. Load Balancing is working already.

# L7 Load Balancing
At HTTP L7 level Load Balancing, this tailored Load Balancing with HTTP address myweb.com/dev; myweb.com/test; myweb.com/prod can be achieved with helps from other apps, such HAProxy, nginx or relatively young project traefik. Here we talk only about nginx. [complete example](https://github.com/nginxinc/kubernetes-ingress/tree/master/examples/complete-example)

Kubernetes provides built‑in HTTP load balancing to route external traffic to the services in the cluster with Ingress. [NGINX and NGINX Plus](https://www.nginx.com/blog/nginx-plus-ingress-controller-kubernetes-load-balancing/) integrate with Kubernetes load balancing, fully supporting Ingress features and also providing extensions to support extended load‑balancing requirements.

For a good understanding, please watch [nginx2016](https://youtu.be/L7JZdyJ8qJQ) and [nginx2017](https://youtu.be/K-1mVPCT7SM) conf video.

kubernetes resources Ingress can be considered purely the rules in your router/firewall. To have it work, you need to get your router/firewall device and for us here is software Ingress-controller nginx(use `helm install nginx`).

nginx is also called reverse-proxy, which works in the opposite direction compared to the company proxy we normally use(forward proxy). From inside the company network we need a proxy to go on the internet, it protects and hides our IPs, etc. When a outsite client want to access website hosted in pod(internally), reverse-proxy redirects traffic to website in pod and hide the pod.
![nginx connections](https://raw.githubusercontent.com/YDD9/docker-app-hello/master/images/nginx.png)

# config file:
ingress.yml</br>
ingres-controller.yml

app-dev.yml
app-test.yml
app-prod.yml

to be continue...