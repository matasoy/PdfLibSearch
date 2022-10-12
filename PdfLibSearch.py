from tkinter import *
import tkinter as tk
from tkinter import TclError, ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename
import tkinter.scrolledtext as scrolledtext
import ctypes
from functools import partial
from json import loads, dumps
import subprocess
import os
import string
import random
from dataclasses import dataclass
import json
import webbrowser
import threading
import subprocess
import time
from PIL import Image, ImageTk
from itertools import count, cycle

ctypes.windll.shcore.SetProcessDpiAwareness(True)




# Setup
root = Tk()
root.iconbitmap("ico.ico")
#root.geometry('1000x600')
frame4 = LabelFrame(root,bg = "#ffffff",width=1000,height=400,padx=5,pady=5)
frame4.pack(fill=BOTH,expand=TRUE,pady=10) 
frame4.columnconfigure(1, weight=1)
frame4.pack_forget()
frame1 = LabelFrame(root,bg = "#e9e9e9",width=1000,height=400,padx=5,pady=5)
frame1.pack(fill=BOTH,expand=TRUE,pady=10) 
frame1.columnconfigure(1, weight=1)
frame2 = LabelFrame(root,bg = "#1f5a8e",width=1000,height=400,padx=5,pady=5)
frame2.pack(fill=BOTH,padx=10,pady=10) 
frame2.columnconfigure(1, weight=1)
frame2.pack_forget()
frame3 = LabelFrame(root,bg = "#ffffff",width=1000,height=400,padx=5,pady=5)
frame3.pack(fill=BOTH,expand=TRUE,pady=10) 
frame3.columnconfigure(1, weight=1)
frame3.pack_forget()

# Used to make title of the application
applicationName = 'PDF Detay Arama'
root.title(applicationName)
root.columnconfigure(0, weight=1)



# Setting the font and Padding for the Text Area
fontName = 'Bahnschrift'
padding = 10
notpad_txt = StringVar()    
pdfklasor_txt = StringVar()

with open("ayar.json") as file:
    data = json.load(file)
    notpad_txt.set(data["ayar"][0]["notepad"])
    pdfklasor_txt.set(data["ayar"][0]["pdfklasor"])
    print(data["ayar"][0]["notepad"]+" "+data["ayar"][0]["pdfklasor"])


metinler="txtler"
#directory="C:\\Users\\Lenovo\\Documents\\Mendeley"
directory=pdfklasor_txt.get()
#editor="C:\\Program Files\\Notepad++\\notepad++.exe"
editor=notpad_txt.get()
ayar_acikmi=0
yardim_acikmi=0

if not os.path.exists(metinler):
    os.makedirs(metinler)



def gizle(widget,d=1):
    if d==0:
        widget.pack_forget()   
    else:
        widget.pack()
        widget.pack(fill=BOTH,expand=TRUE,pady=10) 
        widget.columnconfigure(1, weight=1)
        root.geometry("1000x600")

def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def callback():
    search_str(metinler,e.get())
    
Label(frame1,text ="Kelime veya Cümle Aratın",font=('Arial 12')).pack(side=TOP) 
e = Entry(frame1,text = "animation", font=('Arial 24'))
e.pack(fill=X, pady=10)
e.focus_set()
b = Button(frame1, text = "ARA", width = 50, command = callback)
b.pack()


def search_str(file_path, word):  
    textArea.delete("1.0","end")
    b.config(text="ARA")    
    kelime_varmi = 0
    for filename in os.listdir(file_path):
        dosyakod = filename.split()[0]
        with open(file_path+"\\"+filename, 'r', encoding="utf8") as fp:
            lines = fp.readlines()
            #textArea.insert(INSERT, filename+"\n\n")
            #tmp_metin += filename+"\n\n" 
            tmp_metin=""
            kelime_varmi=0
            for line in lines:            
                if line.find(word) != -1:
                    #textArea.insert(INSERT, str(lines.index(line))+". Satır\n")
                    #textArea.insert(INSERT, str(line)+"\n")
                    tmp_metin += dosyakod+"-"+str(lines.index(line))+" . Satır\n"
                    tmp_metin += str(line)+"\n"
                    kelime_varmi = 1
            if kelime_varmi==1:
                textArea.insert(INSERT, filename+"\n\n"+tmp_metin+"\n\n")
    add_highlighter()
    
    
