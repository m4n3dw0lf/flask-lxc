#!/usr/bin/python3

from flask import request, Flask, Response, Blueprint
import lxc, uuid, json, socket, threading

lxc_api = Blueprint('lxc_api',__name__,url_prefix='/lxc')
    
@lxc_api.route('/create/<container>',methods=['POST'])
def create(container):
  try:
    config = request.json
    image = config['image']
    args = config['args']
    lxc_container = lxc.Container(container)
    if lxc_container.create(image,args=args):
        status = "success"
    else:
        status = "failed"
    response = Response(
                response=json.dumps({"status":"{}".format(status)}),
                status=200,
                mimetype='application/json'
               )
  except Exception as e:
    response = Response(
                response=json.dumps({"error":"{}".format(e)}),
                status=500,
                mimetype='application/json' 
               )
  return response

def proxy(proto,dst,sport,dport):
    def tcp_client(conn,addr,dst,dport):
        endpoint = socket.socket(2,1)
        endpoint.connect((dst,dport))
        while True:
          req = conn.recv(65535)
          if not req: break
          endpoint.send(req)
          res = endpoint.recv(65535)
          if not res: break
          conn.send(res)
        conn.close()
        endpoint.close()
    def udp_client(server,data,addr,dst,dport):
       endpoint = socket.socket(2,2)
       while True:
         endpoint.sendto(data,(dst,dport))
         d = endpoint.recvfrom(65535)
         data = d[0]
         server.sendto(data, addr)
    sport = int(sport)
    dport = int(dport)
    if proto == "tcp":
      server = socket.socket(2,1)
      server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      server.bind(("0.0.0.0",sport))
      server.listen(0)
      while True:
        conn, addr = server.accept()
        t = threading.Thread(target=tcp_client,name="tcp-proxy-{}:{}".format(dst,dport),args=[conn,addr,dst,dport])
        t.setDaemon(True)
        t.start()
    elif proto == "udp":
      server = socket.socket(2,2)
      server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      server.bind(("0.0.0.0",sport))
      while True:
        d = server.recvfrom(65535)
        data = d[0]
        addr = d[1]
        t = threading.Thread(target=udp_client,name="udp-proxy-{}:{}".format(dst,dport),args=[server,data,addr,dst,dport])
        t.setDaemon(True)
        t.start()


@lxc_api.route('/expose/<container>',methods=['POST'])
def expose(container):
  try:
    data = request.json
    lxc_container = lxc.Container(container)
    dst = str(lxc_container.get_ips()[0])
    proto= data["protocol"]
    sport = data["sport"]
    dport = data["dport"]
    t = threading.Thread(target=proxy,name="{}://{}:{}".format(proto,container,dport),args=[
                                                                                     proto,
                                                                                     dst,
                                                                                     sport,
                                                                                     dport,
                                                                                   ]
                         )
    t.setDaemon(True)
    t.start()
    response = Response(
                 response=json.dumps({"status":"success"}),
                 status=200,
                 mimetype='application/json'
               )
  except Exception as e:
    response = Response(
                response=json.dumps({"error":"{}".format(e)}),
                status=500,
                mimetype='application/json' 
               )
  return response


@lxc_api.route('/destroy/<container>',methods=['GET'])
def destroy(container):
  try:
    lxc_container = lxc.Container(container)
    if lxc_container.destroy():
      status = "success"
    else:
      status = "failed"
    response = Response(
                response=json.dumps({"status":"{}".format(status)}),
                status=200,
                mimetype='application/json'
               )
  except Exception as e:
    response = Response(
                response=json.dumps({"error":"{}".format(e)}),
                status=500,
                mimetype='application/json' 
               )
  return response  

@lxc_api.route('/start/<container>',methods=['GET'])
def start(container):
  try:
    lxc_container = lxc.Container(container)
    if lxc_container.start():
      status = "success"
    else:
      status = "failed"
    response = Response(
                response=json.dumps({"status":"{}".format(status)}),
                status=200,
                mimetype='application/json'
               )
  except Exception as e:
    response = Response(
                response=json.dumps({"error":"{}".format(e)}),
                status=500,
                mimetype='application/json'
               )
  return response

@lxc_api.route('/stop/<container>',methods=['GET'])
def stop(container): 
  try:
    lxc_container = lxc.Container(container)
    if lxc_container.stop():
      status = "success"
    else:
      status = "failed"
    response = Response(
                response=json.dumps({"status":"{}".format(status)}),
                status=200,
                mimetype='application/json'
               )
  except Exception as e:
    response = Response(
                response=json.dumps({"error":"{}".format(e)}),
                status=500,
                mimetype='application/json' 
               )
  return response

@lxc_api.route('/config/<container>',methods=["GET","POST"])
def config(container):
  try:
    lxc_container = lxc.Container(container)
    if request.method == "POST":
      data = request.json
      key = data["key"]
      value = data["value"]
      lxc_container.set_config_item(key,value)
      jdata = {key:value}
    else:
      config = {}
      for key in lxc_container.get_keys():
        try:
          value = str(lxc_container.get_config_item(key))
          config[key] = value
        except KeyError:
          continue
      jdata = config
    response = Response(
                response=json.dumps({key:value}),
                status=200,
                mimetype='application/json'
               )
  except Exception as e:
    response = Response(
                 response=json.dumps({"error":"{}".format(e)}),
                 status=500,
                 mimetype='application/json'
               )
  return response

@lxc_api.route('/list',methods=['GET'])
def list():
  try:
    container_list = {"containers":[]}
    containers = lxc.list_containers()
    for c in containers:
        container_list["containers"].append(str(c))
    response = Response(
                response=json.dumps(container_list),
                status=200,
                mimetype='application/json'
               )
  except Exception as e:
    response = Response(
                response=json.dumps({"error":"{}".format(e)}),
                status=500,
                mimetype='application/json' 
               )
  return response


