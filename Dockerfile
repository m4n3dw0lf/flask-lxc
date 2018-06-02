FROM debian:stretch

MAINTAINER Angelo Moura "m4n3dw0lf@gmail.com"

WORKDIR /app

RUN apt-get update; apt-get install -y \
                    lxc python python-pip \
                    python-lxc bridge-utils \
                    debootstrap libcap2-bin \
                    python-setuptools

COPY . .

RUN cp /app/docker_conf/default.conf /etc/lxc/default.conf ; cp /app/docker_conf/lxc-net /etc/default/lxc-net

RUN pip install -r requirements.txt

CMD ["python","run.py"]

