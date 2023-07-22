from tkinter import simpledialog, messagebox
import tkinter as tk
from time import sleep
import threading
import pygame
import os
import re

'''Set the working directory of the file'''
DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(DIR)

'''Load in settings.conf'''
fail = False
try:
    settings = open(f"{DIR}/settings.conf","r")
    sc = settings.readlines()
except FileNotFoundError:
    response = messagebox.askyesno("Critical Error", f"settings.conf couldn't be found. Load default settings instead?")
    if response:
        with open(f"{DIR}/resources/defaultsettings.conf","r") as default:
            sc = default.readlines()
        with open(f"{DIR}/settings.conf","w") as settings:
            for line in sc:
                settings.write(line)
        messagebox.showinfo("Fixed Settings", f"Note that if there was a settings file, it has been reset.")
    else:
        exit(0)
'''This part of the code is super gross but its banging - don't touch it'''
try:
    Font_Size = int(sc[0].strip().split()[1])
except ValueError:
    fail = True
colors = []
for i in range(1,5):
    if fail == True:
        break
    color = sc[i].strip().split()[1]
    if bool(re.match(r'^#([A-Fa-f0-9]{6})$', color)):
        colors.append(color)
    else:
        fail = True
if fail == True:
    response = messagebox.askyesno("Critical Error", f"settings.conf could not be read properly. Load default settings instead?")
    if response:
        with open(f"{DIR}/resources/defaultsettings.conf","r") as default:
            sc = default.readlines()
        with open(f"{DIR}/settings.conf","w") as settings:
            for line in sc:
                settings.write(line)
        colors = []
        Font_Size = int(sc[0].strip().split()[1])
        for i in range(1,5):
            colors.append(sc[i].strip().split()[1])
    else:
        exit(0)
Background_Color = colors[0]
Text_Color = colors[1]
Box_Color = colors[2]
Button_Color = colors[3]
LEDsize = 2 + Font_Size

'''SOUND EFFECT GENERATION'''
SOUND_ENABLED = True
def play_music():
    pygame.mixer.init()
    pygame.mixer.music.load("./resources/soundtrack.wav")
    pygame.mixer.music.play(-1)  # -1 plays the sound on an infinite loop
sound_thread = threading.Thread(target=play_music, daemon=True)

''' FUNCTIONS NOT ATTACHED TO BUTTONS '''
SAVESTATE = True
def save(state):
    if state not in [True,False]:
        raise TypeError("state given incorrectly to save function.")
    global SAVESTATE, WORKING_FILE
    if WORKING_FILE == "":
        return
    else:
        SAVESTATE = state
        if state:
            savedLED.itemconfig(led, fill="green")
        else:
            savedLED.itemconfig(led, fill="red")
    
UPLOAD_STATE = True
def upload(state):
    if state not in [True,False]:
        raise TypeError("state given incorrectly to upload function.")
    global UPLOAD_STATE
    UPLOAD_STATE = state
    if state:
        uploadLED.itemconfig(led, fill="green")
    else:
        uploadLED.itemconfig(led, fill="red")

def add_to_manifest(filename,action):
    with open("manifest","a") as manifest:
        manifest.write(f"{filename} {action}\n")

def is_valid_filename(filename):
    try:
        # Check if the filename is a valid pathname component
        os.path.normpath(filename)
        # Check if the filename is a valid filename
        return not any(c in r' ,.\/:*?"<>|' for c in filename)
    except OSError:
        return False
            
def validate_channel_file(lines):
    if len(lines) == 0:
        return None
    for i,line in enumerate(lines):
        if not line:
            continue
        if line.startswith("#"):
            continue
        words = line.split()
        if len(words) != 2:
            return f"Wrong number of arguments:\nline {i}:\n\"{line}\""
        try:
            time_str, state = words[0],words[1]
            state_val = int(state)
            if is_valid_time(time_str) == False:
                return f"\"{time_str}\" is not a valid time (0000 - 2359)"
            if state_val not in [0,1]:
                return f"\"{state}\" is not a valid state; either 0 or 1"
        except ValueError:
            return f"\"{state}\" is not a valid state; either 0 or 1"
    return None

