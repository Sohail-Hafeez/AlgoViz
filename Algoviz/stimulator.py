import customtkinter as ctk
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

process1 = [] # list for FCFS , SJF and SRJF algorithm
process2 = [] # round ribbon
process3 = [] # priority




# Create the main window
app = ctk.CTk()  # Create an instance of the CTk class
app.title("Stimulator")

valid_username = "a"
valid_password = "a"

def signUp():
    frame.pack_forget()
    frame1.pack(padx=20, pady=50)

frame1 = ctk.CTkFrame(master=app,
                      width=400,
                      height=500,
                      corner_radius=10,
                      bg_color="#000000")  # Using a valid color (black)

# Adding Logo
image = Image.open(r"C:\Users\Mushaf\Desktop\project\Algoviz.png")  # Open the image using PIL directly
logo = ctk.CTkImage(light_image=image, size=(100, 100))  # Pass the PIL image directly to CTkImage

# Create a Label to display the logo
logo_label = ctk.CTkLabel(master=frame1, image=logo, text="")
logo_label.place(x=140, y=30)  # Adjust x, y to overlap with the title text

# Username entry
username_entry1 = ctk.CTkEntry(master=frame1, placeholder_text="Username", width=300, height=40)
username_entry1.place(x=25, y=165)

# Password entry
password_entry1 = ctk.CTkEntry(master=frame1, placeholder_text="Password", width=300, height=40, show="*")
password_entry1.place(x=25, y=225)

def signUp1():
    global valid_username, valid_password  # Access global variables
    # Get the entered username and password
    valid_username = username_entry1.get()
    valid_password = password_entry1.get()
    print(valid_username, valid_password)  # Debugging line to print the values

    frame1.pack_forget()
    frame.pack()

# Sign Up button
b3 = ctk.CTkButton(master=frame1,
                   text="Sign Up",
                   width=150,   # Set the width of the button
                   height=35,   # Set the height of the button
                   fg_color="#0000FF",  # Button color (light blue)
                   hover_color="#2b7ef6",  # Button color on hover
                   border_color="#1a5fb2",  # Border color
                   border_width=2,  # Border width
                   command=signUp1)
b3.place(relx=0.5, rely=0.69, anchor=ctk.CENTER)  # Center the button


def loginButton():
    global valid_username, valid_password  # Access global variables
    # Get the entered username and password
    username = username_entry.get()
    password = password_entry.get()

    # If the credentials are correct
    if username == valid_username and password == valid_password:
        # Destroy the login frame
        frame.destroy()

        # Create and show the dashboard frame
        show_dashboard()
    else:
        # Show the error message panel
        error_message_label.place(relx=0.35, rely=0.45, anchor='center')  # Show error message

def show_dashboard():
    dashboard_frame.pack(fill="both", expand=True)
    dashboard_label.place(x=500,y=5)

dashboard_frame = ctk.CTkFrame(master=app, width=1200, height=700, corner_radius=10)
dashboard_label = ctk.CTkLabel(dashboard_frame, text="Welcome to the ALGOVIZ!", font=("Arial", 30),text_color="#CCCC66")

bframe = ctk.CTkFrame(master = dashboard_frame , width = 300 , height = 400 , corner_radius = 20 )
bframe.place(x = 20 , y = 50)
bframe_label = ctk.CTkLabel(master = bframe, text="Algorithms", font=("Arial", 26),text_color="#CCCC66")
bframe_label.place(x=80,y=10)


# Function to generate the Gantt chart
def generate_gantt_chart(process1, gframe):
    if not process1:
        print("No processes to schedule.")
        return

    # Clear the previous Gantt chart (destroy all children of gframe)
    for widget in gframe.winfo_children():
        widget.destroy()

    # Sort by arrival time
    sorted_processes = sorted(process1, key=lambda x: x["arrival"])

    current_time = 0
    start_times = []
    
    # Define a list of colors to cycle through
    colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink']

    for i, p in enumerate(sorted_processes):
        start = max(current_time, p["arrival"])
        finish = start + p["burst"]
        start_times.append((p["pid"], start, p["burst"]))
        current_time = finish

    # Gantt Chart Plotting
    # Adjust the figure size to fit within the gframe dimensions (700x400)
    fig, ax = plt.subplots(figsize=(7, 4))  # 7, 4 corresponds to 700x400 in pixel scale

    for i, (pid, start, duration) in enumerate(start_times):
        color = colors[i % len(colors)]  # Cycle through colors
        ax.broken_barh([(start, duration)], (10, 9), facecolors=color)
        ax.text(start + duration / 2, 14, pid, ha='center', va='center', color='white', fontsize=9)

    ax.set_ylim(5, 35)
    ax.set_xlim(0, current_time + 2)
    ax.set_xlabel('Time')
    ax.set_yticks([])
    ax.set_title('Gantt Chart - FCFS Scheduling')
    plt.tight_layout()

    # Embed the plot in the tkinter frame (gframe)
    canvas = FigureCanvasTkAgg(fig, master=gframe)  # Create canvas to embed the figure
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)  # Ensure canvas fills the frame
    





