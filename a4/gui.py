import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import Text
from ds_messenger import DirectMessenger, DirectMessage
from Profile import *
import time
from pathlib import Path

class Body(tk.Frame):
    def __init__(self, root, recipient_selected_callback = None, send_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._contacts = [str]
        self.send_callback = send_callback
        self._selected_callback = recipient_selected_callback
        self._draw() #packs the widgets

    #select contact
    def node_select(self, event):
        index = int(self.posts_tree.selection()[0])
        entry = self._contacts[index] #friend list
        if self._selected_callback is not None:
            self._selected_callback(entry)

    def insert_contact(self, contact:str):
        if contact not in self._contacts:
            self._contacts.append(contact)
            id = len(self._contacts) -1
            self._insert_contact_tree(id, contact)
    
    def _insert_contact_tree(self, id, contact:str):
        if len(contact) > 25:
            entry = contact[:24] + "..."
        id = self.posts_tree.insert('', id, id, text=contact)
    
    #display user messages
    def insert_user_message(self, message:str):
        self.entry_editor.insert(tk.END, message + "\n", "entry-right")

    #display contact messages
    def insert_contact_message(self, message:str):
        self.entry_editor.insert(tk.END, message + "\n", "entry-left")
    
    def get_text_entry(self) -> str:
        return self.message_editor.get("1.0", "end").rstrip()
    
    def set_text_entry(self, text:str):
        self.message_editor.delete(1.0, tk.END)
        self.message_editor.insert(1.0, text)

    def send_click(self):
        if self.send_callback is not None:
            self.send_callback()

    def _draw(self):
        posts_frame = tk.Frame(master=self, width=250)
        posts_frame.pack(fill=tk.BOTH, side=tk.LEFT)

        self.posts_tree = ttk.Treeview(posts_frame)
        self.posts_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.posts_tree.pack(fill=tk.BOTH, side=tk.TOP, expand=False, padx=5, pady=5)

        add_button = tk.Button(posts_frame, text="Add Contact", height=2, command=self.send_callback)
        add_button.pack(fill=tk.BOTH, side=tk.TOP)

        entry_frame = tk.Frame(master=self, bg="")
        entry_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        editor_frame = tk.Frame(master=entry_frame, bg="red")
        editor_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        scroll_frame = tk.Frame(master=entry_frame, bg="blue", width=10)
        scroll_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)

        message_frame = tk.Frame(master=self, bg="yellow")
        message_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=False)

        self.message_editor = tk.Text(message_frame, width=0, height=5)
        self.message_editor.pack(fill=tk.BOTH, side=tk.LEFT, expand=True, padx=0, pady=0)

        self.entry_title = tk.Text(editor_frame, bg="gray" ,width=0, height = 1)
        self.entry_title.pack(fill=tk.BOTH, side=tk.TOP, expand=False, padx=0, pady=0)

        self.entry_editor = tk.Text(editor_frame, width=0, height=5)
        self.entry_editor.tag_configure('entry-right', justify='right')
        self.entry_editor.tag_configure('entry-left', justify='left')
        self.entry_editor.pack(fill=tk.BOTH, side=tk.LEFT, expand=True, padx=0, pady=0)

        entry_editor_scrollbar = tk.Scrollbar(master=scroll_frame, command=self.entry_editor.yview)
        self.entry_editor["yscrollcommand"] = entry_editor_scrollbar.set
        entry_editor_scrollbar.pack(fill=tk.Y, side=tk.LEFT, expand=False, padx=0, pady=0)



class Footer(tk.Frame):
    def __init__(self, root, send_callback=None, username="None"):
        tk.Frame.__init__(self,root)
        self.root = root
        self._send_callback = send_callback
        self.username = username
        self._draw()
    
    def send_click(self):
        if self._send_callback is not None:
            self._send_callback()

    def _draw(self):
        save_button = tk.Button(master=self, text="Send", width=20, command=self.send_click)
        save_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        self.footer_label = tk.Label(master=self, text="Ready.")
        self.footer_label.pack(fill=tk.BOTH, side=tk.LEFT, padx=5)
        
        self.username_label = tk.Label(master=self, text="Logged in as " + self.username)
        self.username_label.pack(fill=tk.BOTH, side=tk.LEFT, padx=100)



