import json
import socket
from collections import namedtuple

# Namedtuple to hold the values retrieved from json messages.
DataTuple = namedtuple('DataTuple', ['type', 'message'])

def extract_json_default(json_msg:str) -> DataTuple:
  '''
  Call the json.loads function on a json string and convert it to a DataTuple object
  '''
  try:
    json_obj = json.loads(json_msg)
    type = json_obj['response']['type']
    message = json_obj['response']['message']
  except json.JSONDecodeError:
    print("Json cannot be decoded.")

  return DataTuple(type, message)

def extract_json_single(json_msg:str, type:str):
  try:
    json_obj = json.loads(json_msg)
    type = json_obj['response'][type]
  except json.JSONDecodeError:
    print("Json cannot be decoded.")

  return type

def get_token_client(username, password, server):
  client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  client_socket.connect((server, 3021))

  join_msg = json.dumps({"join": {"username":username, "password":password, "token": ""}})
  client_socket.send(join_msg.encode("utf-8"))
  responseConnect = client_socket.recv(2048).decode("utf-8")
  return client_socket, responseConnect

def join(username:str, password:str, server:str, port:int):
  client_socket, responseConnect = get_token_client(username, password, server)
  resType, resMess= extract_json_default(responseConnect)

  resToken = ""
  if resType == "ok":
    resToken = extract_json_single(responseConnect, "token")

  return client_socket, resType, resMess, resToken

def send_bio(client, token, bio, timeStamp):
  send_bio = '{"token": "' + token + '", "bio": {"entry": "' + bio + '", "timestamp": "' + timeStamp + '"}}'
  client.send(send_bio.encode("utf-8"))

  repsonseBIO = client.recv(2048).decode("utf-8")
  print(extract_json_single(repsonseBIO, "message"))

def send_post(client, token, message:str, timeStamp:str):
  send_post = '{"token": "' + token + '", "post": {"entry": "' + message + '", "timestamp": "' + timeStamp + '"}}'
  client.send(send_post.encode("utf-8"))

  responseMSG = client.recv(2048).decode("utf-8")
  print(extract_json_single(responseMSG, "message"))