FCFS = ctk.CTkButton(master=bframe,
                   text="FCFS",
                   font=("Arial", 20),
                   width=120,   # Set the width of the button
                   height=35,   # Set the height of the button
                   fg_color="#0000FF",  # Button color (light blue)
                   hover_color="#2b7ef6",  # Button color on hover
                   border_color="#1a5fb2",  # Border color
                   border_width=2 , # Border width
                   command=lambda: generate_gantt_chart(process1, gframe))

FCFS.place(relx=0.45, rely=0.2, anchor=ctk.CENTER)


def generate_gantt_chart_sjf(process1, gframe):
    if not process1:
        print("No processes to schedule.")
        return

    # Clear the previous Gantt chart (destroy all children of gframe)
    for widget in gframe.winfo_children():
        widget.destroy()

    # Sort initially by arrival time for tie-breaking
    processes = sorted(process1, key=lambda x: (x["arrival"], x["burst"]))

    current_time = 0
    completed = []
    remaining = processes.copy()
    start_times = []

    while remaining:
        # Get processes that have arrived
        arrived = [p for p in remaining if p["arrival"] <= current_time]
        
        if arrived:
            # Pick process with shortest burst time
            next_process = min(arrived, key=lambda x: x["burst"])
        else:
            # If no process has arrived yet, fast forward time
            current_time = remaining[0]["arrival"]
            continue

        start = max(current_time, next_process["arrival"])
        finish = start + next_process["burst"]
        start_times.append((next_process["pid"], start, next_process["burst"]))
        current_time = finish

        completed.append(next_process)
        remaining.remove(next_process)

    # Define a list of colors to cycle through
    colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink']

    # Plotting the Gantt chart
    fig, ax = plt.subplots(figsize=(7, 4))

    for i, (pid, start, duration) in enumerate(start_times):
        color = colors[i % len(colors)]
        ax.broken_barh([(start, duration)], (10, 9), facecolors=color)
        ax.text(start + duration / 2, 14, pid, ha='center', va='center', color='white', fontsize=9)

    ax.set_ylim(5, 35)
    ax.set_xlim(0, current_time + 2)
    ax.set_xlabel('Time')
    ax.set_yticks([])
    ax.set_title('Gantt Chart - SJF Scheduling')
    plt.tight_layout()

    # Embed the plot in tkinter frame
    canvas = FigureCanvasTkAgg(fig, master=gframe)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)


SJF = ctk.CTkButton(master=bframe,
                   text="SJF",
                   font=("Arial", 20),
                   width=120,   # Set the width of the button
                   height=35,   # Set the height of the button
                   fg_color="#0000FF",  # Button color (light blue)
                   hover_color="#2b7ef6",  # Button color on hover
                   border_color="#1a5fb2",  # Border color
                   border_width=2,  # Border width
                   command=lambda: generate_gantt_chart_sjf(process1, gframe))
SJF.place(relx=0.45, rely=0.35, anchor=ctk.CENTER)