class NewContactDialog(tk.simpledialog.Dialog):
    def __init__(self, root, title=None, server=None, user=None, pwd=None, filepath=None):
        self.root = root
        self.server = server
        self.user = user
        self.pwd = pwd
        self.filepath = filepath
        super().__init__(root, title)

    def body(self, frame):
        #Creates the configuration window
        self.server_label = tk.Label(frame, width=30, text="DS Server Address")
        self.server_label.pack()
        self.server_entry = tk.Entry(frame, width=30)
        self.server_entry.pack()

        self.filepath_label = tk.Label(frame, width=30, text="Folder Directory")
        self.filepath_label.pack()
        self.filepath_entry = tk.Entry(frame, width=30)
        self.filepath_entry.pack()

        self.username_label = tk.Label(frame, width=30, text="Username")
        self.username_label.pack()
        self.username_entry = tk.Entry(frame, width=30)
        self.username_entry.pack()

        self.password_label = tk.Label(frame, width=30, text="Password")
        self.password_label.pack()
        self.password_entry = tk.Entry(frame, width=30)
        self.password_entry['show'] = "*"
        self.password_entry.pack()

    def apply(self):
        self.server = self.server_entry.get()
        self.user = self.username_entry.get()
        self.pwd = self.password_entry.get()
        self.filepath = self.filepath_entry.get()

