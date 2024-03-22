
import time, ui, ds_protocol
from ds_messenger import *
from Profile import *

def send(profile, admin):
  '''
  The send function joins a ds server and sends a message, bio, or both

  :param server: The ip address for the ICS 32 DS server.
  :param port: The port where the ICS 32 DS server is accepting connections.
  :param username: The user name to be assigned to the message.
  :param password: The password associated with the username.
  :param message: The message to be sent to the server.
  :param bio: Optional, a bio for the user.
  '''
  ############# Connecting to the Server ##################################
  # server = profile.dsuserver
  server = "168.235.86.101"
  if server is None:
    server = ui.prompt_info("What is the server you want to connect to?", str=True)
    profile.dsuserver = server
    profile.save_profile(str(profile.filepath))
  port = 3021
  username = profile.username
  password = profile.password

  client, resType, resMess, resToken = ds_protocol.join(username, password, server, port)
  print("\n" + resMess)

  #################################################3

  if resType == "ok":
    # publishAns = ui.yes_or_no("Would you like to publish your profile")

    # if publishAns == "yes":
    #   post_option(client, resToken, profile)

    messAns = ui.yes_or_no("Would you like to go into your messages")
    if messAns == "yes":
      user = DirectMessenger(server, username, password)
      user.client = client
      user.token = resToken
      send_message(profile, user)
    
    client.close()
    return True

  client.close()
  
  return False

############################# End of Send #############################

def print_messages(info):
  for msg in info:
    print(f'From {msg.recipient} "{msg.message}" @ {msg.timestamp}')

def send_message(profile, user, repeating=False):
  print("Messages")
  print_messages(user.retrieve_all())
  print("New Messages:")
  print_messages(user.retrieve_new())
  
  if repeating is False:
    sendAns = ui.yes_or_no("Would you like to send a message")
    while sendAns == "yes":
      recipient = input("Who is your recipient?")
      message = input("What is your message?")
      direct_msg = DirectMessage("to", recipient,message, time.time())
      if user.send(message, recipient) is True:
        profile.add_message(str(recipient), direct_msg)
        profile.save_profile(str(profile.filepath))

        all = user.retrieve_all()
        print("All messages: ", all)
      sendAns = ui.yes_or_no("Would you like to send another message")
  ui.aline("Returning to publish command...")

def post_option(client, token, profile, repeating = False):
  ui.run_post_menu()
  option = ui.prompt_info("What would you like to post", str=False, command=True, option = "post")
  for elm in option:
    if elm == "bio":
      post_bio(client, token, profile)
    elif elm == "posts":
      post_post(client, token, profile)
  
  if repeating is False:
    againAns = ui.yes_or_no("Would you like to post something else")
    if againAns == "yes":
      post_option(client, token, profile, True)
    ui.aline("Returing to publish command...")
  
def post_bio(client, token, profile):
  if profile.bio != None:
    ds_protocol.send_bio(client, token, profile.bio, str(time.time()))
  else:
    ui.aline("Your bio is empty.")
    createAns = ui.yes_or_no("Would you like to add a bio")
    if createAns == "yes":
      profile.bio = ui.get_entry("Please enter your new bio")
      profile.save_profile(str(profile.filepath))
  ui.aline("Returning to post command...")

def post_post(client, token, profile):
  post = ui.choose_post(profile)
  if post != None:
    message = str(post.get_entry())
    timeStamp = str(post.get_time())
    ds_protocol.send_post(client, token, message, timeStamp)
    continue_posting(client, token, profile)
  ui.aline("Returning to post command...")


def continue_posting(client, token, profile):
  postAnother = ui.yes_or_no("Would you like to post another")

  if postAnother == "yes":
    print("\nEnter 'list' to see your list of posts.")
    print("Enter 'create' to create a new post.")
    print("Enter 'stop' to stop posting.")
    message = input("\nEnter the index of the next post:\n")

    while message.lower() != "stop":
      index = int(message)
      while index not in range(len(profile._posts)+1):
        index = int(ui.prompt_info("Invalid index, try again", str=True))

      if message.isnumeric():
        postTP = profile.get_post_by_ID(index-1)
        post_entry = postTP.get_entry()
        ds_protocol.send_post(client, token, post_entry, str(postTP.get_time()))
      elif message.lower() == "list":
        print(ui.index_all_posts(profile._posts))
      elif message.lower() == "create":
        ui.create_post(profile)
      else:
        print("Invalid index.")
    
      message = input("\nEnter the index of the next post:\n")