def validate_assignments_file(lines):
    if len(lines) != 9:
        return "Wrong number of lines in file"
    else:
        checks = os.listdir(f"{DIR}/channels")
        for i,line in enumerate(lines):
            if i > 7:
                continue
            args = line.split()
            if args[0] != f"channel{i+1}":
                return f"Bad modify: {args[0]} not a valid name; should be \"channel{i}\""
            if len(args) != 2:
                return f"Wrong number of args on line {i} ({len(args)})"
            elif args[1] not in checks:
                return f"{args[1]} is not one of the listed files"
            elif args[1] == "_assignments":
                return f"cannot assign assignments file to itself (line {i})"
                
    return

def is_valid_time(time_str):
    try:
        time_value = int(time_str)
        if 0 <= time_value < 2400:
            # Check if the time has exactly 4 digits and represents valid hours and minutes
            return len(time_str) == 4 and 0 <= int(time_str[:2]) <= 23 and 0 <= int(time_str[2:]) <= 59
    except ValueError:
        pass
    return False 

''' TO RUN ON PROGRAM CLOSE ''' 
def confirm_closing():
    global SAVESTATE, UPLOAD_STATE
    if SAVESTATE == False:
        response = messagebox.askyesno("Unsaved Work", f"You have not saved the open file.\nClose the program anyways?")
        if response:
            SAVESTATE = True
        else:
            return
    if UPLOAD_STATE == False:
        response = messagebox.askyesno("Unsaved Work", f"You have not uploaded your changes.\nClose the program anyways?")
        if response:
            UPLOAD_STATE = True
        else:
            return
    if SAVESTATE and UPLOAD_STATE:
        kill_program()   
           
def kill_program():
    root.destroy()
    # Disable music and play closing sound
    if SOUND_ENABLED:
        pygame.mixer.music.stop()
        sound_thread.join()
        pygame.mixer.music.load("./resources/close.wav")
        pygame.mixer.music.play()
        sleep(2)
    exit(0) 

'''
ROOT WINDOW:
The root window is divided into two halves; the left half
is for the inputs, and the right half is for the ouputs. This
is a very loose definition.
'''
root = tk.Tk()
root.title("Aperture Science Frog Connectivity Unit")
root.configure(bg=Background_Color)
root.protocol("WM_DELETE_WINDOW", confirm_closing)
root.minsize(575, 325)

# Debug Function
def print_window_size():
    width = root.winfo_width()
    height = root.winfo_height()
    print(f"Window size: {width}x{height}")

# Create Vars
Connect_Status = tk.BooleanVar()
Upload_Status = tk.BooleanVar()

'''
LEFT FRAME:
The left frame contains the title, several buttons, and the actionbar,
which displays the current action. Many of the buttons are packed together
into subframes. The packing order goes:
GUI Title (Top)
FileSubframe (Top)
   List (Left)
   New (Left)
FileSelect (Top)
EditSubframe (Top)
   Delete (Left)
   Edit (Left)
   Save (Left)
ServerSubframe (Top)
   Connect (Left)
   Upload (Left)
AssistantSubframe (Top)
   Actionbar (Left)
   Help (Left)

'''
left_frame = tk.Frame(root,bg=Background_Color)
left_frame.pack(side=tk.LEFT, padx=10, pady=10)

# Create the GUI Title
fixed_text = tk.Label(left_frame, text="Aperature Science Frog\nConnectivity Unit", fg=Text_Color,background=Background_Color, font=('Arial', Font_Size+2))
fixed_text.pack(side=tk.TOP,anchor=tk.N,pady=5)

''' File Manager Subframe - List, New'''
filetools = tk.Frame(left_frame,bg="#2F394D")
filetools.pack(side=tk.TOP, padx=10, pady=10)

# Create the "List Files" button
def on_list_files_button_click():
    global SAVESTATE
    if SAVESTATE == False:
        response = messagebox.askyesno("Unsaved Work", f"You have not saved the current file.\nList directory anyways?")
        if not response:
            return
        else:
            save(True)
    titlebar.delete(1.0, tk.END)
    titlebar.insert(tk.END, "Directory List:")
    actionbar.delete(1.0, tk.END)
    actionbar.insert(tk.END, "Directory Printed.")
    text_box.delete("1.0", tk.END)
    files = sorted(os.listdir(f"{DIR}/channels"))
    if len(files) == 0:
        set_actionbar("No Files to Display.")
        text_box.insert(tk.END, "<Empty>")
        return 
    for file in files:
        text_box.insert(tk.END,f"{file}\n")
        
