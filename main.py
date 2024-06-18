import sys
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from PIL import ImageTk, Image
import webbrowser

root = tk.Tk()
root.geometry("430x600")
root.title("TOL Viewer")
root.resizable(False,False)
root.configure(bg='white')

s = Style()
s.configure('My.TFrame', background='white')

container = ttk.Frame(root, width=460, height=600,style='My.TFrame')
canvas = tk.Canvas(container,bg='white')
scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
scrollbarx = ttk.Scrollbar(container, orient="horizontal", command=canvas.xview)
scrollable_frame = ttk.Frame(canvas, style='My.TFrame')
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set, xscrollcommand=scrollbarx.set)

try:
    code_file = open(sys.argv[1],'r')
    imgs = []
    if ".tol" in sys.argv[1]:

        class LinkLabel(tk.Label):
            def __init__(self,parent, *argv, **kwargs):
                try:
                    self.url = kwargs.pop('url')
                except:
                    raise ValueError('No parameter url!')
                try:
                    font = kwargs.pop('font')
                    if font.__class__.__name__ == 'str':
                        font = tuple(font.split())
                    font_res = list(font)
                    font_res.append('underline')
                    font_res = tuple(set(font_res))
                except:
                    font_res = ('arial',10,'underline')
                super().__init__(parent,*argv, font=font_res, fg='blue', cursor='hand2',bg='white', **kwargs)
                self.bind('<Button-1>', self.open_url)
            def open_url(self,event=None):
                webbrowser.open_new_tab(self.url)
                self.config(fg = 'purple')

        def create_label(text:str, size:int, img:str,is_url:int,color:str,underline:bool):
            global imgs
            if is_url == 0:
                if underline == True:
                    tk.Label(scrollable_frame, text=text, image = img, font=(None, size,"underline"),foreground=color,bg='white').pack(side="top", anchor="w", padx=4)
                else:
                    tk.Label(scrollable_frame, text=text, image = img, font=(None, size),foreground=color,bg='white').pack(side="top", anchor="w", padx=4)
                    tk.Label.image = img
                    imgs.append(img)
            else:
                LinkLabel(scrollable_frame,text=text,url=text).pack(side="top", anchor="w", padx=4)

        def TOL(com:str):
            if com[0] == '>':
                if com[1] == '🔴':
                    create_label(com[2:],21, None,0,"red",True)
                elif com[1] == '🟢':
                    create_label(com[2:],21, None,0,"green",True)
                elif com[1] == '🔵':
                    create_label(com[2:],21, None,0,"blue",True)
                elif com[1] == '🟡':
                    create_label(com[2:],21, None,0,"yellow",True)
                else:
                    create_label(com[1:], 21, None,0,"black",True)
            elif com[0] == '^':
                if com[1] == '🔴':
                    create_label(com[2:],16, None,0,"red",False)
                elif com[1] == '🟢':
                    create_label(com[2:],16, None,0,"green",False)
                elif com[1] == '🔵':
                    create_label(com[2:],16, None,0,"blue",False)
                elif com[1] == '🟡':
                    create_label(com[2:],16, None,0,"yellow",False)
                else:
                    create_label(com[1:], 16,None,0,"black",False)
            elif com[0:2] == '* ':
                if com[0:3] == '* 🔴':
                    create_label(f"  ● {com[3:]}", 11, None,0,"red",False)
                elif com[0:3] == '* 🟢':
                    create_label(f"  ● {com[3:]}", 11, None,0,"green",False)
                elif com[0:3] == '* 🔵':
                    create_label(f"  ● {com[3:]}", 11, None,0,"blue",False)
                elif com[0:3] == '* 🟡':
                    create_label(f"  ● {com[3:]}", 11, None,0,"yellow",False)
                else:
                    create_label(f"  ● {com[2:]}", 11, None,0,"black",False)
            elif com == ';;;':
                create_label(" ", 5, None,0,None,False)
            elif com[0] == '[':
                if com[len(com)-1] == ']':
                    img = ImageTk.PhotoImage(Image.open(com[1:len(com)-1]))
                    create_label("",32,img,0,None,False)
            elif com[0] == '{':
                if com[len(com)-1] == '}':
                    create_label(com[1:len(com)-1], None,None,1,None,False)
            elif com[0] == '🔴':
                    create_label(com[1:],11, None,0,"red",False)
            elif com[0] == '🟢':
                create_label(com[1:],11, None,0,"green",False)
            elif com[0] == '🔵':
                create_label(com[1:],11, None,0,"blue",False)
            elif com[0] == '🟡':
                create_label(com[1:],11, None,0,"yellow",False)
            else:
                create_label(com,11, None,0,"black",False)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        scrollbarx.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        for line in code_file:
            line0 = line.strip()
            TOL(line0)

        container.pack(fill="both", side="top", expand=True)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        scrollbarx.pack(side="bottom", fill="x")

        root.mainloop() 
    else:
        print("This file isnt .tol!")
except FileNotFoundError:
    print("File not found!")
except IndexError:
    print("You missed argument!")