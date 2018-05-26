#!/usr/bin/python3

from flask import request, Flask, Response, Blueprint
import lxc, uuid, json

container = Blueprint('lxc',__name__,url_prefix='/lxc')

@container.route('/create/<container>',methods=['POST'])
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

@container.route('/destroy/<container>',methods=['GET'])
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

@container.route('/start/<container>',methods=['GET'])
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

@container.route('/stop/<container>',methods=['GET'])
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






