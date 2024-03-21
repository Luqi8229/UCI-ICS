
import json, time
from ds_protocol import extract_json_single, get_token_client
from ui import choose_profile

class DirectMessage:
  def __init__(self):
    self.recipient = None
    self.message = None
    self.timestamp = None

class DirectMessenger:
  def __init__(self, dsuserver=None, username=None, password=None):
    self.dsuserver = dsuserver
    self.username = username
    self.password = password
    self.token = None
    self.client = None
    self.profile = None
    self.friends = []
    self.history = []

  def load(self):
    try:
      self.client, response = get_token_client(self.username, self.password, self.dsuserver)
      self.token = extract_json_single(response, "token")
      print(extract_json_single(response, "message"))
    except:
      self.profile = choose_profile()
      self.username = self.profile.username
      self.password = self.profile.password
      self.dsuserver = self.profile.dsuserver
      self.friends = self.profile.friends
      self.history = self.profile.history
      if self.dsuserver == None:
        self.profile.dsuserver = input("\nWhat is the server address you want to connect to:\n")
        self.dsuserver = self.profile.dsuserver
        self.profile.save_profile(str(self.profile.filepath))
      self.client, response = get_token_client(self.username, self.password, self.dsuserver)
      message = extract_json_single(response, "message")
      if "Invalid" in message:
        print(f'{self.username} already exists in the server.\nChoose another profile.')
        self.load()
      self.token = extract_json_single(response, "token")

  def send(self, message:str, recipient:str) -> bool:
    # must return true if message successfully sent, false if send failed.
    if recipient not in self.friends:
      self.friends.append(recipient)
    message = {"entry": message, "recipient": recipient, "timestamp": str(time.time())}
    send_msg = json.dumps({"token": self.token, "directmessage": message})
    self.client.send(send_msg.encode("utf-8"))
    response = self.client.recv(2048).decode("utf-8")
    msgType = extract_json_single(response, "type")
    if msgType == "ok":
      self.history.append(message)
      self.profile.save_profile(str(self.profile.filepath))
      return True
    return False
		
  def retrieve_new(self) -> list:
    # must return a list of DirectMessage objects containing all new messages
    send_func = json.dumps({"token":self.token, "directmessage": "new"})
    self.client.send(send_func.encode("utf-8"))

    response = self.client.recv(2048).decode("utf-8")
    history = extract_json_single(response, "messages")
    self.history.append(history)
    self.profile.save_profile(str(self.profile.filepath))
    return history

  def retrieve_all(self) -> list:
    # must return a list of DirectMessage objects containing all messages
    send_func = json.dumps({"token":self.token, "directmessage": "all"})
    self.client.send(send_func.encode("utf-8"))

    response = self.client.recv(2048).decode("utf-8")
    history = extract_json_single(response, "messages")
    self.history.append(history)
    self.profile.save_profile(str(self.profile.filepath))
    return history

if __name__ == "__main__":
  messenger = DirectMessenger()
  messenger.load()
  print("history\n", messenger.retrieve_all())
  print("new messages\n", messenger.retrieve_new())
  if messenger.send("What's up", "getTester") is True:
    print("Messenge sent!")
  else:
    print("Messenge failed to send")