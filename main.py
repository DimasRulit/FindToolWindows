import queue
import sys
import threading
import time
import tkinter as tk
from tkinter import ttk


import keyboard

from functions.auto_close import mouse_click
from functions.PyAnimator import Animator
from functions.functions_ import on_left_click, on_right_click
from functions.creating_win import rounded_win


import sqlite3


import customtkinter
import win32api

from PIL import Image
from functions.formats import image_formats, imgs


from ctypes import windll
from BlurWindow.blurWindow import blur


scl_f_b = []


Alpha_win = 0.7

def do_nothing(event):
    pass


def darker(kaka):
    #app3.attributes("-topmost", True) 
    if kaka==True:
        anim = Animator(0.01,Alpha_win,0.3,120,'ease',True)
        for v in anim:
            app3.attributes('-alpha', v)
            app3.update()
    else:
        anim = Animator(Alpha_win,0.01,0.3,120,'ease',True)
        for v in anim:
            app3.attributes('-alpha', v)
            app3.update()
        app3.withdraw()


def create_widgets():
    frame_1 = customtkinter.CTkFrame(master=frame_app)
    frame_1.grid(row=1,columnspan=2,pady=5, padx=5,sticky="nswe")
    search_entry = customtkinter.CTkEntry(master=frame_1, placeholder_text="Search...",width=780,height=20, font=('Arial',40))
    search_entry.pack(pady=10, padx=10)
    
    search_results_text = tk.Text(app1, height=20, width=100)
    search_results_text.pack()

    # привязываем обработчик событий к полю ввода
    
    search_entry.bind('<KeyRelease>', lambda event: schedule_search_files(search_entry, search_results_text))

    return search_entry, search_results_text

def clear_scrollable_frame():

    for button in scl_f_b:
        button.destroy()
    scl_f_b.clear()


def schedule_search_files(search_entry, search_results_text):
    search_query = search_entry.get().lower()
    if search_query.strip():
        app1.attributes("-topmost", True) 

        global search_timer, search_thread, scl_f_b
        for button in scl_f_b:
            button.destroy()
        if search_timer:
            app.after_cancel(search_timer)
        if search_thread:
            search_thread.do_run = False
        
        scl_f_b = []
        if not search_thread or not search_thread.is_alive():
            search_timer = app.after(500, lambda: search_files(search_entry, search_results_text))
    else:
        app1.wm_attributes("-alpha", 0)



def search_files(search_entry, search_results_text):
    global search_thread
    search_query = search_entry.get().lower()
    app1.update()
    app1.wm_attributes("-alpha", 1)
    if search_query.strip():
        
        search_thread = threading.Thread(target=search_files_helper, args=(search_query, search_results_text))
        search_thread.start()


def on_enter(event, button):
    text = button.cget("text")
    print(text)
    print(len(text))
    spaces = " " * (100 - len(text))
    button.configure(text=f"{spaces}{text}".rstrip())



def on_leave(event, button,text):
    button.configure(text=text)




def search_files_helper(search_query, search_results_text):
    app1.update()
    app1.deiconify()
    if search_query.strip():
        global scl_f_b
        conn = sqlite3.connect('file_index.db')
        c = conn.cursor()
        drives = win32api.GetLogicalDriveStrings().split('\x00')[:-1]
        for widget in app1.winfo_children():
            widget.destroy()
            print('DELETED')
        app1.deiconify()
        app1.update()
        
        try:
            scl_f_b = []
            scl_f = customtkinter.CTkScrollableFrame(master=app1, label_text='', bg_color='#000001',corner_radius=10)
            scl_f.pack(side='top', fill='both', expand=True,pady=10)

            for drive in drives:
                for row in c.execute(
                        'SELECT * FROM files WHERE name LIKE ? AND path LIKE ?',
                        ('%' + search_query + '%', drive + '%')
                ):
                    file_name = row[0].lower()
                    if search_query in file_name:
                        result = row[0]
                        if result != '':
                            app1.deiconify()
                            app1.wm_attributes("-alpha", 1)
                            
                            letter = customtkinter.CTkButton(master=scl_f,
                                                             text=result, image=load_img(result),
                                                             width=800, 
                                                             height=30,
                                                             fg_color="#363636",
                                                             hover_color="#505050",
                                                             anchor='w')
                            letter.bind("<Button-1>", lambda event, r=row[1]: on_left_click(r))
                            letter.bind("<Button-3>", lambda event, r=str(row[1])[:-len(row[0])]: on_right_click(r))
                            letter.bind("<Enter>", lambda event, button=letter: on_enter(event, button))
                            letter.bind("<Leave>", lambda event, button=letter, text=result: on_leave(event, button,text))

                            letter.pack(side="top", padx=5, pady=3)
                            scl_f_b.append(letter)

                    if not getattr(search_thread, "do_run", True):
                        break
        finally:
            c.close()
            conn.close()

        

