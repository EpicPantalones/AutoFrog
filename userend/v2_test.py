import tkinter as tk

def show_frame(frame):
    # Hide all frames
    main_frame.pack_forget()
    niche_frame.pack_forget()
    settings_frame.pack_forget()

    # Show the selected frame
    frame.pack(fill=tk.BOTH, expand=True)

# Create the main tkinter window
main_window = tk.Tk()
main_window.configure(bg='lightblue')
main_window.title("AutoFrog Tool")

# Create the main frame with buttons
main_frame = tk.Frame(main_window)
main_frame.pack(fill=tk.BOTH, expand=True)

main_label = tk.Label(main_frame, text="Main Frame", font=("Helvetica", 18))
main_label.pack(pady=20)

niche_button = tk.Button(main_frame, text="Niche Frame", command=lambda: show_frame(niche_frame))
niche_button.pack()

settings_button = tk.Button(main_frame, text="Settings Frame", command=lambda: show_frame(settings_frame))
settings_button.pack()

# Create the niche frame with buttons
niche_frame = tk.Frame(main_window)
niche_label = tk.Label(niche_frame, text="Niche Frame", font=("Helvetica", 18))
niche_label.pack(pady=20)

back_button_niche = tk.Button(niche_frame, text="Back to Main", command=lambda: show_frame(main_frame))
back_button_niche.pack()

# Create the settings frame with buttons
settings_frame = tk.Frame(main_window)
settings_label = tk.Label(settings_frame, text="Settings Frame", font=("Helvetica", 18))
settings_label.pack(pady=20)

back_button_settings = tk.Button(settings_frame, text="Back to Main", command=lambda: show_frame(main_frame))
back_button_settings.pack()

# Initially, show the main frame
show_frame(main_frame)

main_window.mainloop()
