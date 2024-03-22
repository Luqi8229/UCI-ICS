
import json, time
from ds_protocol import extract_json_single, get_token_client
# from ui import choose_profile

class DirectMessage(dict):
    def __init__(self, ty, recipient, message, timestamp):
        self.type = ty
        self.recipient = recipient
        self.message = message
        self.timestamp = timestamp
        dict.__init__(self, type=self.type, recipient=self.recipient, message=self.message, timestamp=self.timestamp)
        # it doesn't work

class DirectMessenger:
    def __init__(self, dsuserver=None, username=None, password=None):
        self.dsuserver = dsuserver
        self.username = username
        self.password = password
        self.token = None
        self.client = None

        self.load_token()

    def load_token(self):
        try:
            self.client, response = get_token_client(self.username, self.password, self.dsuserver)
            tp = extract_json_single(response, "type")
            message = extract_json_single(response, "message")
            if tp != "ok":
                return message
            elif tp == "ok":
                self.token = extract_json_single(response, "token")
                print(message)
                return None
        except Exception:
            self.username = input("Enter your username: ")
            self.password = input("Enter your password: ")
            self.dsuserver = input("Enter your server: ")
            self.client, response = get_token_client(self.username, self.password, self.dsuserver)
            message = extract_json_single(response, "message")
            while "Invalid" in message:
                print(f'{self.username} already exists in the server.\nChoose another profile.')
                self.load_token()
            self.token = extract_json_single(response, "token")

    def send(self, message:str, recipient:str) -> bool:
        # must return true if message successfully sent, false if send failed.
        message = {"entry": message, "recipient": recipient, "timestamp": str(time.time())}
        send_msg = json.dumps({"token": self.token, "directmessage": message})
        self.client.send(send_msg.encode("utf-8"))
        response = self.client.recv(2048).decode("utf-8")
        msgType = extract_json_single(response, "type")
        if msgType == "ok":
            print(extract_json_single(response, "message"))
            return True
        return False
		
    def retrieve_new(self) -> list:
        # must return a list of DirectMessage objects containing all new messages
        send_func = json.dumps({"token":self.token, "directmessage": "new"})
        self.client.send(send_func.encode("utf-8"))

        response = self.client.recv(2048).decode("utf-8")
        history = extract_json_single(response, "messages")
        dm_list = []
        for msg in history:
            recipient = msg["from"]
            # print(f"recipient: {recipient}")
            message = msg["message"]
            # print(f"message: {message}")
            timestamp = msg["timestamp"]
            # print(f"timestamp: {timestamp}")
            dm = DirectMessage("from", recipient, message, timestamp)
            dm_list.append(dm)
        return dm_list

    def retrieve_all(self) -> list:
        # must return a list of DirectMessage objects containing all messages
        send_func = json.dumps({"token":self.token, "directmessage": "all"})
        self.client.send(send_func.encode("utf-8"))

        response = self.client.recv(2048).decode("utf-8")
        history = extract_json_single(response, "messages")
        dm_list = []
        for msg in history:
            if "entry" in msg:
                ty = "to"
                recipient = msg["recipient"]
                message = msg["entry"]
            elif "message" in msg:
                ty = "from"
                recipient = msg["from"]
                message = msg["message"]
            timestamp = msg["timestamp"]
            dm = DirectMessage(ty, recipient, message, timestamp)
            dm_list.append(dm)
        return dm_list


if __name__ == "__main__":
    messenger = DirectMessenger()
    messenger.load_token()
    print("history\n", messenger.retrieve_all())
    print("new messages\n", messenger.retrieve_new())
    if messenger.send("What's up", "getTester") is True:
        print("Messenge sent!")
    else:
        print("Messenge failed to send")