def animation():
    global search_thread
    height = 127
    width = 800
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()
    x_coordinate = int((screen_width/2) - (width/2))
    y_coordinate = int((screen_height/2) - (height/2)-200)

    anim = Animator(0,height+200,0.1,120,'ease',False)
    for v in anim:
        app1.geometry("{}x{}+{}+{}".format(width, v, x_coordinate, y_coordinate+150))
        app1.update()
    search_thread.join()



def load_img(text):
    # Получаем расширение файла
    file_extension = text.split(".")[-1]
    print(file_extension)
    # Проверяем, что расширение файла присутствует в словаре image_formats
    if file_extension.upper() in image_formats:
        img_format = image_formats[file_extension.upper()]
        print(f"Файл является форматом {img_format}.")
        
        # Проверяем, есть ли формат в словаре imgs
        img = customtkinter.CTkImage(Image.open(imgs["IMG"]))
        return img
    else:
        if file_extension=='ai':
            img = customtkinter.CTkImage(Image.open(imgs["AI"]))
            return img
        img = customtkinter.CTkImage(Image.open(imgs["OTHER"]))
        return img
global letter
block_button_op = True



global op_menu

def options():
    global search_thread


    global op_menu
    letter.configure(command=None)
    search_thread.do_run = False
    anim = Animator(-y_coordinate,-1000,0.3,120,'ease',False)
    #AnimGr()
    for v in anim:
        app.geometry("{}x{}+{}+{}".format(width, height, x_coordinate, v))
        search_entry.focus_set()
        app.update()
    op_menu = customtkinter.CTkToplevel()
    op_menu.config(background='#000001')
    op_menu.attributes("-transparentcolor", '#000001')
    op_menu.overrideredirect(True)
    op_menu.attributes("-topmost", True) 

    

    op_menu.geometry("{}x{}+{}+{}".format(width, height, x_coordinate, y_coordinate))
    
    op_menu_ = rounded_win(op_menu,width=700,height=100)
    
    op_menu_but = customtkinter.CTkButton(master=op_menu_,text='Close options', width=750,height=30,fg_color="#363636", corner_radius=10,
                                                             hover_color="#505050",
                                                             anchor='w',command=option_top)
    op_menu_but.pack(pady=10,padx=10)


def option_top():
    letter.configure(command=options)
    op_menu.destroy()
    toggle_window()



customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")
app = customtkinter.CTk()
app.config(background='#000001')
app.attributes("-transparentcolor", '#000001')



app3 = customtkinter.CTkToplevel()
app3.configure(bg="#000000")
app3.attributes('-fullscreen', True)
app3.attributes('-alpha', 0)
app3.transient(app)
darker(True)

app1 = customtkinter.CTkToplevel()
app1.transient(app) 




height = 127
width = 800
app.overrideredirect(True)
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
x_coordinate = int((screen_width/2) - (width/2))
y_coordinate = int((screen_height/2) - (height/2)-200)


app1.geometry("{}x{}+{}+{}".format(width, height+200, x_coordinate, y_coordinate+150))
app1.overrideredirect(True)
app1.deiconify()
app1.wm_attributes("-alpha", 0)
app1.config(background='#000001')
app1.attributes("-transparentcolor", '#000001')







