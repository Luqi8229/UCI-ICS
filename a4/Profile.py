# Profile.py
#
# ICS 32
# Assignment #2: Journal
#
# Author: Mark S. Baldwin, modified by Alberto Krone-Martins
#
# v0.1.9

# You should review this code to identify what features you need to support
# in your program for assignment 2.
#
# YOU DO NOT NEED TO READ OR UNDERSTAND THE JSON SERIALIZATION ASPECTS OF THIS CODE 
# RIGHT NOW, though can you certainly take a look at it if you are curious since we 
# already covered a bit of the JSON format in class.
#
import json, time
from pathlib import Path
from ds_messenger import DirectMessage


"""
DsuFileError is a custom exception handler that you should catch in your own code. It
is raised when attempting to load or save Profile objects to file the system.

"""
class DsuFileError(Exception):
    pass

"""
DsuProfileError is a custom exception handler that you should catch in your own code. It
is raised when attempting to deserialize a dsu file to a Profile object.

"""
class DsuProfileError(Exception):
    pass


class Post(dict):
    """ 

    The Post class is responsible for working with individual user posts. It currently 
    supports two features: A timestamp property that is set upon instantiation and 
    when the entry object is set and an entry property that stores the post message.

    """
    def __init__(self, entry:str = None, timestamp:float = 0):
        self._timestamp = timestamp
        self.set_entry(entry)

        # Subclass dict to expose Post properties for serialization
        # Don't worry about this!
        dict.__init__(self, entry=self._entry, timestamp=self._timestamp)
    
    def set_entry(self, entry):
        self._entry = entry 
        dict.__setitem__(self, 'entry', entry)

        # If timestamp has not been set, generate a new from time module
        if self._timestamp == 0:
            self._timestamp = time.time()

    def get_entry(self):
        return self._entry
    
    def set_time(self, time:float):
        self._timestamp = time
        dict.__setitem__(self, 'timestamp', time)
    
    def get_time(self):
        return self._timestamp

    """

    The property method is used to support get and set capability for entry and 
    time values. When the value for entry is changed, or set, the timestamp field is 
    updated to the current time.

    """ 
    entry = property(get_entry, set_entry)
    timestamp = property(get_time, set_time)
    
    
class Profile:
    """
    The Profile class exposes the properties required to join an ICS 32 DSU server. You 
    will need to use this class to manage the information provided by each new user 
    created within your program for a2. Pay close attention to the properties and 
    functions in this class as you will need to make use of each of them in your program.

    When creating your program you will need to collect user input for the properties 
    exposed by this class. A Profile class should ensure that a username and password 
    are set, but contains no conventions to do so. You should make sure that your code 
    verifies that required properties are set.

    """

    def __init__(self, dsuserver=None, filepath=None, username=None, password=None, bio=None, posts=[], friends=[], history={}):
        self.dsuserver = dsuserver # REQUIRED
        self.filepath = filepath
        self.username = username # REQUIRED
        self.password = password # REQUIRED
        self.bio = bio # OPTIONAL
        self._posts = posts # OPTIONAL
        self.friends = friends
        self.history = history
    
    def add_history(self, dm):
        print(f'history to add {dm}')
        if dm not in self.history[dm["recipient"]]:
            self.history[dm["recipient"]].append(dm)
            print(f'history added {dm}')
    
    def add_friend(self, contact):
        if contact not in self.friends:
            self.friends.append(contact)
            self.history[contact] = []

    def add_message(self, msg: DirectMessage) -> None:
        self.add_friend(msg["recipient"])
        self.add_history(msg)

    def add_post(self, post: Post) -> None:
        self._posts.append(post)

    def del_post(self, index: int) -> bool:
        try:
            del self._posts[index-1]
            return True
        except IndexError:
            return False
        
    def get_posts(self) -> list[Post]:
        return self._posts
    
    def get_post_by_ID(self, id:int):
        return self._posts[id]

    def save_profile(self, path: str) -> None:
        p = Path(path)
        if p.exists() and p.suffix == '.dsu':
            try:
                f = open(p, 'w')
                json.dump(self.__dict__, f)
                f.close()
            except Exception as ex:
                raise DsuFileError("Error while attempting to process the DSU file.", ex)
        else:
            raise DsuFileError("Invalid DSU file path or type")

    def load_profile(self, path:str) -> None:
        p = Path(path)

        if p.exists() and p.suffix == '.dsu':
            try:
                f = open(p, 'r')
                obj = json.load(f)
                self.filepath = obj['filepath']
                self.username = obj['username']
                self.password = obj['password']
                self.dsuserver = obj['dsuserver']
                self.bio = obj['bio']
                self.history = {}
                for fred in obj['history']:
                    if fred not in self.friends:
                        self.friends.append(fred)
                        self.history[fred] = []
                    for rec in obj["history"][fred]:
                        if rec not in self.history[fred]:
                            self.history[fred].append(rec)
                self._posts = []
                for post_obj in obj['_posts']:
                    post = Post(post_obj['entry'], post_obj['timestamp'])
                    self._posts.append(post)
                f.close()
            except Exception as ex:
                raise DsuProfileError(ex)
        else:
            raise DsuFileError()