list_button = tk.Button(filetools, text="List", command=on_list_files_button_click, bg=Button_Color, highlightthickness=0, font=('Arial', Font_Size))
list_button.pack(side=tk.LEFT,padx=5,pady=5)

# Create the "New Files" button
def on_newfile_button_click():
    user_input = simpledialog.askstring("Create File", "Enter a filename:")
    if user_input:
        if is_valid_filename(user_input):
            with open(f"{DIR}/channels/{user_input}","w") as file:
                file.write(f"# CHANNEL NAME: {user_input}")
            messagebox.showinfo("Created File", f"Created file \"{user_input}\"")
            refresh_menu()
            add_to_manifest(user_input,"edit")
        else:
            messagebox.showinfo("Invalid Name", f"\"{user_input}\" is not a valid filename.")
    else:
        return
    upload(False)

new_button = tk.Button(filetools, text="New", command=on_newfile_button_click, bg=Button_Color, highlightthickness=0, font=('Arial', Font_Size))
new_button.pack(side=tk.LEFT,padx=5,pady=5)

# Create the File Select Button and File Select Dropdown
def refresh_menu():
    global popup_menu
    popup_menu = tk.Menu(root, tearoff=0)
    options = sorted(os.listdir(f"{DIR}/channels"))
    if len(options) == 0:
        popup_menu.add_radiobutton(label="None", variable=fileselect_var, value="None", command=on_popup_selected)
    else:
        for option in options:
            popup_menu.add_radiobutton(label=option, variable=fileselect_var, value=option, command=on_popup_selected)

def on_popup_selected():
    global chn_dir
    refresh_menu()
    selected_option = fileselect_var.get()
    if selected_option:
        if selected_option == "None":
            file_select_button.config(text="Select a file...")
            return
        file_select_button.config(text=selected_option)

fileselect_var = tk.StringVar()
refresh_menu()

file_select_button = tk.Button(left_frame, text="Select a file...", command=lambda: popup_menu.post(file_select_button.winfo_rootx(), file_select_button.winfo_rooty() + file_select_button.winfo_height()), bg=Button_Color, highlightthickness=0, font=('Arial', Font_Size))
file_select_button.pack(side=tk.TOP,padx=10, pady=5)

''' Edit Menu Subframe - Edit, Delete, Save, Saved LED'''
edittools = tk.Frame(left_frame,bg="#2F394D")
edittools.pack(side=tk.TOP, padx=5, pady=5)

# Create the "Delete" button
def on_delete_button_click():
    filename = fileselect_var.get()
    if filename == "" or filename == "None":
        set_actionbar("No File Selected.")
        return
    if filename == "_assignments":
        set_actionbar("Cannot Delete That.")
        return
    response = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete\n '{filename}'?")
    if response:
        os.remove(f"{DIR}/channels/{filename}")
        add_to_manifest(filename,"delete")
        refresh_menu()
        file_select_button.config(text="Select a file...")
        upload(False)
        set_actionbar("Deleted File.")

delete_button = tk.Button(edittools, text="Delete", command=on_delete_button_click, bg=Button_Color, highlightthickness=0, font=('Arial', Font_Size))
delete_button.pack(side=tk.LEFT,padx=5, pady=5)

# Create the "Edit" button
WORKING_FILE = ""
def on_edit_button_click():
    global SAVESTATE, WORKING_FILE
    filename = fileselect_var.get()
    if filename == "" or filename == "None":
        actionbar.delete(1.0, tk.END)
        actionbar.insert(tk.END, "No File Selected.")
        return
    if SAVESTATE == False:
        response = messagebox.askyesno("Unsaved Work", f"You have not saved the open file.\nSwitch files anyways?")
        if not response:
            return
        else:
            save(True)
    with open(f"{DIR}/channels/{filename}","r") as file:
        text_box.delete("1.0", tk.END)
        for line in file:
            text_box.insert(tk.END,f"{line.strip()}\n")
        WORKING_FILE = filename
        titlebar.delete(1.0, tk.END)
        titlebar.insert(tk.END, filename)
        set_actionbar("Editing File...")