app.geometry("{}x{}+{}+{}".format(width, height, x_coordinate, y_coordinate))
app.overrideredirect(True)
app.deiconify()

fak = 1000-y_coordinate
fak = 1000-fak
print(fak)


def destroy():
    app.quit()
    app.destroy()




 
frame_app = rounded_win(app,corner_radius=10)

letter = customtkinter.CTkButton(master=frame_app,
                                     text='Options', 
                                     width=750,
                                     height=30,
                                     fg_color="#363636", 
                                     corner_radius=10,
                                     hover_color="#505050",
                                     anchor='w')



cl_b = customtkinter.CTkImage(Image.open('ICONS\close.png'),size=(30,30))


close = customtkinter.CTkButton(master=frame_app,text='❌',width=50,height=30,fg_color="#363636",corner_radius=10,
                                                             hover_color="#860000",anchor='center',command=destroy)
style = ttk.Style()
style.configure('TButton', shadow=True)

letter.grid(row=0,column=0, padx=5, pady=3,sticky='ew')
close.grid(row=0,column=1, padx=5, pady=3,sticky='ew')


search_entry, search_results_text = create_widgets()
anim = Animator(-1000,y_coordinate,0.3,120,'ease',False)
#AnimGr()
for v in anim:
    app.attributes("-topmost", True) 
    app.geometry("{}x{}+{}+{}".format(width, height, x_coordinate, v))
    search_entry.focus_set()
    app.update()
    app.attributes("-topmost", True) 

focus = 0


is_open = False
def toggle_window():
    
    global search_thread
    global is_open
    global search_entry
    global Alpha_win
    if not is_open:
        threading.Thread(target=darker,args=(False,)).start()
        app.attributes("-topmost", True) 
        app1.attributes("-topmost", True) 
        anim = Animator(y_coordinate,-1000,0.3,120,'ease',False)
        for v in anim:
            app.geometry("{}x{}+{}+{}".format(width, height, x_coordinate, v))
            app1.geometry("{}x{}+{}+{}".format(width, height+200, x_coordinate, v+150))
            app.update()
            app1.update()
        search_entry.delete(0,tk.END)
        app1.wm_attributes("-alpha", 0)
        is_open=True
        if search_thread != None:
            if search_thread.is_alive():
                search_thread.join()
            
    else:
        app3.deiconify()
        threading.Thread(target=darker,args=(True,)).start()
        app.attributes("-topmost", True) 
        app1.attributes("-topmost", True) 
        app.deiconify()
        app1.deiconify()
        #app1.withdraw()
        anim = Animator(-1000,y_coordinate,0.3,120,'ease',False)
        
        for v in anim:
            app.geometry("{}x{}+{}+{}".format(width, height, x_coordinate, v))
            app1.geometry("{}x{}+{}+{}".format(width, height+200, x_coordinate, v+150))
            search_entry.focus_set()
            app.update()
            app1.update()
        search_entry.focus_set()

        is_open=False
        return is_open    

def check_queue():
    global search_thread
    global is_open
    global running
    global a1
    global a2
    

    while True:
        try:
            text_1 = result_queue.get(block=False)
            # Обрабатываем значение text_1
            if text_1=='clicked':
                print(text_1)
                
                if search_thread:
                    search_thread.do_run = False
                if a1:
                    a1.do_run = False
                if is_open==False:
                    toggle_window()
        except queue.Empty:
            pass
        time.sleep(0.1)



def focus_in(event):
    global focus
    focus += 1
    #toggle_window()

def focus_out(event):
    global focus
    focus -= 1
    if focus == 0:
        toggle_window()



def on_press(key):
    if key.name == 'shift' and keyboard.is_pressed('ctrl'):
        toggle_window()

keyboard.on_press(on_press)


search_timer = None
search_thread = None

result_queue = queue.Queue()
running = True


a1 = threading.Thread(target=check_queue, daemon=True).start()


a2 = threading.Thread(target=mouse_click, args=(app, result_queue), daemon=True).start()


app.bind("<FocusIn>", focus_in)
app.bind("<FocusOut>", focus_out)
app.mainloop()
