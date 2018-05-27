# Flask LXC API Blueprint 

<br>

## Requirements

### Install LXC

- Debian 9 (Jessie) Setup

```
sudo apt-get install -y lxc python-lxc

echo 'USE_LXC_BRIDGE="true"' | sudo tee /etc/default/lxc-net

sudo bash -c 'cat << EOF > /etc/lxc/default.conf
lxc.network.type = veth
lxc.network.link = lxcbr0
lxc.network.flags = up
lxc.network.hwaddr = 00:16:3e:a1:b2:c3
EOF'

sudo service lxc-net restart
```

## Running locally

```
git clone https://github.com/m4n3dw0lf/flask-lxc
sudo pip install -r requirements.txt
sudo python run.py
```

## Importing as blueprint on your flask app

- install the package

```
pip install flask_lxc
```

- register the blueprint

```
from flask import Flask
from flask_lxc import lxc_api

# Can be your own app
app = Flask(__name__)
app.register_blueprint(lxc_api)
```

<br><br>

## API

### Create new LXC Container

syntax:

```
curl -X POST \
http://localhost:5000/lxc/create/<CONTAINER> \
-H "Content-Type:application/json" \
-d '{
 "image":"<IMAGE>",
 "args":{
   "release":"<RELEASE>",
   "arch":"<ARCH>"
 }
}'
```

example:

```
curl -X POST \
http://localhost:5000/lxc/create/debian1 \
-H "Content-Type:application/json" \
-d '{
 "image":"debian",
 "args":{
   "release":"jessie",
   "arch":"amd64"
 }
}'
```

<br>

### List LXC Containers

syntax:

`curl http://localhost:5000/lxc/list`

<br>

### Start LXC Container

syntax:

`curl http://localhost:5000/lxc/start/<CONTAINER_NAME>`

example:

`curl http://localhost:5000/lxc/start/debian1`

<br>

### Stop LXC Container

syntax:

`curl http://localhost:5000/lxc/stop/<CONTAINER_NAME>`

example:

`curl http://localhost:5000/lxc/stop/debian1`

<br>

### Destroy LXC Container

syntax:

`curl http://localhost:5000/lxc/destroy/<CONTAINER_NAME>`

example:

`curl http://localhost:5000/lxc/destroy/debian1`

<br>

### Expose port of the container

syntax:

```
curl -X POST \
http://localhost:5000/lxc/expose/<CONTAINER_NAME> \
-H "Content-Type:application/json" \
-d '{
  "sport":"<PORT_TO_EXPOSE>",
  "dport":"<CONTAINER_PORT>",
  "protocol":"<PROTOCOL>"
}'
```

example:

```
curl -X POST \
http://localhost:5000/lxc/expose/debian1 \
-H "Content-Type:application/json" \
-d '{
  "sport":"80",
  "dport":"80",
  "protocol":"tcp"
}'
```

### Get config keys

syntax:

`curl http://localhost:5000/lxc/config/<CONTAINER>`

example:

`curl http://localhost:5000/lxc/config/debian1`

### Set config keys

syntax:
```
curl -X POST \
http://localhost:5000/lxc/config/<CONTAINER> \
-H "Content-Type:application/json" \
-d '{
  "<KEY>":"<VALUE>"
}'
```

example:

```
curl -X POST \
http://localhost:5000/lxc/config/debian1 \
-H "Content-Type:application/json" \
-d '{
  "lxc.network":"veth"
}'
```

<br><br>

## Reference

Instructions to setup LXC and LXC Networking for Debian Jessie

- https://wiki.debian.org/LXC
