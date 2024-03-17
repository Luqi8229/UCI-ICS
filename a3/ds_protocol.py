# ds_protocol.py
# protocol for exchanging messages - system of rules to transfer data

# Starter code for assignment 3 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# NAME
# EMAIL
# STUDENT ID

import json
import socket
from collections import namedtuple

# Namedtuple to hold the values retrieved from json messages.
# TODO: update this named tuple to use DSP protocol keys
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

def join(username:str, password:str, server:str, port:int):
  CODE = "utf-8"
  join_msg = '{"join": {"username": "' + username + '", "password": "' + password + '", "token":""}}'
  server_address = (server, port)

  client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  client_socket.connect(server_address)

  client_socket.send(join_msg.encode(CODE))
  responseConnect = client_socket.recv(2048).decode(CODE)
  
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
  send_msg = '{"token": "' + token + '", "post": {"entry": "' + message + '", "timestamp": "' + timeStamp + '"}}'
  client.send(send_msg.encode("utf-8"))

  responseMSG = client.recv(2048).decode("utf-8")
  print(extract_json_single(responseMSG, "message"))

def requestInput(type:str):
  ip = input(f"Please enter your {type}:\n")
  return ip


