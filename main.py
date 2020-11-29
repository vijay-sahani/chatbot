from tkinter import *
from tkinter import messagebox as msg
from tkinter import colorchooser
from tkinter import filedialog
import datetime
import time
import random
import webbrowser
import pyttsx3
import os
import wikipedia
import threading
import smtplib
from py_Info import answers
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


info = {"name":"email_id"}
emaii_id = "your email id"
password = "your password"


def Wishme():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        greet = f"Bot:Good Morning, Sir"
    elif hour >= 12 and hour < 18:
        greet = f"Bot:Good Afternoon, Sir"
    else:
        greet = f"Bot:Good Evening, Sir"
    return greet


class Chatbot:
    def __init__(self, master):
        self.master = Frame(master)
        bg_color = "#4f4f4f"
        fg_color = "#ffffff"
        frame_bg = "grey"
        frame_relief = GROOVE
# Scrollbar for text box
        self.f1 = Frame(master, bd=6, relief=frame_relief, bg=frame_bg)
        self.f1.pack(fill=BOTH, expand=True)
        self.scrollbar = Scrollbar(self.f1, bd=0)
        self.scrollbar.pack(side=RIGHT, fill=Y)
# Text box
        self.text = Text(self.f1, bg=bg_color, spacing3=5, font="Verdana 10", width=10, height=1,
                         yscrollcommand=self.scrollbar.set, bd=1, padx=6, pady=6, relief=GROOVE, state=NORMAL, fg=fg_color)
        self.text.pack(fill=BOTH, expand=True)
        self.text.insert(END, Wishme()+"\n")
        self.text.config(state=DISABLED)
        self.scrollbar.config(command=self.text.yview)
# Status bar
        self.f2 = Frame(master, bd=3, bg=frame_bg, relief=frame_relief)
        self.f2.pack(side=BOTTOM, fill=X)
        self.inp = StringVar()
        self.inp.set("No messages yet!")
        self.status = Label(self.f2, textvariable=self.inp, bg="gray36", bd=3,
                            relief=SUNKEN, anchor="w", font="Verdana 9", fg=fg_color)
        self.status.pack(side=BOTTOM, fill=X)
# Entry field for user input
        self.f3 = Frame(master, bd=1, bg=frame_bg, relief=frame_relief)
        self.f3.pack(side=LEFT, fill=X, expand=True)
        self.entry = Entry(self.f3, bd=1, insertbackground=fg_color,
                           relief=GROOVE, bg=bg_color, fg=fg_color)
        self.entry.pack(side=LEFT, fill=X, expand=True)
# Send Button
        self.f4 = Frame(master, bd=0, bg=frame_bg, relief=frame_relief)
        self.f4.pack(side=RIGHT)
        self.button = Button(self.f4, text="Send>>", width=6, bd=1, bg="gray36", fg=fg_color,
                             relief=GROOVE, font="Verdana 7 bold")
        self.button.bind("<Button>", self.send)
        master.bind("<Return>", self.send)
        self.button.pack(side=RIGHT)
# Menus
        menu = Menu(master)
        master.config(menu=menu, bd=2)
# File menu
        f = Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=f)
        f.add_command(label='Clear chat', command=self.clear)
        f.add_separator()
        f.add_command(label='Exit', command=exit)
# Edit menu
        edit = Menu(menu, tearoff=0)
        menu.add_cascade(label='Edit', menu=edit)
        theme = Menu(edit, tearoff=0)
        edit.add_cascade(label='Themes', menu=theme)
        # theme.add_command(label='Theme 1', command=self.Theme1)
        theme.add_command(label='Theme 1', command=self.Theme2)
        theme.add_command(label='Theme 2', command=self.Theme3)
        theme.add_separator()
        make_your = Menu(theme, tearoff=0)
        theme.add_cascade(label="Make your own", menu=make_your)
        make_your.add_command(label='Choose background',
                              command=self.choose_color)
        make_your.add_command(label='Choose font color',
                              command=self.choose_font)
# Help menu
        m2 = Menu(menu, tearoff=0)
        menu.add_cascade(label='Help', menu=m2)
        m2.add_command(label="About", command=self.about)
        m2.add_command(label="Follow ME", command=self.follow_me)