def generate_gantt_chart_srjf(process1, gframe):
    if not process1:
        print("No processes to schedule.")
        return

    for widget in gframe.winfo_children():
        widget.destroy()

    # Create deep copy with remaining burst time
    processes = [{
        "pid": p["pid"],
        "arrival": p["arrival"],
        "burst": p["burst"],
        "remaining": p["burst"]
    } for p in process1]

    time = 0
    complete = 0
    n = len(processes)
    gantt = []

    last_pid = None

    while complete < n:
        # Get all arrived processes with remaining time
        available = [p for p in processes if p["arrival"] <= time and p["remaining"] > 0]

        if available:
            # Select process with shortest remaining time
            current = min(available, key=lambda x: x["remaining"])

            # If different from last running process, add new entry
            if current["pid"] != last_pid:
                gantt.append({"pid": current["pid"], "start": time, "duration": 1})
            else:
                gantt[-1]["duration"] += 1

            current["remaining"] -= 1
            if current["remaining"] == 0:
                complete += 1

            last_pid = current["pid"]
        else:
            # CPU idle
            if last_pid != "IDLE":
                gantt.append({"pid": "IDLE", "start": time, "duration": 1})
            else:
                gantt[-1]["duration"] += 1
            last_pid = "IDLE"

        time += 1

    # Define a list of colors to cycle through
    colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink']
    pid_color_map = {}
    color_index = 0

    # Plotting Gantt chart
    fig, ax = plt.subplots(figsize=(7, 4))

    for segment in gantt:
        pid = segment["pid"]
        start = segment["start"]
        duration = segment["duration"]

        if pid not in pid_color_map:
            if pid == "IDLE":
                pid_color_map[pid] = 'gray'
            else:
                pid_color_map[pid] = colors[color_index % len(colors)]
                color_index += 1

        color = pid_color_map[pid]
        ax.broken_barh([(start, duration)], (10, 9), facecolors=color)
        ax.text(start + duration / 2, 14, pid, ha='center', va='center', color='white', fontsize=8)

    ax.set_ylim(5, 35)
    ax.set_xlim(0, time + 2)
    ax.set_xlabel('Time')
    ax.set_yticks([])
    ax.set_title('Gantt Chart - SRJF Scheduling')
    plt.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=gframe)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)


SRJF = ctk.CTkButton(master=bframe,
                   text="SRJF",
                   font=("Arial", 20),
                   width=120,   # Set the width of the button
                   height=35,   # Set the height of the button
                   fg_color="#0000FF",  # Button color (light blue)
                   hover_color="#2b7ef6",  # Button color on hover
                   border_color="#1a5fb2",  # Border color
                   border_width=2 , # Border width
                   command=lambda: generate_gantt_chart_srjf(process1, gframe))
SRJF.place(relx=0.45, rely=0.50, anchor=ctk.CENTER)

def generate_rr_gantt_chart(process2, gframe):
    if not process2:
        print("No processes to schedule.")
        return

    # Clear previous chart
    for widget in gframe.winfo_children():
        widget.destroy()

    # Extract global time quantum (assume all are the same, take from first)
    time_quantum = process2[0]["timeQuantum"]

    # Sort by arrival time
    processes = sorted(process2, key=lambda x: x["arrival"])
    remaining_burst = {p["pid"]: p["burst"] for p in processes}
    arrival_dict = {p["pid"]: p["arrival"] for p in processes}

    ready_queue = []
    current_time = 0
    gantt = []
    arrived = []

    while remaining_burst:
        # Add newly arrived processes
        for p in processes:
            if p["arrival"] <= current_time and p["pid"] not in arrived:
                ready_queue.append(p["pid"])
                arrived.append(p["pid"])

        if not ready_queue:
            current_time += 1
            continue

        pid = ready_queue.pop(0)
        exec_time = min(time_quantum, remaining_burst[pid])
        gantt.append((pid, current_time, exec_time))
        current_time += exec_time
        remaining_burst[pid] -= exec_time

        # Add newly arrived during execution
        for p in processes:
            if p["arrival"] <= current_time and p["pid"] not in arrived:
                ready_queue.append(p["pid"])
                arrived.append(p["pid"])

        if remaining_burst[pid] > 0:
            ready_queue.append(pid)
        else:
            del remaining_burst[pid]

    # Plot Gantt Chart
    fig, ax = plt.subplots(figsize=(7, 4))
    colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink']
    color_map = {}

    for i, (pid, start, duration) in enumerate(gantt):
        if pid not in color_map:
            color_map[pid] = colors[len(color_map) % len(colors)]
        ax.broken_barh([(start, duration)], (10, 9), facecolors=color_map[pid])
        ax.text(start + duration / 2, 14, pid, ha='center', va='center', color='white', fontsize=9)

    ax.set_ylim(5, 35)
    ax.set_xlim(0, current_time + 2)
    ax.set_xlabel('Time')
    ax.set_yticks([])
    ax.set_title('Gantt Chart - Round Robin Scheduling')
    plt.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=gframe)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)


RR = ctk.CTkButton(master=bframe,
                   text="RR",
                   font=("Arial", 20),
                   width=120,   # Set the width of the button
                   height=35,   # Set the height of the button
                   fg_color="#0000FF",  # Button color (light blue)
                   hover_color="#2b7ef6",  # Button color on hover
                   border_color="#1a5fb2",  # Border color
                   border_width=2 , # Border width
                   command=lambda: generate_rr_gantt_chart(process2, gframe))
