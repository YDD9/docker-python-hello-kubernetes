**A Docker Hello World! APP written in Python Flask**
To explore Docker technology and VirtualBox, together with testing for NAT and Bridge network settings.
(Next step is to deploy this dokcer APP with Kubernetes.)

- [setup](#setup)
- [requirements.txt python packages specification](#requirementstxt-python-packages-specification)
- [Dockerfile](#dockerfile)
- [build your image](#build-your-image)
- [run your app in Docker](#run-your-app-in-docker)
- [verify in browser](#verify-in-browser)
- [variations test](#variations-test)
- [push docker images to dockerhub for easy usages on other PCs](#push-docker-images-to-dockerhub-for-easy-usages-on-other-pcs)
- [save docker images locally and import for use](#save-docker-images-locally-and-import-for-use)


# setup
host: win10 + VirtualBox5.2 (network NAT)
guest: Debian9.3 Linux (run inside VirtualBox) + python2.7 + pipreqs
        docker container 17.03.0-ce: run inside Debian Linux

**All below steps are done inside the guest Debian Linux unless specified.**

# requirements.txt python packages specification
Generate a packages specification based on your project import, not used packages will be ignored.
Better to use `pip freeze` when you have an virtual env for your project.
```
$ pip install pipreqs
$ pipreqs --force 'C:\Users\ydd9\Documents\PythonHelloDockerK8s'
```

# Dockerfile
open dockerhub website to find a Linux image with python and follow the Dockerfile template there.
Dockerfile is used to build an image for you

# build your image
```
$ cd PythonHelloDockerK8s
$ docker build ./ -t ydd9/python-hello
```

# run your app in Docker
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

# verify in browser
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

# variations test

docker container will run at high number port, you still can check in Debian the display "Hello World!", but in win10, guest host needs to reconfig to be able to display.
```
$ docker run -p 8080 ydd9/python-hello
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


# push docker images to dockerhub for easy usages on other PCs
https://docs.docker.com/docker-cloud/builds/push-images/
```
$ export DOCKER_ID_USER="username"
$ docker login
$ docker tag my_image $DOCKER_ID_USER/my_image
$ docker push $DOCKER_ID_USER/my_image
# verify in docker hub
```

# save docker images locally and import for use
```
$ docker save my_image > my_image.tar

$ docker load --input my_image.tar
```



