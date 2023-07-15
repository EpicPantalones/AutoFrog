from time import sleep
from interpreter import *
import tkinter as tk
import threading
import pygame

'''LOAD SETTINGS'''
with open("settings.conf","r") as settings:
    args = settings.read().split()
    settings = []
    for i in range(0,len(args)):
        if i % 2 == 1:
            settings.append(args[i])
    FONTSIZE = int(settings[0])


'''SOUND EFFECT GENERATION'''
THREAD_ENABLED = True
def play_sound():
    pygame.mixer.init()
    pygame.mixer.music.load("resources/soundtrack.wav")
    pygame.mixer.music.play(-1)  # -1 plays the sound on an infinite loop
sound_thread = threading.Thread(target=play_sound, daemon=True)

# '''SOCKET_LISTENING'''
# from socket_server import start_socket_server, handle_client, handle_message
# host = ""
# port = 1234
# socket_thread = threading.Thread(target=start_socket_server, args=(host,port)).start()

'''
VISUAL / EXTRA COMMANDS
These commands are for the Tkinter GUI to use.
If removed, they would not affect the performance
of the system, but would degrade the visuals.
'''    
def on_entry_click(event):
    if entry.get() == "Enter a command...":
        entry.delete(0, tk.END)  # Delete the default text

def on_focus_out(event):
    if entry.get() == "":
        entry.insert(0, "Enter a command...")  # Insert the default text

'''
PROCESSING COMMANDS
These commands are also for the Tkinter GUI, but 
if they were to be removed, the system would no 
longer function correctly.
'''
def submit_input():
    # Receive message and post it to the terminal
    msg = entry.get()
    if len(msg) != 0:
        # Post to the terminal
        output_left.insert(tk.END,f"> {msg}\n")
        # Parse the message by argument
        args = msg.split()
        # interpret the message
        result = interpret(args)
        output_left.insert(tk.END,f"> {result}\n")
    else:
        # Just post newline
        output_left.insert(tk.END,f">\n")
    
    # Move window to the end of the message
    output_left.see(tk.END)
    # Clear the entry buffer
    entry.delete(0, tk.END)

def on_closing():
    print("Closing windows...")
    root.destroy()
    

'''
GUI CREATION
This system sets up the creation of the GUI itself.
'''
# Create the root window
root = tk.Tk()
root.configure(bg='lightblue')
root.title("AutoFrog Tool")
root.protocol("WM_DELETE_WINDOW", on_closing)

# Create the left and right frames (populated after)
frame_left = tk.Frame(master=root,relief=tk.GROOVE,width=50,height=100)
frame_right = tk.Frame(master=root,relief=tk.GROOVE,width=50,height=100)
frame_left.configure(bg='lightblue')
frame_right.configure(bg='lightblue')

'''Left frame inputs'''
# Entry box for user input 
entry = tk.Entry(master=frame_left,justify='left')
entry.insert(0, "Enter a command...")                   # default text to show
entry.configure(font=("Arial", FONTSIZE+2))
entry.bind("<FocusIn>", on_entry_click)                 # when clicked one
entry.bind("<FocusOut>", on_focus_out)                  # when out of focus
entry.bind("<Return>", lambda event: submit_input())    # bind enter key to send
# Console window (black bg)
output_left = tk.Text(master=frame_left,height=20)
output_left.configure(bg='black',fg='white',font=("Arial", FONTSIZE))
output_left.insert(tk.END,"Welcome to the AutoFrog Tool! Enter a command, or type \"help\"\n")
output_left.tag_add("t_col", "1.0", "1.end")            # These three commands make
output_left.tag_config("t_col",foreground='cyan')       # the text of the AutoFrog
output_left.bind("<Key>", lambda e: "break")            # welcome cyan instead of white
# Button Frame (Not in use)
frame_buttons_left = tk.Frame(master=frame_left,background='lightblue',height=1)
output_frame = tk.Text(master=frame_buttons_left,width=5,height=1)
output_frame.pack()

'''Right frame inputs'''
# Output title box
title_right = tk.Text(master=frame_right,height=1)
title_right.configure(bg="lightgray",fg="gray",font=("Arial", FONTSIZE))
title_right.insert(tk.END,"Nothing to Display.")
title_right.bind("<Key>", lambda e: "break") # prevents users from editing textbox
# Output Display
output_right = tk.Text(master=frame_right,height=20,background='lightgray')
output_right.configure(font=("Arial", FONTSIZE))
output_right.bind("<Key>", lambda e: "break")

'''Packing System'''
# Pack Left Frame
entry.pack(padx=5,pady=5,side=tk.TOP,fill=tk.X)
output_left.pack(padx=5,pady=5,side=tk.TOP,fill=tk.BOTH,expand=True)
frame_buttons_left.pack(padx=5,pady=5,side=tk.TOP,fill=tk.X)
# Pack Right Frame
title_right.pack(padx=5,pady=5,side=tk.TOP,fill=tk.X)
output_right.pack(padx=5,pady=5,side=tk.TOP,fill=tk.Y,expand=True)
# Pack the two frames into Root
frame_right.pack(side=tk.RIGHT,fill="y",expand=True)
frame_left.pack(side=tk.RIGHT,fill=tk.BOTH,expand=True)


'''PRODUCTION'''
'''Display the GUI'''
if THREAD_ENABLED:
    sound_thread.start()
root.mainloop()

'''ON PROGRAM TERMINATION'''
# Way to stop server???

# Disable music and play closing sound
if THREAD_ENABLED:
    pygame.mixer.music.stop()
    sound_thread.join()
    pygame.mixer.music.load("resources/close.wav")
    pygame.mixer.music.play()
    sleep(2)
    