RR.place(relx=0.45, rely=0.65, anchor=ctk.CENTER)

def generate_priority_gantt_chart(process3, gframe):
    if not process3:
        print("No processes to schedule.")
        return

    # Clear previous chart
    for widget in gframe.winfo_children():
        widget.destroy()

    # Sort processes by arrival time first, then by priority
    sorted_processes = sorted(process3, key=lambda x: (x["arrival"], x["priority"]))

    current_time = 0
    completed = []
    gantt_data = []

    while len(completed) < len(sorted_processes):
        # Get ready queue (processes that have arrived and not completed)
        ready_queue = [p for p in sorted_processes if p["arrival"] <= current_time and p not in completed]

        if not ready_queue:
            current_time += 1
            continue

        # Select process with highest priority (lowest number = higher priority)
        current_process = min(ready_queue, key=lambda x: x["priority"])
        start_time = current_time
        end_time = start_time + current_process["burst"]

        gantt_data.append((current_process["pid"], start_time, current_process["burst"]))
        current_time = end_time
        completed.append(current_process)

    # Plotting
    fig, ax = plt.subplots(figsize=(7, 3))
    colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink']
    color_map = {}

    for i, (pid, start, duration) in enumerate(gantt_data):
        if pid not in color_map:
            color_map[pid] = colors[i % len(colors)]
        ax.broken_barh([(start, duration)], (10, 9), facecolors=color_map[pid])
        ax.text(start + duration / 2, 14, pid, ha='center', va='center', color='white', fontsize=9)

    ax.set_ylim(5, 30)
    ax.set_xlim(0, current_time + 2)
    ax.set_xlabel('Time')
    ax.set_yticks([])
    ax.set_title('Gantt Chart - Priority Scheduling (Non-Preemptive)')
    plt.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=gframe)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)


PriorityQ = ctk.CTkButton(master=bframe,
                   text="Priority",
                   font=("Arial", 20),
                   width=120,   # Set the width of the button
                   height=35,   # Set the height of the button
                   fg_color="#0000FF",  # Button color (light blue)
                   hover_color="#2b7ef6",  # Button color on hover
                   border_color="#1a5fb2",  # Border color
                   border_width=2,  # Border width
                   command=lambda: generate_priority_gantt_chart(process3, gframe))
PriorityQ.place(relx=0.45, rely=0.80, anchor=ctk.CENTER)

pframe = ctk.CTkFrame(master = dashboard_frame , width = 300 , height = 400 , corner_radius = 20 )
pframe.place(x = 1050 , y = 50)
pframe_label = ctk.CTkLabel(master = pframe, text="Add Process", font=("Arial", 22),text_color="#CCCC66")
pframe_label.place(x=70,y=10)

# textField entry
pname = ctk.CTkEntry(master=pframe, placeholder_text="", width=250, height=38)
pname.place(x=25, y=60)
pname_label = ctk.CTkLabel(master = pframe, text="Process Name", font=("Arial", 15),text_color="#CCCC66")
pname_label.place(x=30,y=44)

pArivalTime = ctk.CTkEntry(master=pframe, placeholder_text="", width=250, height=38)
pArivalTime.place(x=25, y=120)
pname_label = ctk.CTkLabel(master = pframe, text="Process Arival Time", font=("Arial", 15),text_color="#CCCC66")
pname_label.place(x=30,y=104)

pBustTime = ctk.CTkEntry(master=pframe, placeholder_text="", width=250, height=38)
pBustTime.place(x=25, y=175)
pBust_label = ctk.CTkLabel(master = pframe, text="Process Bust Time", font=("Arial", 15),text_color="#CCCC66")
pBust_label.place(x=30,y=160)

pPriority = ctk.CTkEntry(master=pframe, placeholder_text="", width=250, height=38)
pPriority.place(x=25, y=230)
pPriority_label = ctk.CTkLabel(master = pframe, text="Process Priority", font=("Arial", 15),text_color="#CCCC66")
pPriority_label.place(x=30,y=215)

pTimeQuantum = ctk.CTkEntry(master=pframe, placeholder_text="", width=250, height=38)
pTimeQuantum.place(x=25, y=285)
pTimeQuantumy_label = ctk.CTkLabel(master = pframe, text="ProcessTime Quantum", font=("Arial", 15),text_color="#CCCC66")
pTimeQuantumy_label.place(x=30,y=270)