edit_button = tk.Button(edittools, text="Edit", command=on_edit_button_click, bg=Button_Color, highlightthickness=0, font=('Arial', Font_Size))
edit_button.pack(side=tk.LEFT,padx=5, pady=5)

# Create the "Save" button
def on_save_button_click():
    global WORKING_FILE
    filename = fileselect_var.get()
    # If no file selected, ignore
    if filename == "" or filename == "None":
        actionbar.delete(1.0, tk.END)
        actionbar.insert(tk.END, "No File Selected.")
        return
    # If file selected, content is what's in the text box
    content = text_box.get("1.0", tk.END)
    # get content's title
    go = True
    # if content and selected file don't match, confirm
    if WORKING_FILE != filename:
        if filename == "_assignments" or WORKING_FILE == "_assignments":
            messagebox.showinfo("Illegal", "Cannot write other file types to _assignments or vice versa.")
            set_actionbar("Error Saving File.")
            return
        response = messagebox.askyesno("Overwrite File", f"open file (\"{WORKING_FILE}\") and selected file (\"{filename}\") are not the same. Save anyways?")
        go = response
    # if asked to save (saves to selected file always)
    if go:
        
        path = f"{DIR}/channels/{filename}"
        lines = content.splitlines()
        if filename == "_assignments":
            errormessage = validate_assignments_file(lines)
            if errormessage:
                response = messagebox.askyesno("Compile Error", f"{errormessage}. Reset assigments file?")
                if response:
                    with open(f"{DIR}/channels/_assignments","w") as file:
                        for i in range(1,9):
                            file.write(f"channel{i} <filename>\n")
                    messagebox.showinfo("Compile Error", "Reset assignments file. Press edit to reload, or fix and re-save.")
                    set_actionbar("Error Saving File.")
                else:
                    messagebox.showinfo("Compile Error", "Did not save assignments file.")
                    set_actionbar("Error Saving File.")
            else:
                with open(f"{DIR}/channels/_assignments","w") as file:
                    for line in lines:
                        file.write(f"{line}\n")
                set_actionbar("File Saved.")
                add_to_manifest("_assignments","edit")
                save(True)
                upload(False)
        else:    
            errormessage = validate_channel_file(lines)
            if errormessage:
                messagebox.showinfo("Compile Error", errormessage)
                set_actionbar("Error Saving File.")
                return
            try:
                lines[0] = f"# CHANNEL NAME: {filename}"
                with open(path, "w") as file:
                    for line in lines:
                        file.write(f"{line}\n")
                set_actionbar("File Saved.")
                save(True)
                upload(False)
                add_to_manifest(filename,"edit")
            except Exception as e:
                messagebox.showinfo(f"An error occurred while saving to the file: {e}")
                set_actionbar("Error Saving File.")

save_button = tk.Button(edittools, text="Save", command=on_save_button_click, bg=Button_Color, highlightthickness=0, font=('Arial', Font_Size))
save_button.pack(side=tk.LEFT,padx=5,pady=5)

# Create the "Saved" LED
savedLED = tk.Canvas(edittools, width=LEDsize, height=LEDsize,background=Background_Color, highlightthickness=0)
led = savedLED.create_oval(1, 1, LEDsize, LEDsize, fill="gray")
savedLED.pack(side=tk.LEFT, pady=5)

''' Server Tools Subframe - Connect LED, Connect, Upload, Upload LED'''
servertools = tk.Frame(left_frame,bg=Background_Color)
servertools.pack(side=tk.TOP,padx=5, pady=10)

# Create the "Connect" LED
connectLED = tk.Canvas(servertools, width=LEDsize, height=LEDsize,background=Background_Color, highlightthickness=0)
led = connectLED.create_oval(1, 1, LEDsize, LEDsize, fill="red")
connectLED.pack(side=tk.LEFT, pady=5)

# Create the "Connect" button
def on_connect_button_click():
    connectLED.itemconfig(led, fill="green")
    upload(True)
    set_actionbar("Connected.")

