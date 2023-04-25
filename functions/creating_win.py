import customtkinter


def rounded_win(app, corner_radius=10,width=400,fg_color=None,height=100):
    frame_app = customtkinter.CTkFrame(app, corner_radius=corner_radius, width=width, height=height,
                                       bg_color='#000001', fg_color=fg_color)
    frame_app.grid(sticky="nswe") # Main round frame, adjust corner_radius
    frame_app.grid_rowconfigure(0, weight=1)
    frame_app.grid_columnconfigure((0, 1), weight=1)
    frame_app.pack()
    return frame_app