# function for add process button
def add():
    
    name = pname.get()
    arrival = int(pArivalTime.get())
    burst = int(pBustTime.get())
    priority = int(pPriority.get())
    timeQuantum = int(pTimeQuantum.get())

    process1.append({"pid": name, "arrival": arrival, "burst": burst})
    process2.append({"pid": name, "arrival": arrival, "burst": burst, "timeQuantum" : timeQuantum})
    process3.append({"pid": name, "arrival": arrival, "burst": burst, "priority" : priority })
    print(f"Added: {process1[-1]}")
    pname.delete(0, ctk.END)
    pArivalTime.delete(0, ctk.END)
    pBustTime.delete(0, ctk.END)
    pPriority.delete(0, ctk.END)



addProcess = ctk.CTkButton(master=pframe,
                   text="Add Process",
                   font=("Arial", 20),
                   width=150,   # Set the width of the button
                   height=35,   # Set the height of the button
                   fg_color="#0000FF",  # Button color (light blue)
                   hover_color="#2b7ef6",  # Button color on hover
                   border_color="#1a5fb2",  # Border color
                   border_width=2,  # Border width
                   command = add)
addProcess.place(relx=0.45, rely=0.90, anchor=ctk.CENTER)

gframe = ctk.CTkFrame(master = dashboard_frame , width = 700 , height = 400 , corner_radius = 20 )
gframe.place(x = 330 , y = 50)

sframe = ctk.CTkFrame(master = dashboard_frame , width = 630 , height = 210 , corner_radius = 20 )
sframe.place(x = 20 , y = 470)

fframe = ctk.CTkFrame(master = dashboard_frame , width = 630 , height = 210 , corner_radius = 20 )
fframe.place(x = 680 , y = 470)

# Set the appearance and color theme
ctk.set_appearance_mode("system")  # Sets the appearance mode to system default (light or dark)
ctk.set_default_color_theme("blue")  # Sets the default color theme to blue


# Get screen size
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
print(screen_width)
print(screen_height)
# Set the window size to the screen size
app.geometry("1200x700")

# Create a frame inside the main window
frame = ctk.CTkFrame(master=app,
                     width=400,
                     height=600,
                     corner_radius=10,
                     bg_color="#000000")  # Using a valid color (white)

frame.pack(padx=20, pady=50)

# Adding Logo
image = Image.open(r"C:\Users\Mushaf\Desktop\project\Algoviz.png")  # Open the image using PIL directly
logo = ctk.CTkImage(light_image=image, size=(100, 100))  # Pass the PIL image directly to CTkImage

# Create a Label to display the logo
logo_label = ctk.CTkLabel(master=frame, image=logo, text="")
logo_label.place(x=140, y=30)  # Adjust x, y to overlap with the title text

# Create the "Login" button
b1 = ctk.CTkButton(master=frame,
                   text="Login",
                   font=("Arial", 20),
                   width=200,   # Set the width of the button
                   height=40,   # Set the height of the button
                   fg_color="#0000FF",  # Button color (light blue)
                   hover_color="#2b7ef6",  # Button color on hover
                   border_color="#1a5fb2",  # Border color
                   border_width=2,   # Border width
                   command=loginButton)
b1.place(relx=0.45, rely=0.53, anchor=ctk.CENTER)

# Username entry
username_entry = ctk.CTkEntry(master=frame, placeholder_text="Username", width=300, height=40)
username_entry.place(x=25, y=150)

# Password entry
password_entry = ctk.CTkEntry(master=frame, placeholder_text="Password", width=300, height=40, show="*")
password_entry.place(x=25, y=210)

# Register prompt
register_label = ctk.CTkLabel(master=frame, text="Don't have an account? ", font=("Arial", 15), text_color="#CCCC66")
register_label.place(x=50, y=400)

# Create the "Sign Up" button
b2 = ctk.CTkButton(master=frame,
                   text="Sign Up",
                   font=("Arial", 17),
                   width=70,   # Set the width of the button
                   height=25,   # Set the height of the button
                   fg_color="#0000FF",  # Button color (light blue)
                   hover_color="#2b7ef6",  # Button color on hover
                   border_color="#1a5fb2",  # Border color
                   border_width=2,  # Border width
                   command=signUp)
b2.place(relx=0.65, rely=0.69, anchor=ctk.CENTER)

# Create the error message label (initially hidden)
error_message_label = ctk.CTkLabel(frame, text="Invalid username or password", font=("Arial", 15), text_color="#CCCC66")
error_message_label.place(relx=0.5, rely=0.75, anchor='center')
error_message_label.place_forget()  # Hide the error message initially

# Start the main loop
app.mainloop()