# Speak's the output
    def speak(self, output):
        # Using try except to avoid unwanted error
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)
        try:
            engine.setProperty('rate', 195)
            engine.say(output)
            engine.runAndWait()
        except:
            return None

    def Attachments(self, receiver, content):
        dir_path = filedialog.askopenfilename()
        fromaddr = emaii_id
        toaddr = receiver
        mssg = MIMEMultipart()
        mssg['From'] = fromaddr
        mssg['To'] = toaddr
        # msg['Subject'] = "Bot Mail do not reply"
        body = content
        mssg.attach(MIMEText(body, 'plain'))
        filename = os.path.basename(dir_path)
        path = dir_path
        attachment = open(path, "rb")
        p = MIMEBase('application', 'octet-stream')
        p.set_payload((attachment).read())
        encoders.encode_base64(p)
        p.add_header('Content-Disposition',
                     "attachment; filename= %s" % filename)
        mssg.attach(p)
        s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        s.ehlo()
        s.login(fromaddr, password)
        text = mssg.as_string()
        s.sendmail(fromaddr, toaddr, text)
        s.quit()

    def sendmail(self, to, content):
        ask = msg.askquestion('Attachment', 'Do you want to attach a file?')
        if ask == 'yes':
            self.Attachments(to, content)
        elif ask == 'no':
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.starttls
            server.login(emaii_id, password)
            server.sendmail(emaii_id, to, content)
            server.close()

    def chat(self, user):
        '''
        Takes input from send method and return
        any one from the below as op(output)
        '''
        if "time" in user:
            t = (time.strftime('%I:%M:%S %p'))
            op = t
        elif "bye" in user or "exit" in user:
            op = msg.askokcancel("Exit", "Confirm Exit")
            if op:
                quit()
            else:
                return "You Cancelled"
        elif "what is" in user:
            user = user.replace("what is ", "")
            ans = answers(user)
            op = ans
        elif "date" in user:
            date = time.strftime('%B %d, %Y')
            op = date
        elif "open yb" in user or "youtube" in user:
            webbrowser.open("https://www.youtube.com")
            op = "Opening Youtube"
        elif "open stack" in user:
            webbrowser.open("https://www.stackoverflow.com")
            op = "Opening Stackoverflow"
        elif "open google" in user:
            webbrowser.open("https://www.google.com")
            op = "Opening Google"
        elif "open gfg" in user:
            webbrowser.open("https://www.geeksforgeeks.org")
            op = "Opening GeeksforGeeks"
        elif 'wiki' in user:
            try:
                user = user.replace('wiki', '')
                results = wikipedia.summary(user, sentences=2)
                op = f"According to wikipedia {results}"
            except:
                op = "No results found sir!"
        elif "search" in user:
            user = user.replace('search', '')
            search = ("https://www.google.com/search?q=" + user)
            webbrowser.open(search)
            op = f"Searching {user}"
        elif "open code" in user:
            path = "path of visual code"
            os.startfile(path)
            op = "Opening visual studio code"
        elif "play music" in user:
            music_d = "path"
            songs = os.listdir(music_d)
            s = random.choice(songs)
            os.startfile(os.path.join(music_d, s))
            op = f"playing {s}"
        elif "send email to" in user:
            try:
                user = user.replace('send email to ', '')
                a, b = user.split(",")
                to = info.get(a)
                content = b
                self.sendmail(to, content)
                op = f"Sending email to {a}\nMessage:{b}\nEmail sent."
            except:
                op = f"Email not sent:("
        elif "+" in user or "-" in user or "*" in user or "/" in user or "%" in user or "//" in user or "x" in user:
            try:
                if "x" in user:
                    user = user.replace("x", "*")
                ans = eval(user)
                op = f"The answer is {ans}"
            except ZeroDivisionError:
                op = "Cannot divide by zero"
            except:
                op = "Invalid Syntax"
        elif "open chat" in user or "whatsapp" in user:
            path = "path of whatsapp"
            os.startfile(path)
            op = "Opening whatsapp"
        else:
            op = 'Type again!'
        return op

    def send(self, event):
        '''
        Takes input from entry box and op(output)
        from the chat method and inserts into screen
        '''
        print(f"Clicked at {event.x}x{event.y}")
        user = self.entry.get().lower()
        question = f"You:{self.entry.get()} \n"
        self.text.config(state=NORMAL)
        self.text.insert(END, question)
        self.text.config(state=DISABLED)
        self.entry.delete(0, END)
        self.inp.set(
            (str(time.strftime("Last message sent Today at "+'%I:%M:%S %p'))))
        self.status.update()
        response = self.chat(user)
        bot = f"Bot:{response} \n"
        self.text.config(state=NORMAL)
        self.text.insert(END, bot)
        self.text.config(state=DISABLED)
        self.text.see(END)
        T = threading.Thread(target=self.speak, args=(response,))
        T.daemon = 1
        T.start()


# Tortique theme


    def Theme2(self):
        self.text.config(bg="#669999", fg="#ffffff")
        self.entry.config(bg="#669999", fg="#ffffff",
                          insertbackground="#ffffff")
        self.status.config(bg="#003333", fg="#ffffff")
        self.button.config(bg="#003333", fg="#ffffff")


# Hacker theme


    def Theme3(self):
        self.text.config(bg="#0F0F0F", fg="#33FF33")
        self.entry.config(bg="#0F0F0F", fg="#33FF33",
                          insertbackground="#33FF33")
        self.status.config(bg="#0F0F0F", fg="#33FF33")
        self.button.config(bg="#0F0F0F", fg="#33FF33")

# Choose your own background
    def choose_color(self):
        color_code = colorchooser.askcolor(title="Choose color")
        print(color_code)
        self.text.config(bg=color_code[1])
        self.entry.config(bg=color_code[1])
        self.status.config(bg=color_code[1])
        self.button.config(bg=color_code[1])

# Choose your own font
    def choose_font(self):
        color_code = colorchooser.askcolor(title="Choose color")
        print(color_code)
        self.text.config(fg=color_code[1])
        self.entry.config(fg=color_code[1], insertbackground=color_code[1])
        self.status.config(fg=color_code[1])
        self.button.config(fg=color_code[1])

# To clear the screen
    def clear(self):
        self.text.config(state=NORMAL)
        self.text.delete(1.0, END)
        self.text.config(state=DISABLED)
        self.inp.set("No Messages Sent!")
        self.status.update()

    def about(self):
        msg.showinfo('About', 'Created by Vijay')

    def follow_me(self):
        ask = msg.askquestion('Follow ME', "Follow me on Instagram")
        if ask == "yes":
            webbrowser.open("https://www.instagram.com/_vj_s/")
        else:
            return None


if __name__ == "__main__":
    root = Tk()
    a = Chatbot(root)
    root.geometry("355x470")
    root.minsize(355, 470)
    root.title("chatbot")
    root.iconbitmap("i.ico")
    root.mainloop()
