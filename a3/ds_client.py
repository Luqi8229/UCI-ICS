# Starter code for assignment 3 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# NAME
# EMAIL
# STUDENT ID

import ds_protocol
import time
import ui
import mc
from Profile import *

def send(server:str, port:int, username:str, password:str, message:str, bio:str=None):
  '''
  The send function joins a ds server and sends a message, bio, or both

  :param server: The ip address for the ICS 32 DS server.
  :param port: The port where the ICS 32 DS server is accepting connections.
  :param username: The user name to be assigned to the message.
  :param password: The password associated with the username.
  :param message: The message to be sent to the server.
  :param bio: Optional, a bio for the user.
  '''
  #TODO: return either True or False depending on results of required operation
  
  CODE = 'utf-8'

  filePath = ui.choose_profile()
  profile = Profile()
  profile.load_profile(filePath)
  
  server = profile.dsuserver
  username = profile.username
  password = profile.password
  bio = profile.bio

  client, resType, resMess, resToken = ds_protocol.join(username, password, server, port)
  print(resMess)

  if resType == "ok":
    timeStamp = str(time.time()) #for empty Profile

    if bio != None:
      publishBio = ui.yes_or_no(f"Would you like to publish your bio [{bio}]")
      if publishBio.lower() == "yes":
        ds_protocol.send_bio(client, resToken, bio, timeStamp)

    post = mc.publish_post_command(filePath)
    if post != None:
      message = str(post.get_entry())
      timeStamp = str(post.get_time())
      ds_protocol.send_post(client, resToken, message, timeStamp)
      continue_posting(client, resToken, filePath)
    
    client.close()
    return True

  client.close()
  
  return False

def continue_posting(client, token, filePath):
  profile = Profile()
  profile.load_profile(str(filePath))
  another_post = input("\nWould you like to post another? (yes/no): ")

  if another_post.lower() == "yes":
    print("\nEnter 'list' to see your list of posts.")
    print("Enter 'create' to create a new post.")
    print("Enter 'stop' to stop posting.")
    message = input("\nEnter the index of the next post:\n")

    while message.lower() != "stop":
      index = int(message)
      while index not in range(len(profile._posts)+1):
        index = int(ui.prompt_info("Invalid index, try again", True))
      if message.isnumeric():
        profile = Profile()
        profile.load_profile(filePath)
        postTP = profile.get_post_by_ID(index-1)
        post_entry = postTP.get_entry()
        if ui.confirm_publish(post_entry) is True:
          ds_protocol.send_post(client, token, post_entry, str(postTP.get_time()))
      elif message.lower() == "list":
        print(ui.index_all_posts(profile._posts))
      elif message.lower() == "create":
        ui.create_post(filePath)
      else:
        print("Invalid index.")
      message = input("\nEnter the index of the next post:\n")

def requestInput(type:str):
  ip = input(f"Please enter your {type}:\n")
  return ip
