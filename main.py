import threading
import tkinter as tk
from tkinter import ttk
import sqlite3
import win32api
import os
import customtkinter
from PyAnimator import Animator




scl_f_b = []

def do_nothing(event):
    pass
def on_left_click(text):
    print(text)
    os.startfile(text)
    

def on_right_click(text):
    print(text)
    os.startfile(text)

def create_widgets():
    frame_1 = customtkinter.CTkFrame(master=app)
    frame_1.pack(pady=5, padx=5, fill="both", expand=True)
    search_entry = customtkinter.CTkEntry(master=frame_1, placeholder_text="Хочу порно....",width=780,height=100, font=('Arial',40))
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

        global search_timer, search_thread, scl_f_b
        for button in scl_f_b:
            button.destroy()
        if search_timer:
            app.after_cancel(search_timer)
        if search_thread:
            search_thread.do_run = False
        
        scl_f_b = []
        if not search_thread or not search_thread.is_alive():
            search_timer = app.after(300, lambda: search_files(search_entry, search_results_text))
    else:
        app1.wm_attributes("-alpha", 0)



def search_files(search_entry, search_results_text):
    global search_thread
    search_query = search_entry.get().lower()
    app1.update()
    if search_query.strip():
        
        search_thread = threading.Thread(target=search_files_helper, args=(search_query, search_results_text))
        search_thread.start()







def search_files_helper(search_query, search_results_text):
    app1.update()
    if search_query.strip():
        global scl_f_b
        conn = sqlite3.connect('file_index.db')
        c = conn.cursor()
        drives = win32api.GetLogicalDriveStrings().split('\x00')[:-1]
        for widget in app1.winfo_children():
            widget.destroy()
            print('DELETED')
        app1.update()

        try:
            scl_f_b = []
            scl_f = customtkinter.CTkScrollableFrame(master=app1, label_text='')
            scl_f.pack(side='top', fill='both', expand=True,pady=10, padx=10)

            for drive in drives:
                for row in c.execute(
                        'SELECT * FROM files WHERE name LIKE ? AND path LIKE ?',
                        ('%' + search_query + '%', drive + '%')
                ):
                    file_name = row[0].lower()
                    if search_query in file_name:
                        result = row[0]
                        if result != '':
                            app1.wm_attributes("-alpha", 1)
                            letter = customtkinter.CTkButton(master=scl_f,
                                                             text=result, 
                                                             width=800, 
                                                             height=30,
                                                             fg_color="#363636",
                                                             hover_color="#505050",
                                                             anchor='w')
                            letter.bind("<Button-1>", lambda event, r=row[1]: on_left_click(r))
                            letter.bind("<Button-3>", lambda event, r=str(row[1])[:-len(row[0])]: on_right_click(r))
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



customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")
app = customtkinter.CTk()

app1 = customtkinter.CTkToplevel()



height = 127
width = 800
app.overrideredirect(True)
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
x_coordinate = int((screen_width/2) - (width/2))
y_coordinate = int((screen_height/2) - (height/2)-200)


app1.geometry("{}x{}+{}+{}".format(width, height+200, x_coordinate, y_coordinate+150))
app1.overrideredirect(True)

app1.configure(fg_color='#363636')
app1.wm_attributes("-alpha", 0)



app.geometry("{}x{}+{}+{}".format(width, height, x_coordinate, y_coordinate))
app.overrideredirect(True)
anim = Animator(-1000,y_coordinate,0.3,120,'ease',False)
fak = 1000-y_coordinate
fak = 1000-fak
print(fak)


letter = customtkinter.CTkButton(master=app,text='Options', width=800,height=30,fg_color="#363636",
                                                             hover_color="#505050",
                                                             anchor='w')
style = ttk.Style()
style.configure('TButton', shadow=True)

letter.pack()
for v in anim:
    app.geometry("{}x{}+{}+{}".format(width, height, x_coordinate, v))
    letter.pack(side="top", padx=5, pady=3)
    
    print(fak/v)
    app.update()







search_entry, search_results_text = create_widgets()
search_timer = None
search_thread = None
app.mainloop()
