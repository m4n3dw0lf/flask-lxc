# Flask LXC API Blueprint 

<br>

## Requirements

#### Install LXC

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

<br><br>

## API

#### Create new LXC Container

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

#### List LXC Containers

`curl http://localhost:5000/lxc/list`

<br>

#### Start LXC Container

`curl http://localhost:5000/lxc/start/<CONTAINER_NAME>`

example:

`curl http://localhost:5000/lxc/start/debian1`

<br>

#### Stop LXC Container

`curl http://localhost:5000/lxc/stop/<CONTAINER_NAME>`

example

`curl http://localhost:5000/lxc/stop/debian1`

<br>

#### Destroy LXC Container

`curl http://localhost:5000/lxc/destroy/<CONTAINER_NAME>`

example

`curl http://localhost:5000/lxc/destroy/debian1`

<br>
<br>

#### Expose ports of the container

> Add the following rule to the iptables: `sudo iptables -t nat -A POSTROUTING -s 10.0.3.0/24 -o eth0 -j MASQUERADE`

```
curl -X POST \
http://localhost:5000/lxc/expose/<CONTAINER_NAME> \
-H "Content-Type:application/json" \
-d '{
  "dst":"<CONTAINER_IP>",
  "port":"<PORT_TO_EXPOSE>",
  "protocol":"<PROTOCOL>"
}'
```

example

```
curl -X POST \
http://localhost:5000/lxc/expose/debian1 \
-H "Content-Type:application/json" \
-d '{
  "dst":"10.0.3.216",
  "port":"80",
  "protocol":"tcp"
}'
```

## Reference

Instructions to setup LXC and LXC Networking for Debian Jessie

- https://wiki.debian.org/LXC