class ImageLabel(tk.Label):
    """
    A Label that displays images, and plays them if they are gifs
    :im: A PIL Image instance or a string filename
    """
    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        frames = [] 
        try:
            for i in count(1):
                frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass
        self.frames = cycle(frames) 
        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100 
        if len(frames) == 1:
            self.config(image=next(self.frames))
        else:
            self.next_frame() 
    def unload(self):
        self.config(image=None)
        self.frames = None 
    def next_frame(self):
        if self.frames:
            self.config(image=next(self.frames))
            self.after(self.delay, self.next_frame)
           
class MyClass(threading.Thread):
    def __init__(self):
        self.stdout = None
        self.stderr = None
        threading.Thread.__init__(self)
    
    def run(self):
        CREATE_NO_WINDOW = 0x08000000
        i=0
        for root, dirs, files in os.walk(directory):
            for filename in files:
                if filename.endswith(".pdf"):
                    f = os.path.join(root, filename)
                    args = "pdftotext.exe -enc UTF-8 \""+f+"\" \"txtler\\"+id_generator()+" "+filename+".txt\""
                    #print(args+" "+str(i))
                    p=subprocess.Popen(args,shell=False,stdout=subprocess.PIPE,stderr=subprocess.PIPE,creationflags=CREATE_NO_WINDOW)
                    i+=1        
        self.stdout, self.stderr = p.communicate()
        gizle(frame1,1)
        gizle(frame4,0)
myclass = MyClass()  
def pdf_to_text():
    
    print("başladı")    
    gizle(frame1,0)
    gizle(frame2,0)
    gizle(frame3,0)
    gizle(frame4,1)
    time.sleep(1)
  
    
    myclass.start()
    #myclass.join()
    print(myclass.stdout)  
    
    #gizle(frame4,0)
    #pb["value"]=300
    #for root, dirs, files in os.walk(directory):
    #    for filename in files:
    ##        if filename.endswith(".pdf"):
    #            f = os.path.join(root, filename)
    #           args = "pdftotext.exe -enc UTF-8 \""+f+"\" \"txtler\\"+id_generator()+" "+filename+".txt\""
    #            print(args+" "+str(i))
    #            subprocess.call(args)
    #            i+=1
def f_ayar_kaydet():    
    print("kaydedildi "+notpad_txt.get()+" "+pdfklasor_txt.get())
    yeniayar = "{\"ayar\":[{\"notepad\": \""+repr(notpad_txt.get())[1:-1]+"\", \"pdfklasor\": \""+repr(pdfklasor_txt.get())[1:-1]+"\"}]}"
    with open("ayar.json", 'w') as file:
        file.write(yeniayar)
        #json.dump(yeniayar, file)


def yardim():
    global yardim_acikmi
    if yardim_acikmi==0:
        gizle(frame1,0)
        gizle(frame2,0)
        gizle(frame3,1)
        yardim_acikmi=1
    else:
        gizle(frame3,0)
        gizle(frame1,1)
        gizle(frame2,0)
        ayar_acikmi=0
        yardim_acikmi=0
def ayarac():      
    global ayar_acikmi
    if ayar_acikmi==0:
        gizle(frame1,0)
        gizle(frame3,0)
        gizle(frame2,1)
        ayar_acikmi=1
    else:
        gizle(frame1,1)
        gizle(frame2,0)
        gizle(frame3,0)
        ayar_acikmi=0

def keyDown(event=None):
    root.title(f'{applicationName} - *{filePath}')
        
def add_highlighter():
    #textArea.tag_add("start", "1.11","1.17")
    #textArea.tag_config("start", background= "black", foreground= "white")    
    for tag in textArea.tag_names():
        textArea.tag_delete(tag)
    arama_sonucu=0
    for i in range(2000):
        start_pos = textArea.search(e.get(), str(i)+'.0', stopindex=END)
        if start_pos:
            arama_sonucu+=1            
            end_pos = '{}+{}c'.format(start_pos, len(e.get())+20)            
            textArea.tag_add('highlight', start_pos+"-20c", end_pos)
            textArea.tag_config('highlight', background="yellow", foreground='red')
    b.config(text="ARA ("+str(arama_sonucu)+" sonuç bulundu)")
    
