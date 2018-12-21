import requests
from bs4 import BeautifulSoup as bs4
import time
import PIL.Image 
import PIL.ImageTk
from tkinter import *

class Window(Frame):

    def __init__(self, master = None):
        Frame.__init__(self, master)

        self.master = master
        
        self.learnpython = IntVar()
        
        self.learnjava = IntVar()

        self.learnjavascript = IntVar()

        self.ruby =IntVar()
        
        self.php = IntVar()

        self.init_window()
        
        self.finalsubreddits = []

        self.currentColor = 'white'

        self.subs = [self.learnpython,self.learnjava,self.learnjavascript,self.ruby,self.php]
    def init_window(self):

        self.master.title("Reddit Parser")

        self.pack(fill = BOTH, expand=1)
         
        sidepanel_header = Label(self,text='Reddit Parser',font='times 30')

        sidepanel_header.pack(pady=15) 

        Label(self, text="check a box to parse\n  that subreddit\n",font='times 16').pack()
        
        Checkbutton(self, text="learnpython", variable=self.learnpython,command=self.update_eta).pack() 
        
        Checkbutton(self, text="learnjava", variable=self.learnjava,command=self.update_eta).pack()
        
        Checkbutton(self, text="learnjavascript", variable=self.learnjavascript,command=self.update_eta).pack()

        Checkbutton(self, text="ruby", variable=self.ruby,command=self.update_eta).pack()

        Checkbutton(self,text="php", variable=self.php,command=self.update_eta).pack()

        redditButton = Button(self, text="Run", command=self.reddit_spider)
 
        redditButton.pack(pady=30) 

        menu = Menu(self.master)

        self.master.config(menu=menu)

        file = Menu(menu)

        file.add_command(label = 'Exit', command=self.client_exit)

        menu.add_cascade(label='File', menu=file)

        edit = Menu(menu)
        
        edit.add_command(label='Clear Text', command=self.clearText)

        edit.add_command(label='Dark/Light mode', command=self.switchMode)
        
        menu.add_cascade(label='Edit', menu=edit)

        about = Menu(menu)

        about.add_command(label='About this', command=self.about_popup)

        menu.add_cascade(label='About', menu=about)
        
        self.graytint = 50
        self.direction = 'dark'
        self.clock = Label(text='',font=('times','14','bold'),fg='white')

        self.clock.pack()

        self.updateClock()
    def updateClock(self):
        
        
        now = time.strftime("%H:%M")
        self.clock.configure(text=now,bg='gray{}'.format(str(self.graytint)))
        if self.direction == 'dark':
            self.graytint -= 5
        if self.graytint < 20:
            self.direction = 'light'
        if self.direction == 'light':
            self.graytint += 5
        if self.graytint > 50:
            self.direction = 'dark'
        
        self.after(2000,self.updateClock)

    def switchMode(self):

        if self.currentColor == 'white':
            t.config(bg='gray14',fg='white')
            self.currentColor = 'black'

            t.insert(END,'>>> Dark mode <<<')
        elif self.currentColor == 'black':
            t.config(bg='white',fg='black')
            self.currentColor = 'white'
            t.insert(END,'>>> Light mode <<<')

    def clearText(self):

        t.delete(1.0,END) 

    def client_exit(self):
            
        exit()

    def update_eta(self):
        time_to_parse.delete(1.0,END)
        checks = 0

        for s in self.subs:
            checks += s.get()
            print_form = str(checks*90)
        time_to_parse.insert(END,print_form+' seconds to parse')
        
    def about_popup(self):

        popup = Toplevel()

        message = "simple parser for reddit that focuses on links to programming resources\n  -----------------   \nGithub: porterwisnie\n\nContact me: porterwisniewski@gmail.com"
        
        Label(popup,text=message,wraplength=500,font=('Courier',14,'bold'),fg='black',bg='gray75').pack()
        
        popup.title('About')

        popup.geometry('600x350')

        popup.config(bg='gray75')
    def reddit_spider(self):
        
        t.delete(1.0,END)

        if self.learnpython.get() == 1:
            self.finalsubreddits.append('learnpython')

        if self.learnjava.get() ==1:
            self.finalsubreddits.append('learnjava')

        if self.learnjavascript.get() ==1:
            self.finalsubreddits.append('learnjavascript')
        
        if self.ruby.get() ==1:
            self.finalsubreddits.append('ruby')
        
        if self.php.get()==1:
            self.finalsubreddits.append('php')

        for subreddit in self.finalsubreddits:
            post_links = []

            links_in_posts = set()

            headers = {'user-agent':'crawler for programming resources from subreddits |  github:porterwisnie  |  repo:resourcesmaster  |'}

            url = 'https://new.reddit.com/r/'+subreddit+'/top/?t=all'

            r = requests.get(url,headers=headers)

            soup = bs4(r.text,'lxml')

            all_outbound_links = [i.get('href') for i in soup.find_all('a')]


            for link in all_outbound_links:
                try:
                    if 'comments' in link and 'http' in link:
                        post_links.append(link)
                except:
                    pass
            time.sleep(1.5)

            for link in post_links:
                r = requests.get(link,headers=headers)

                soup2 = bs4(r.text,'lxml')

                for item in soup2.find_all('a'):
                    link2 = item.get('href')
                    try:
                        if link2[0:4] == 'http' and 'reddit.com/user' not in link2 and 'RemindMeBot' not in link2 and 'register?dest' not in link2:
                            links_in_posts.add(link2)
                    except:
                        pass
                time.sleep(1.5)
            t.insert(END, '*'+subreddit+'*\n')
            for re in links_in_posts:
                t.insert(END, re+'\n')





root =Tk()

root.geometry("1600x950")

scroll = Scrollbar(root)

t = Text(root, height=25, width=80,font=('times','13','bold'))

scroll.pack(side=RIGHT, fill=Y)
t.pack(side=LEFT, fill=Y)
scroll.config(command=t.yview)
t.config(yscrollcommand=scroll.set)


time_to_parse = Text(root, height=1, width=20,font=('times','13','bold'),)

time_to_parse.pack(pady=10)
       
img = PIL.Image.open("testlogo.jpg")

photo = PIL.ImageTk.PhotoImage(img)

logo = Label(root,image=photo,height=100,width=100)

logo.pack()

app = Window(root)
root.mainloop()
