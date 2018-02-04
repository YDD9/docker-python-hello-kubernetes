# Dockerfile

Environment variables are notated in the Dockerfile either with `$variable_name` or `${variable_name}`. They are treated equivalently and the brace syntax is typically used to address issues with variable names with no whitespace, like `${foo}_bar`.

The `${variable_name}` syntax also supports a few of the standard bash modifiers as specified below:

`${variable:-word}` indicates that if variable is set then the result will be that value. If variable is not set then word will be the result.</br>
`${variable:+word}` indicates that if variable is set then word will be the result, otherwise the result is the empty string.</br>
In all cases, word can be any string, including additional environment variables.

Escaping is possible by adding a `\` before the variable: `\$foo` or `\${foo}`, for example, will translate to $foo and ${foo} literals respectively.

Example (parsed representation is displayed after the #):
```
FROM busybox
ENV foo /bar
WORKDIR ${foo}   # WORKDIR /bar
ADD . $foo       # ADD . /bar
COPY \$foo /quux # COPY $foo /quux
```

Environment variables are supported by the following list of instructions in the Dockerfile:
```
ADD
COPY
ENV
EXPOSE
FROM
LABEL
STOPSIGNAL
USER
VOLUME
WORKDIR
```

as well as: </br>
`ONBUILD` (when combined with one of the supported instructions above)
Note: prior to 1.4, ONBUILD instructions did NOT support environment variable, even when combined with any of the instructions listed above.

Environment variable substitution will use the same value for each variable throughout the entire instruction. In other words, in this example:
```
ENV abc=hello
ENV abc=bye def=$abc
ENV ghi=$abc
```
will result in def having a value of hello, not bye. However, ghi will have a value of bye because it is not part of the same instruction that set abc to bye.

# Understand how `CMD` and `ENTRYPOINT` interact
Both `CMD` and `ENTRYPOINT` instructions define what command gets executed when running a container. There are few rules that describe their co-operation.

Dockerfile should specify at least one of `CMD` or `ENTRYPOINT` commands.

`ENTRYPOINT` should be defined when using the container as an executable.

`CMD` should be used as a way of defining default arguments for an `ENTRYPOINT` command or for executing an ad-hoc command in a container.

`CMD` will be overridden when running the container with alternative arguments.

# Spcial trick for windows OS
https://docs.docker.com/engine/reference/builder/#shell
```
# escape=`

shell
```

# Use multiple build
https://docs.docker.com/develop/develop-images/multistage-build/

`AS builder` and `--from=builder`

```
FROM golang:1.7.3 AS builder
WORKDIR /go/src/github.com/alexellis/href-counter/
RUN go get -d -v golang.org/x/net/html
COPY app.go    .
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o app .

FROM alpine:latest
RUN apk --no-cache add ca-certificates
WORKDIR /root/
COPY --from=builder /go/src/github.com/alexellis/href-counter/app .
CMD ["./app"]
```

# apt-get
APT-GET
Probably the most common use-case for RUN is an application of apt-get. The RUN apt-get command, because it installs packages, has several gotchas to look out for.

You should avoid RUN apt-get upgrade or dist-upgrade, as many of the “essential” packages from the parent images can’t upgrade inside an unprivileged container. If a package contained in the parent image is out-of-date, you should contact its maintainers. If you know there’s a particular package, foo, that needs to be updated, use apt-get install -y foo to update automatically.

Always combine RUN apt-get update with apt-get install in the same RUN statement. For example:
```
    RUN apt-get update && apt-get install -y \
        package-bar \
        package-baz \
        package-foo
```


## List Docker CLI commands
docker
docker container --help

## Display Docker version and info
docker --version
docker version
docker info

## Excecute Docker image
docker run hello-world

## List Docker images
docker image ls

## List Docker containers (running, all, all in quiet mode)
docker container ls</br>
docker container ls -all</br>
docker container ls -a -q</br>

docker build -t friendlyhello .  # Create image using this directory's Dockerfile</br>
docker run -p 4000:80 friendlyhello  # Run "friendlyname" mapping port 4000 to 80</br>
docker run -d -p 4000:80 friendlyhello         # Same thing, but in detached mode</br>
docker container ls                                # List all running containers</br>
docker container ls -a             # List all containers, even those not running</br>
docker container stop <hash>           # Gracefully stop the specified container</br>
docker container kill <hash>         # Force shutdown of the specified container</br>
docker container rm <hash>        # Remove specified container from this machine</br>
docker container rm $(docker container ls -a -q)         # Remove all containers</br>
docker image ls -a                             # List all images on this machine</br>
docker image rm <image id>            # Remove specified image from this machine</br>
docker image rm $(docker image ls -a -q)   # Remove all images from this machine</br>
docker login             # Log in this CLI session using your Docker credentials</br>
docker tag <image> username/repository:tag  # Tag <image> for upload to registry</br>
docker push username/repository:tag            # Upload tagged image to registry</br>
docker run username/repository:tag                   # Run image from a registry</br>