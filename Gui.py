import tkinter as tk
from tkinter import scrolledtext, ttk
from tkinter import *
import asyncio
from typing import Concatenate
import websockets
import ssl
import pathlib
import threading
from queue import Queue
import hashlib

async def send(websocket, message):
        #print(f"Connected to server. You can now send messages.")
        #print(f"\tType /quit to leave the chat.")
        if message == "/quit":
            await websocket.close()
        await websocket.send(message)

class ChatApp:
    def __init__(self, root):
        # SSL configuration
        self.ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        self.localhostpem = pathlib.Path(__file__).with_name("localhost.pem")
        self.ssl_context.load_verify_locations(self.localhostpem)

        self.root = root


        self.root.withdraw()
        #create login window
        self.login = tk.Toplevel()
        #set title of login window
        self.login.title("Login Window")
        #self.login.resizable(width = False, height = False) 
        self.login.configure(width = 400, height = 300)
        #create server to connect to
        self.server_label = tk.Label(self.login, text = "Enter Server IP:")
        self.server_label.pack()
        #create field to input server
        self.server_entry = tk.Entry(self.login)
        self.server_entry.pack()
        #self.pls = Label(self.login, text = "Please login to continue", justify = CENTER,font = ('Arial',14))
        #create and username laebl
        self.username_label = tk.Label(self.login,text = "Username:")
        self.username_label.pack()
        #create field to put username
        self.username_entry = tk.Entry(self.login)
        self.username_entry.pack()
        #create and pack password label
        self.password_label = tk.Label(self.login,text = "Password:")
        self.password_label.pack()
        #create and place the password label and entry
        self.password_entry = tk.Entry(self.login, show= "*")
        self.password_entry.pack()
        



        

        self.loginbutton = tk.Button(self.login, text = "ATTEMPT", font = ('Arial', 14), command = self.close_login_menu)
        self.registerbutton = tk.Button(self.login, text = "Register", font = ('Arial',14), command = self.open_register_window)
        self.loginbutton.pack()
        self.registerbutton.pack()
        self.loginbutton.bind("<Return>", lambda event: self.close_login_menu)
        
        self.websocket = None
        self.username = None
        self.message_queue = Queue()
        self.receive_task = None
        self.root.after(100,self.check_messages)



    #*****************************************************************************************************************
    # this is the root stuff or the main window
        self.set_dark_theme()
        self.root.title("Change This Later")
        self.root.geometry("800x600")
        
        
        # Configure grid layout
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        self.create_widgets()
    def open_register_window(self):
        
        self.register = tk.Toplevel()
        self.register.title("Please Register")
        self.register.configure(width = 400, height = 300)
        self.user_label = tk.Label(self.register, text = "Enter Username")
        self.user_label.pack()
        self.user_entry = tk.Entry(self.register)
        self.user_entry.pack()
        self.pass_label = tk.Label(self.register,text = "Please enter Desired Pass")
        self.pass_label.pack()
        self.pass_entry = tk.Entry(self.register)
        self.pass_entry.pack()
        self.confpass_label = tk.Label(self.register, text = "Confirm Password")
        self.confpass_label.pack()
        self.confpass_entry = tk.Entry(self.register)
        self.confpass_entry.pack()
        self.registerregisterbutton = tk.Button(self.register,text = "Register", font = ('Arial',14),command = self.register_now())
        self.registerregisterbutton.pack()
    def register_now(self):
        user = self.user_entry.get()
        passw = self.pass_entry.get()
        confpassw = self.confpass_entry.get()
        if(passw != confpassw):
            self.register.title("passwords don't match")
        else:
            return
        
    def close_login_menu(self):
        server_ip = self.server_entry.get() or "localhost"
        username = self.username_entry.get()
        ppassword = self.password_entry.get()
        encoded_pass = ppassword.encode('utf-8')
        password = hashlib.sha512(encoded_pass).hexdigest()
        # Correct the thread target and arguments
        threading.Thread(
            target=self.async_connect_and_login,
            args=(server_ip, username, password),
            daemon=True
        ).start()
    def async_connect_and_login(self, server_ip, username, password):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        self.loop = loop
        try:
            self.websocket = loop.run_until_complete(self.connect_to_server(server_ip, username, password))
            
            if self.websocket:
                self.receive_task = asyncio.ensure_future(self.receive_messages())# need to figure out what the function is to receive messages
                loop.run_until_complete(self.receive_task)
        #except Exception as e:
            #self.message_queue.put(("error", f"Connection error: {str(e)}"))
        finally:
            loop.close()     



    async def connect_to_server(self, server_ip, username, password):
        server_address = f"wss://{server_ip}:8765"
        try:
            websocket = await websockets.connect( server_address, ssl=self.ssl_context )
            await websocket.send(f"{username}\n{password}")
            result = await websocket.recv()
            
            if result == "Authentication successful!":
                self.message_queue.put(("login_success", username))
                return websocket
                #self.login.destroy()
                #self.root.reiconify()
            else:
                self.message_queue.put(("error", "Login failed"))
                return None
                
        except Exception as e:
            #self.message_queue.put(("error", f"Connection error: {str(e)}"))
            return None 




    def set_dark_theme(self):
        self.bg_color = "#2d2d2d"
        self.text_bg = "#3d3d3d"
        self.user_bg = "#404040"
        self.chatter_bg = "#2d2d2d" # need to change all chatter_bg to chatter_bg
        self.text_fg = "#ffffff"
        self.root.configure(bg=self.bg_color)

    def create_widgets(self):
        # Create chat area
        self.historybig = tk.Frame(self.root, bg=self.bg_color)
        self.historybig.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # Chat history
        self.historyscroll = scrolledtext.ScrolledText(self.historybig,wrap=tk.WORD, state='disabled', bg=self.text_bg, fg=self.text_fg, insertbackground=self.text_fg, font=('Arial', 18))
        self.historyscroll.pack(expand=True, fill='both')
        
        # Input area
        self.messagearea = tk.Frame(self.root, bg=self.bg_color)
        self.messagearea.grid(row=1, column=0, sticky="ew", padx=10, pady=10)
        
        self.messageinput = ttk.Entry( self.messagearea, font=('Arial', 18), style="Dark.TEntry")
        self.messageinput.pack(side=tk.LEFT, expand=True, fill='x', padx=(0, 10))
        self.messageinput.bind("<Return>", lambda event: self.sendmessage())
        
        self.send_button = ttk.Button(self.messagearea, text="Send", command=self.sendmessage, style="Dark.TButton")
        self.send_button.pack(side=tk.RIGHT)
        
        # Configure styles
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Dark theme styles
        self.style.configure("Dark.TEntry", fieldbackground=self.text_bg, foreground=self.text_fg, insertcolor=self.text_fg, bordercolor=self.bg_color, lightcolor=self.bg_color, darkcolor=self.bg_color)
        
        self.style.configure("Dark.TButton", background="#4d4d4d", foreground=self.text_fg, bordercolor="#4d4d4d", focusthickness=3, focuscolor="#4d4d4d")
        self.style.map("Dark.TButton", background=[('active', '#5d5d5d')], foreground=[('active', self.text_fg)])
    
                
    def sendmessage(self):
        usermessage = self.messageinput.get()
        if not usermessage.strip():
            return
        
        #self.showmessage(usermessage, "user") # probably change to send asyncio stuff and names should be passed by the server
        #websocket stuff
        #if self.websocket and not self.websocket.closed:
        #if self.websocket:
            #asyncio.run_coroutine_threadsafe( self.websocket.send(usermessage), asyncio.get_event_loop())
        #send here
        if self.websocket:
            asyncio.run_coroutine_threadsafe(send(self.websocket,usermessage),self.loop)

        #send(self.websocket,usermessage)
        self.messageinput.delete(0, tk.END) # clear field after sending the message
        
        # Simulate bot response after a short delay
        #self.root.after(1000, self.generate_bot_response, usermessage)# this is just for testing 
    #able to send messages

    async def receive_messages(self):
        try:
            while True:
                message = await self.websocket.recv()
                self.message_queue.put(("message", message))
        # Simulated response - replace with actual API call
        #bot_response = f"Bot: I received your message - {messageinput[::-1]}"
        #self.showmessage(bot_response, "bot") # again person should be passed in by the server
        except Exception as e:
            #self.message_queue.put(("error", f"Connection error: {str(e)}"))
            return None         
    def showmessage(self, message, sender):
        self.historyscroll.config(state='normal')
        
        tag_name = f"{sender}_tag"
        
        self.historyscroll.tag_configure(tag_name, background=self.user_bg if sender == "user" else self.chatter_bg, foreground=self.text_fg, lmargin1=20, lmargin2=20, rmargin=20, spacing3=10, wrap=tk.WORD)
        
        self.historyscroll.insert(tk.END, "\n" + message + "\n", tag_name)
        self.historyscroll.config(state='disabled')
        
        # Auto-scroll to bottom
        self.historyscroll.see(tk.END)
    def check_messages(self):
        while not self.message_queue.empty():
            item = self.message_queue.get()
            if isinstance(item, tuple) and len(item) == 2:
                msg_type, content = item
                if msg_type == "login_success":  # Corrected message type
                    self.login.destroy()
                    self.root.deiconify()
                    self.username = content
                    self.showmessage(f"Logged in as {self.username}", "system")
                elif msg_type == "message":
                    self.showmessage(content, "other")
                elif msg_type == "error":
                    self.showmessage(content, "error")
        self.root.after(100, self.check_messages)
if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()

# alskdfalksdjf;alskdfja;lkdfja;sldkjf
