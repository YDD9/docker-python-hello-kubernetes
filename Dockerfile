# simply specify image python version2, other availables are slim, version3...
FROM python:2

# set the app working path
WORKDIR /usr/src/app

# copy from current path requirements.txt
# to current path in Docker container(it is set just above WORKDIR)
# install modules for python
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# copy application to Docker container
COPY . .

# EXPOSE just document the <port=8080> used inside the app.py, but it does not have any effect.
# docker run -p <docker container port>:<port=8080> have mapping effects.
# docker run -p can publish port and affect port mapping,
# docker run -P can publish all exposed ports and map them to to high-order ports 30000.
# Dockerfile section EXPOSE https://docs.docker.com/engine/reference/builder/#expose
# Networking section https://docs.docker.com/engine/userguide/networking/#exposing-and-publishing-ports
# docker run expose port https://docs.docker.com/engine/reference/run/#expose-incoming-ports
EXPOSE 80

# run the app in Docker container
CMD [ "python", "./app.py" ]
