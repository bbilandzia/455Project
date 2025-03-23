import tkinter as tk
from tkinter import scrolledtext, ttk
from tkinter import *
class ChatApp:
    def __init__(self, root):
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
        self.password_entry = tk.Entry(self.login)
        self.password_entry.pack()
        

        self.loginbutton = tk.Button(self.login, text = "ATTEMPT", font = ('Arial', 14), command = self.close_login_menu)
        self.loginbutton.pack()






    #*****************************************************************************************************************
    # this is the root stuff or the main window
        self.set_dark_theme()
        self.root.title("Change This Later")
        self.root.geometry("800x600")
        
        
        # Configure grid layout
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        self.create_widgets()
    
    def close_login_menu(self):
        #compare pass against pass of user selected
        #grab the user and pass from the login text boxes
        user = self.username_entry.get()
        passwordstuff = self.password_entry.get()
        correct = True
        if( correct == True):
            #self.password_entry.delete(0,tk.END)
            self.login.destroy()
            self.root.deiconify()
        #if correct
        #clear fields
        #closes login window
        #unhides root
    
    def set_dark_theme(self):
        self.bg_color = "#2d2d2d"
        self.text_bg = "#3d3d3d"
        self.user_bg = "#404040"
        self.bot_bg = "#2d2d2d" # need to change all bot_bg to chatter_bg
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
        
        self.showmessage(usermessage, "user") # probably change to send asyncio stuff and names should be passed by the server
        self.messageinput.delete(0, tk.END) # clear field after sending the message
        
        # Simulate bot response after a short delay
        self.root.after(1000, self.generate_bot_response, usermessage)# this is just for testing 
        
    def generate_bot_response(self, messageinput):
        # Simulated response - replace with actual API call
        bot_response = f"Bot: I received your message - {messageinput[::-1]}"
        self.showmessage(bot_response, "bot") # again person should be passed in by the server
        
    def showmessage(self, message, sender):
        self.historyscroll.config(state='normal')
        
        tag_name = f"{sender}_tag"
        self.historyscroll.tag_configure(tag_name, background=self.user_bg if sender == "user" else self.bot_bg, foreground=self.text_fg, lmargin1=20, lmargin2=20, rmargin=20, spacing3=10, wrap=tk.WORD)
        
        self.historyscroll.insert(tk.END, "\n" + message + "\n", tag_name)
        self.historyscroll.config(state='disabled')
        
        # Auto-scroll to bottom
        self.historyscroll.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()

# alskdfalksdjf;alskdfja;lkdfja;sldkjf