class MainApp(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self,root)
        self.root = root
        self.username = None
        self.password = None
        self.server = None
        self.recipient = None #should only be one user at a time
        self.filepath = None
        self.profile = Profile()
        self.directMessenger = None #loaded in load_file

        self._draw() #pack the widgets into root frame

    def configure_server(self):
        self.server = tk.simpledialog.askstring("Server Address", "Please enter the server you want to connect to")

    def load_screen(self):
        self.footer.destroy()
        self.footer = Footer(self.root, send_callback=self.send_message, username=self.username)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)
        
        print(f'Logged in as {self.username}')
        self.show_contacts()
        
        main.after(2000, app.check_new) #updates window

    def get_info(self, title):
        ud = NewContactDialog(self.root, title, self.username, self.password, self.filepath)
        # self.server = ud.server
        # self.username = ud.user
        # self.password = ud.pwd
        # self.filepath = Path(ud.filepath)
        self.server = "168.235.86.101"
        self.username = "Cyro"
        self.passwrod = "Slimes"
        self.filepath = Path("C:\\Users\\luqip\\uciWork\\a4\\Cyro.dsu")
        
    def new_file(self):
        self.get_info("Create New Profile")
        fileName = self.username + ".dsu"
        self.filepath = Path(self.filepath) / fileName
        self.filepath.touch()
        self.profile = Profile(self.server, str(self.filepath), self.username, self.password)
        self.profile.save_profile(str(self.filepath))
        self.directMessenger = DirectMessenger(self.server, self.username, self.password)
        self.directMessenger.load_token()
        self.load_screen()

    def open_file(self):
        self.get_info("Login into Profile")
        if self.filepath.exists() is True and self.filepath.name == self.username + ".dsu":
            self.profile.load_profile(str(self.filepath))
            self.username = self.profile.username
            self.password = self.profile.password
            self.filepath = Path(self.profile.filepath)
            
            self.directMessenger = DirectMessenger(self.server, self.username, self.password)
            self.directMessenger.load_token()
            self.load_screen()
            messagebox.showinfo("Profile Loaded", f"Profile {self.username} has been loaded succesfully")
        else:
            print("ERROR: profile does not exist")
            messagebox.showerror("File Not Found", f'Profile {self.username} does not exist. \nCreate a new file.')
    
    def recipient_selected(self, recipient):
        self.recipient = recipient
        self.body.entry_editor.delete(1.0, tk.END)
        self.body.entry_title.delete(1.0, tk.END)
        self.body.entry_title.insert(1.0, self.recipient, "entry-left")
        
        all_dms = self.directMessenger.retrieve_all()
        recp_dm = self.directMessenger.recipient_history(self.recipient, all_dms)
        self.loop_messages(recp_dm)
        
        prof_history = self.profile.history[self.recipient]
        dm_history = self.combine_history(prof_history, recp_dm)
        self.loop_messages(dm_history)
        chatHistory = sorted(dm_history, key=lambda x: float(x["timestamp"]))
        
        new_history = self.directMessenger.retrieve_new()
        new_dm = self.directMessenger.recipient_history(self.recipient, new_history)
        print("History")
        self.load_chat(chatHistory)
        print("New")
        self.load_chat(new_dm)

    def send_message(self):
        message = self.body.get_text_entry()
        if message.strip() != " " and self.recipient != None:
            if self.directMessenger.send(message, self.recipient) is True:
                self.body.insert_user_message(message)
                self.body.set_text_entry("")
                dm = DirectMessage("to", self.recipient, message, str(time.time()))
                print(f'Message Sent to {dm.recipient}: {dm.message} @ {dm.timestamp}')
                self.profile.add_message(dm)
                self.profile.save_profile(str(self.filepath))
                
    def combine_history(self, lst1, lst2):
        for dm in lst1:
            if dm not in lst2:
                lst2.append(dm)
        return lst2
    
    def load_chat(self, lst:list):
        if len(lst) > 0:
            for dm in lst:
                if self.recipient == dm["recipient"]:
                    self.print_message(dm)
                    if dm["type"] == "to":
                        self.body.insert_user_message(dm["message"])
                    elif dm["type"] == "from":
                        self.body.insert_contact_message(dm["message"])
                    self.profile.add_message(dm)
                    self.profile.save_profile(self.filepath)
        else:
            print("No messages")

    def add_contact(self):
        contact = tk.simpledialog.askstring("Add Contact", "Enter the name of your new contact")
        if len(contact) > 0:
            self.body.insert_contact(contact)
            self.profile.add_friend(contact)
            print(f'added {contact}')
            self.profile.save_profile(str(self.filepath))

    def loop_messages(self, lst):
        if len(lst) > 0:
            for dm in lst:
                self.print_message(dm)

    def print_message(self, msg):
            print(f'{msg["type"].capitalize()} {msg["recipient"]} "{msg["message"]}" @ {msg["timestamp"]}')
    
    def show_contacts(self):
        friendList = self.profile.friends
        for person in friendList:
            print(f"show {person}")
            self.body.insert_contact(person)

    def check_new(self):
        self.root.after(2000, self.check_new)
        dm_list = self.directMessenger.retrieve_new()
        if dm_list != []:
            self.load_chat(dm_list)

    def _draw(self):
        #Build menu and add to root frame
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar

        profile_tab = tk.Menu(menu_bar) #Profile Tab
        menu_bar.add_cascade(menu=profile_tab, label="Profile")
        profile_tab.add_command(label="New", command=self.new_file)
        profile_tab.add_command(label="Open...", command=self.open_file)
        
        settings_file = tk.Menu(menu_bar) #Setting Tab
        menu_bar.add_cascade(menu=settings_file, label="Settings")
        settings_file.add_command(label="Add Contact", command=self.add_contact)
        settings_file.add_command(label="Configure DS Server", command=self.configure_server)

        #Body and Footer class must be initialized and packed into root window
        self.body = Body(self.root, recipient_selected_callback=self.recipient_selected, send_callback=self.add_contact)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        self.footer = Footer(self.root, send_callback=self.send_message)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)

if __name__ == "__main__":
    main = tk.Tk() #creates root window
    main.title("ICS 32 Distributed Social Messenger") #title of window
    main.geometry("720x480") #size of window
    main.option_add('*tearOff', False)
    
    app = MainApp(main) #creates window
    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())
    main.mainloop()