connect_button = tk.Button(servertools, text="Connect", command=on_connect_button_click, bg=Button_Color, highlightthickness=0, font=('Arial', Font_Size))
connect_button.pack(side=tk.LEFT,anchor=tk.SW,padx=5,pady=5)

# Create the "Upload" button
def on_upload_button_click():
    global UPLOAD_STATE
    if UPLOAD_STATE:
        set_actionbar("Nothing to Upload.")
        return
    upload(True)
    if os.path.isfile(f"{DIR}/manifest"):
        os.remove(f"{DIR}/manifest")
    set_actionbar("Uploaded.") 

upload_button = tk.Button(servertools, text="Upload", command=on_upload_button_click, bg=Button_Color, highlightthickness=0, font=('Arial', Font_Size))
upload_button.pack(side=tk.LEFT,anchor=tk.SW,padx=5,pady=5)

# Create the "Connect" LED
uploadLED = tk.Canvas(servertools, width=LEDsize, height=LEDsize,background=Background_Color, highlightthickness=0)
led = uploadLED.create_oval(1, 1, LEDsize, LEDsize, fill="gray")
uploadLED.pack(side=tk.LEFT, pady=5)

''' Assistant Subframe - Actionbar, Help '''
assisttools = tk.Frame(left_frame,bg=Background_Color)
assisttools.pack(side=tk.TOP,padx=5, pady=5)

# Create the "Actionbar"
def set_actionbar(text):
    actionbar.delete(1.0, tk.END)
    actionbar.insert(tk.END, text)

actionbar = tk.Text(assisttools, height=1, width=25,fg=Text_Color, bg=Box_Color, highlightthickness=0, font=('Arial', Font_Size))
actionbar.bind("<Key>", lambda e: "break") # prevents users from editing textbox 
actionbar.pack(side=tk.LEFT,pady=5,fill=tk.X)

# Create the "Help button
def on_help_button_click():
    global SAVESTATE
    if SAVESTATE == False:
        response = messagebox.askyesno("Unsaved Work", f"You have not saved the current file.\nOpen helpfile anyways?")
        if not response:
            return
        else:
            save(True)
    titlebar.delete(1.0, tk.END)
    titlebar.insert(tk.END, "Help File:")
    actionbar.delete(1.0, tk.END)
    actionbar.insert(tk.END, "Dumped Helpfile.")
    text_box.delete("1.0", tk.END)
    with open(f"{DIR}/resources/help.utf8","r") as helpfile:
        content = helpfile.readlines()
        for line in content:
            text_box.insert(tk.END,line)  

help_button = tk.Button(assisttools, text="help", command=on_help_button_click, bg=Button_Color, highlightthickness=0, font=('Arial', Font_Size))
help_button.pack(side=tk.LEFT,anchor=tk.SW,pady=5)

'''
RIGHT FRAME:
The right frame contains a titlebar that displays the current file (if open),
and a text box that can be edited to change the working file. The text box and
scroll bar are packed together in a subframe. The packing order goes:
Titlebar (Top)
Subframe (Top)
   Text (Left)
   Scroll (Right)
'''
right_frame = tk.Frame(root,bg="#2F394D")
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

# Create the "Titlebar"
titlebar = tk.Text(right_frame, height=1, width=3,fg=Text_Color, bg=Box_Color, highlightthickness=0, font=('Arial', Font_Size))
titlebar.bind("<Key>", lambda e: "break") # prevents users from editing textbox 
titlebar.pack(side=tk.TOP,pady=3,fill=tk.X)

# Create the "Text" frame, which holds the text box and scroll bar
texttools = tk.Frame(right_frame,bg=Background_Color)
texttools.pack(side=tk.TOP,fill=tk.BOTH,expand=True,padx=5, pady=5)

# Create the right text box
text_box = tk.Text(texttools, height=10, width=30, fg=Text_Color, bg=Box_Color, highlightthickness=0, font=('Arial', Font_Size))
def on_text_change(args):
    save(False)
text_box.bind("<KeyRelease>", on_text_change) # toggle the save state when edited.
text_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Create scroll bar
scrollbar = tk.Scrollbar(texttools, command=text_box.yview)
text_box.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

'''PRODUCTION'''
if SOUND_ENABLED:
    sound_thread.start()
    
root.mainloop()