import tkinter as tk
from tkinter import ttk, filedialog
from typing import Text

class Body(tk.Frame):
    def __init__(self, root, recipient_selected_callback = None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._contacts = [str]
        self._selected_callback = recipient_selected_callback
        self._draw() #packs the widgets

    def node_select(self, event):
        index = int(self.posts_tree.selection()[0])
        entry = self._contacts[index] #friend list
        if self._selected_callback is not None:
            self._selected_callback(entry)

    def insert_contact(self, contact:str):
        self._contacts.append(contact)
        id = len(self._contacts) -1
        self._insert_contact_tree(id, contact)
    
    def _insert_contact_tree(self, id, contact:str):
        if len(contact) > 25:
            entry = contact[:24] + "..."
        id = self.posts_tree.insert('', id, id, text=contact)
    
    #display user messages
    def insert_user_message(self, message:str):
        self.entry_editor.insert(1.0, message + "\n", "entry-right")

    #display contact messages
    def insert_contact_message(self, message:str):
        self.entry_editor.insert(1.0, message + "\n", "entry-left")
    
    def get_text_entry(self) -> str:
        return self.message_editor.get("1.0", "end").rstrip()
    
    def set_text_entry(self, text:str):
        self.message_editor.delete(1.0, tk.END)
        self.message_editor.insert(1.0, text)

    def _draw(self):
        posts_frame = tk.Frame(master=self, width=250)
        posts_frame.pack(fill=tk.BOTH, side=tk.LEFT)

        self.posts_tree = ttk.Treeview(posts_frame)
        self.posts_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.posts_tree.pack(fill=tk.BOTH, side=tk.TOP, expand=True, padx=5, pady=5)

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

        self.entry_editor = tk.Text(editor_frame, width=0, height=5)
        self.entry_editor.tag_configure('entry-right', justify='right')
        self.entry_editor.tag_configure('entry-left', justify='left')
        self.entry_editor.pack(fill=tk.BOTH, side=tk.LEFT, expand=True, padx=0, pady=0)

        entry_editor_scrollbar = tk.Scrollbar(master=scroll_frame, command=self.entry_editor.yview)
        self.entry_editor["yscrollcommand"] = entry_editor_scrollbar.set
        entry_editor_scrollbar.pack(fill=tk.Y, side=tk.LEFT, expand=False, padx=0, pady=0)



class Footer(tk.Frame):
    def __init__(self, root, send_callback=None):
        tk.Frame.__init__(self,root)
        self.root = root
        self._send_callback = send_callback
        self._draw()
    
    def send_click(self):
        if self._send_callback is not None:
            self._send_callback()

    def _draw(self):
        save_button = tk.Button(master=self, text="Send", width=20)

        #TO DO: configure the button to bind its click to the send_click() function
        save_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        self.footer_label = tk.Label(master=self, text="Ready.")
        self.footer_label.pack(fill=tk.BOTH, side=tk.LEFT, padx=5)



class NewContactDialog(tk.simpledialog.Dialog):
    def __init__(self, root, title=None, user=None, pwd=None, server=None):
        self.root = root
        self.server = server
        self.user = user
        self.pwd = pwd
        super().__init__(root, title)

    def body(self, frame):
        # Creates the configuration window
        self.server_label = tk.Label(frame, width=30, text="DS Server Address")
        self.server_label.pack()
        self.server_entry = tk.Entry(frame, width=30)
        self.server_entry.insert(tk.END, self.server)
        self.server_entry.pack()

        self.username_label = tk.Label(frame, width=30, text="Username")
        self.username_label.pack()
        self.username_entry = tk.Entry(frame, width=30)
        self.username_entry.insert(tk.END, self.user)
        self.username_entry.pack()

        #TO Do password label and entry
        self.password_label = tk.Label(frame, width=30, text="Password")
        self.password_label.pack()
        self.password_entry = tk.Entry(frame, width=30)
        self.password_entry.insert(tk.END, self.user)
        self.password_entry['show'] = "*"
        self.password_entry.pack()

    def apply(self):
        self.user = self.username_entry.get()
        self.pwd = self.password_entry.get()
        self.server = self.server_entry.get()



class MainApp(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self,root)
        self.root = root
        self.username = None
        self.password = None
        self.server = None
        self.recipient = None #should only be one user at a time

        #implement directMessenger
        self.directMessenger = None

        self._draw() #pack the widgets into root frame
        self.body.insert_contact("exampleStudent")

    def send_message(self):
        #TO DO
        pass

    def add_contact(self):
        #TO DO
        #Hint: check how to use tk.simpledialog.askstring to retrive
        #the name of the new contact, and then use one of the body methods
        #to add the contact to your contact list
        pass

    def recipient_selected(self, recipient):
        self.recipient = recipient

    def configure_server(self):
        ud = NewContactDialog(self.root, "Configure Account", self.username, self.password, self.server)

        self.username = ud.user
        self.password = ud.pwd
        self.server = ud.server

        #TO DO: configure and instantiate DirectMessenger

    def publish(self, message:str):
        #To DO
        pass

    def check_new(self):
        #To Do
        pass

    def _draw(self):
        #Build menu and add to root frame
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar

        menu_file = tk.Menu(menu_bar) #File Tab
        menu_bar.add_cascade(menu=menu_file, label="File")
        menu_file.add_command(label="New")
        menu_file.add_command(label="Open...")
        menu_file.add_command(label="Close")

        settings_file = tk.Menu(menu_bar) #Setting Tab
        menu_bar.add_cascade(menu=settings_file, label="Settings")
        settings_file.add_command(label="Add Contact", command=self.add_contact)
        settings_file.add_command(label="Configure DS Server", command=self.configure_server)

        #Body and Footer class must be initalized and packed into root window
        self.body = Body(self.root, recipient_selected_callback=self.recipient_selected)
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
    id = main.after(2000, app.check_new) #updates window
    print(id)
    main.mainloop