def kodbul(event=None):
    try:
        print(textArea.selection_get())
        arama = textArea.selection_get()
        arama_satir=1
        arama2 = arama
        if arama2.find("-") != -1:
            arama_satir = arama2.split("-")[1]
            arama = arama2.split("-")[0]
            print("aranan:"+arama+" Tıkklanan sayfa:"+arama_satir)                
        for filename in os.listdir(metinler):
            dizi = filename.split()
            
            if dizi[0]==arama:
                print("dosya bulundu "+metinler+"\\"+filename)   
                aramaveri = "-n"+arama_satir
                arg2 = '\"'+notpad_txt.get()+'\" \"'+metinler+'\\'+filename+'\" '+aramaveri
                print(arg2)                
                subprocess.call(arg2)        
        print("arama bitti")
    except:
        print("hata")
        
def webcallback(url):
    webbrowser.open_new(url)

aciklama1 = Text(frame3,wrap=WORD)
aciklama1.insert(INSERT,"Programı ilk çalıştırdığınızda ayarlar panelini açın ve kurulu ise Notepad++ uygulamasının exe yolunu kopyalayıp tırnak olmadan ilgili yere yapıştırın. Bu yol genellikle C:\\Program Files\\Notepad++\\notepad++.exe veya C:\\Program Files (x86)\\Notepad++\\notepad++.exe şeklindedir.\n\n\nArdından üzerinde çalışmak istediğiniz pdf arşiv klasörünün yolunu kopyalayıp ilgili alana yapıştırın (Örnek: C:\\Users\\Username\\Documents\\Mendeley) ve kaydet butonuna basın. Programı kapatıp açtığınızda Dosya menüsünden Arşivi Tara butonuna tıklayın. Arşivinizdeki dosyaların miktarı ve sayfa sayısına göre işlem zaman alacaktır. \n\n\nİşlem bittikten sonra aramalarınızı gerçekleştirebilirsiniz. Çıkan sonuçlardan satırların başlarında bulunan 10 karakterlik kodlara çift tıklayarak belgeyi ilgili satır numarasından açılmasını sağlayabilirsiniz. Bunu yapabilmek için notepad++ uygulamasını kurmuş olmanız şart. İndirmek için şu adrese gidebilirsiniz. https://notepad-plus-plus.org/downloads/ \n\n\n\n Detaylı bilgi için matasoy@gmail.com")
aciklama1.pack()
aciklama1.config(highlightthickness = 0, borderwidth=0, state=DISABLED)

link1 = Label(frame3, text="Github matasoy", fg="blue", cursor="hand2")
link1.pack()
link1.bind("<Button-1>", lambda e: webcallback("https://github.com/matasoy"))

    
Label(frame2,text ="NOTEPAD++ exe'sinin ve PDF klasörünün yollarını girin",bg = "#1f5a8e").pack()    
Label(frame2,text ="Notepad++ Exe",bg = "#1f5a8e").pack()    
ayar_notepad = Entry(frame2,textvariable=notpad_txt, font=('Arial 24')).pack(fill=X,pady=2)
Label(frame2,text ="PDF Klasörü",bg = "#1f5a8e").pack()    
ayar_pdfklasor = Entry(frame2,textvariable=pdfklasor_txt, font=('Arial 24')).pack(fill=X, pady=2)
ayar_kaydet = Button(frame2, text = "Kaydet", command = f_ayar_kaydet).pack(padx=2, pady=2)

#yükleniyor gifi
Label(frame4,text ="PDF dosyaları analiz ediliyor, lütfen bekleyin",bg = "#ffffff",font=('Arial 24')).pack()   
lbl = ImageLabel(frame4)
lbl.pack()
lbl.load('loading.gif') 

textArea = scrolledtext.ScrolledText(frame1, font=f'{fontName} 12',wrap=WORD, relief=FLAT,undo=True)
textArea.pack(fill=BOTH, expand=TRUE, padx=padding, pady=padding)
textArea.bind("<Key>", keyDown)
textArea.bind("<ButtonRelease-1>", kodbul)
textArea.delete("1.0","end")

#MENÜ AYARLARI
menu = Menu(root)
root.config(menu=menu)

fileMenu = Menu(menu, tearoff=0)
menu.add_cascade(label="Dosya", menu=fileMenu)

fileMenu.add_command(label="Kapat", command=root.quit)
fileMenu.add_command(label="Arşivi Tara", command=pdf_to_text)


formatMenu = Menu(menu, tearoff=0)
menu.add_cascade(label="Ayarlar", command=ayarac)
menu.add_cascade(label="Nasıl Kullanılır", command=yardim)

root.mainloop()