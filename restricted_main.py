import tkinter as tk
from tkinter import ttk
from tkinter import StringVar
import threading
import functions as fn
import re
import time

# Create the columns
truck_col = ['Body Number', 'Plate Number', 'Date Aquired', 
             'Model', 'Unit Description', 'Serial Number', 
             'Engine Number', 'Status', 'Location']

truck_entry_col = ['Body Number (6 chars) ', 'Plate Number (8 chars)', 'Date Aquired (mm/yyyy)', 
             'Model (max 10 chars)', 'Unit Description (16 chars)', 'Serial Number (18 chars) ', 
             'Engine Number (20 chars) ', 'Status (ACTIVE/INACTIVE/SOLD)', 'Location (20 chars)']

repair_entry_col = ['Body Number (6 chars)','Truck Plate No (8 chars)','Date (mm/yyyy)','Location (20 chars)','Amount','Work Done (160 chars)']
repair_col = ['Body Number','Truck Plate No','Date','Location','Amount','Work Done']

plate_no = "test"
body_no = "test"

truck_error = None
repair_error = None
truck_entry_error = None
change_status_error = None
time_frame_error = None
location_error = None

all_trucks = None
active_trucks = None
inactive_trucks = None
sold_trucks = None

all_locations = set()
all_plate_no = set()
all_body_no = set()

def change_to_list():
    global all_locations, all_body_no
    while not (all_locations and all_plate_no and all_body_no):
        time.sleep(1)
    if isinstance(all_locations, set):
        all_locations = list(all_locations)
        all_locations.sort()
        print(all_locations)
    if isinstance(all_body_no, set):
        all_body_no = list(all_body_no)
        all_body_no.sort()
        print(all_body_no)
threading.Thread(target=change_to_list, daemon=True).start()

# Build the sets
def get_all_trucks():
    global all_trucks
    all_trucks = fn.get_request()
threading.Thread(target=get_all_trucks, daemon=True).start()

def get_all_locations():
    global all_trucks, all_locations
    time.sleep(4)
    while (not all_trucks):
        get_all_locations()
    for i in range(len(all_trucks)):
        all_locations.add(str(all_trucks[i][8]))
    print(all_locations)
threading.Thread(target=get_all_locations, daemon=True).start()

def get_all_plate_no():
    global all_trucks, all_plate_no
    time.sleep(4)
    while (not all_trucks):
        get_all_locations()
    for i in range(len(all_trucks)):
        all_plate_no.add(str(all_trucks[i][1]))
    print(all_plate_no)
threading.Thread(target=get_all_plate_no, daemon=True).start()

def get_all_body_no():
    global all_trucks, all_body_no
    time.sleep(4)
    while (not all_trucks):
        get_all_locations()
    for i in range(len(all_trucks)):
        all_body_no.add(str(all_trucks[i][0]))
    print(all_body_no)
threading.Thread(target=get_all_body_no, daemon=True).start()

def get_all_active():
    global active_trucks
    active_trucks = fn.get_request(status='active')
    
def get_all_inactive():
    global inactive_trucks
    inactive_trucks = fn.get_request(status='inactive')

def get_all_sold():
    global sold_trucks
    sold_trucks = fn.get_request(status='sold')

# Define functions
def show_frame(frame):
    frame.tkraise()

def move_to_truck_entry():
    global truck_entry_error, all_body_no
    while not all_body_no or not isinstance(all_body_no, list):
        time.sleep(1)
    for widget in entry_frame.winfo_children():
        widget.destroy()
    show_frame(entry_frame)
    space = tk.Label(entry_frame, text="", font=("Helvetica", 16))
    space.pack(pady=60)
    add_title = tk.Label(entry_frame, text="Search for Truck", font=("Helvetica", 16))
    add_title.pack(pady=5) 
    setup_entry_form('Search for truck')
    truck_entry_error = tk.Label(entry_frame, text="", fg='red', font=("Arial", 12))
    truck_entry_error.pack(pady=20)

def move_to_truck_pg(entries):
    global plate_no, body_no
    while(not all_body_no or not all_plate_no):
        time.sleep(1)
    if not entries[1] and not entries[0]:
        truck_entry_error.config(text='Error: Cannot have empty Entry')
    elif entries[1] and entries[1] not in all_plate_no:
        truck_entry_error.config(text='Error: Plate Number not in Truck List')
    elif entries[0] and entries[0] not in all_body_no:
        truck_entry_error.config(text='Error: Body Number not in Truck List')
    else:
        plate_no = entries[1]
        body_no = entries[0]
        if not body_no:
            print("Body_no = None")
        if not plate_no:
            print("Plate_no = None")
        show_frame(truck_frame)
      
def move_to_active_pg():
    show_frame(active_frame)
    threading.Thread(target=get_all_active, daemon=True).start()
    threading.Thread(target=get_all_inactive, daemon=True).start()
    threading.Thread(target=get_all_sold, daemon=True).start()
    
def move_to_update_truck_pg():
    global change_status_error
    for widget in entry_frame.winfo_children():
        widget.destroy()
    show_frame(entry_frame)
    space = tk.Label(entry_frame, text="", font=("Helvetica", 16))
    space.pack(pady=60)
    add_title = tk.Label(entry_frame, text="Change Status or Location", font=("Helvetica", 16))
    add_title.pack(pady=5) 
    setup_entry_form('Change status or location')
    change_status_error = tk.Label(entry_frame, text="", fg='red', font=("Arial", 12))
    change_status_error.pack(pady=20)

def move_to_time_frame_pg():
    global time_frame_error
    for widget in entry_frame.winfo_children():
        widget.destroy()
    show_frame(entry_frame)
    space = tk.Label(entry_frame, text="", font=("Helvetica", 16))
    space.pack(pady=60)
    add_title = tk.Label(entry_frame, text="Search Repairs within Time frame", font=("Helvetica", 16))
    add_title.pack(pady=5) 
    setup_entry_form('Search for time')
    truck_error = tk.Label(entry_frame, text="", fg='red', font=("Arial", 12))
    truck_error.pack(pady=20)

def add_new_truck_pg():
    global truck_error
    for widget in entry_frame.winfo_children():
        widget.destroy()
    show_frame(entry_frame)
    add_title = tk.Label(entry_frame, text="Add Truck", font=("Helvetica", 16))
    add_title.pack(pady=20)  
    setup_entry_form(truck_entry_col)
    truck_error = tk.Label(entry_frame, text="", fg='red', font=("Arial", 12))
    truck_error.pack(pady=20)
    
def add_new_repair_pg():
    global repair_error
    for widget in entry_frame.winfo_children():
        widget.destroy()
    show_frame(entry_frame)
    add_title = tk.Label(entry_frame, text="Add Repair", font=("Helvetica", 16))
    add_title.pack(pady=20)  
    setup_entry_form(repair_entry_col)
    repair_error = tk.Label(entry_frame, text="", fg='red', font=("Arial", 12))
    repair_error.pack(pady=40)

def back_main_pg():
    show_frame(main_frame)

def back_truck_pg():
    show_frame(truck_frame)

def show_database(status=None, location=None, plate_no=None, body_no=None, start=None, end=None):
    global all_trucks
    if plate_no:
        print("plate no: " + plate_no)
    else:
        print("No plate number")
    
    if body_no:
        print("body no: " + body_no)
    else:
        print("No body no")
    
    # Create a new window
    window = tk.Toplevel()
    window.title("Database View")
    window.geometry("900x400")
    
    columns = repair_col if (plate_no or body_no) else truck_col
    if (columns == repair_col and status == 'location'):
        columns = truck_col

    # Create a Treeview widget
    tree = ttk.Treeview(window, columns=columns, show='headings')

    # Define column headings
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor='center')

    # Add a scrollbar
    scrollbar = tk.Scrollbar(window, orient='vertical', command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side='right', fill='y')

    # Pack the Treeview widget
    tree.pack(expand=True, fill='both')

    if(all_trucks and ((not status) and (not location) and (not plate_no) and (not body_no))):
        for row in all_trucks:
            tree.insert('', tk.END,values=row)
    
    elif(active_trucks and (status == 'active')):
        for row in active_trucks:
            tree.insert('', tk.END,values=row)
    
    elif(inactive_trucks and (status == 'inactive')):
        for row in inactive_trucks:
            tree.insert('', tk.END,values=row)
    
    elif(sold_trucks and (status == 'sold')):
        for row in sold_trucks:
            tree.insert('', tk.END,values=row)
    
    else:
        def update_treeview():
            data = fn.get_request(status=status, location=location, plate_no=plate_no, body_no=body_no, start=start, end=end)  # Load data
            if len(data) == 0:
                if columns == repair_col:
                    data = [["None"]*len(repair_col)]
                elif columns == truck_col:
                    data = [["None"]*len(truck_col)]
            print(data)
            for row in data:
                tree.insert('', tk.END, values=row)
            
        # Run data loading in a separate thread
        threading.Thread(target=update_treeview, daemon=True).start()

def is_valid_truck_data(data):
    global truck_error
    for entry in data:
        if len(entry) == 0:
            truck_error.config(text="Error: Missing Entry")
            return False
    
    if len(data[0]) > 6:
        truck_error.config(text="Error: Body Number is too long")
        return False
             
    elif len(data[1]) > 8 or len(data[1]) < 6:
        truck_error.config(text='Error: Plate Number is wrong')
        return False
    
    elif re.fullmatch(r"^(0[1-9]|1[0-2])/(\d{4})$",data[2]) is None :
        truck_error.config(text='Error: Date is in wrong format')
        return False
    
    elif len(data[3]) > 10:
        truck_error.config(text="Error: Model is too long")
        return False
    
    elif len(data[4]) > 16:
        truck_error.config(text="Error: Unit Description is too long")
        return False
    
    elif len(data[5]) > 18:
        truck_error.config(text="Error: Serial Number is too long")
        return False
    
    elif len(data[6]) > 20:
        truck_error.config(text="Error: Engine Number is too long")
        return False
    
    elif data[7] not in ('ACTIVE','INACTIVE','SOLD'):
        truck_error.config(text="Error: Status is not active/inactive/sold")
        return False
 
    return True

def is_valid_repair_data(data):
    global repair_error
    for entry in data:
            if len(entry) == 0:
                repair_error.config(text="Error: Missing Entry")
                return False
        
    for i in (0,2,4):
        data[i] = data[i].replace(" ", '')
    
    if len(data[0]) > 6:
        repair_error.config(text='Error: Body Number is too long')
        return False
    
    if len(data[1]) > 8:
        repair_error.config(text="Error: Plate Number is too long")
        return False
    
    elif re.fullmatch(r"^(0[1-9]|1[0-2])/(\d{4})$",data[2]) is None :
        repair_error.config(text="Error: Date is in wrong format")
        return False
    
    elif len(data[3]) > 20:
        repair_error.config(text="Error: Location is too long")
        return False
    
    elif len(data[5]) > 160:
        repair_error.config(text="Error: Work Done is too long")
        return False
    
    elif not data[4].isdigit():
        repair_error.config(text="Error: Amount is not a number")
        return False

    return True

def submit_data(data, type=None):
    # This function will handle submitting the entered data to the appropriate place
    if len(data) == len(truck_col):  # Assuming data length matches the truck columns
        global all_body_no, all_locations, all_plate_no, all_trucks
        
        # Preprocess data
        for i in (0,1,2,5,6,7):
            data[i] = data[i].replace(" ", '')
        for i in (0,1,7,8):
            data[i] = data[i].upper()
        
        while (isinstance(all_body_no, set) or isinstance(all_locations, set)):
            time.sleep(1)
        
        if is_valid_truck_data(data): 
            threading.Thread(target=lambda: fn.post_request(data=data, type='truck'), daemon=True).start()
            all_body_no.append(data[0])
            all_body_no = all_body_no.sort()
            if data[8] not in all_locations:
                all_locations.append(data[8])
                all_locations.sort()
            all_plate_no.append(data[1])
            all_trucks.append(data)
            print(all_locations)
            print(all_body_no)
            print(all_plate_no)
            back_main_pg()
            
    elif len(data) == len(repair_col):  # Assuming data length matches the trip columns
        
        for i in (0,1,3,4):
            data[i] = data[i].replace(" ", '')
        
        for i in (0,1,3,4):
            data[i] = data[i].upper()
        
        data[4] = data[4].replace(',','')
        
        if is_valid_repair_data(data):
            threading.Thread(target=lambda: fn.post_request(data=data, type='repair'), daemon=True).start()
            back_main_pg()
    
    elif len(data) == 2:
        if type == 'change':
            data[0] = data[0].upper()
            if data[0] not in ('ACTIVE','INACTIVE','SOLD'):
                change_status_error.config(text='Error: Status is not ACTIVE/INACTIVE/SOLD')
            elif len(data[1]) > 20:
                change_status_error.config(text='Error: Location is too long')
            else:
                new_status = None
                new_location = None
                if data[0]:
                    new_status = data[0]
                if data[1]:
                    new_location = data[1]
                threading.Thread(target=lambda: fn.post_request(new_status=new_status if new_status else None, new_location=new_location if new_location else None, plate_no=plate_no if plate_no else None, body_no=body_no if body_no else None), daemon=True).start()
                back_truck_pg()
        elif type == 'time':
            if re.fullmatch(r"^(0[1-9]|1[0-2])/(\d{4})$",data[0]) is None:
                time_frame_error.config(text='Error: Date is in wrong format')
            elif re.fullmatch(r"^(0[1-9]|1[0-2])/(\d{4})$",data[1]) is None:
                time_frame_error.config(text='Error: Date is in wrong format')
            else:
                show_database(start=data[0], end=data[1], plate_no=plate_no if plate_no else None, body_no=body_no if body_no else None)
                
def setup_entry_form(columns=None):
    
    # Create a frame for entry_frame entries
    sub_entry_frame = tk.Frame(entry_frame) 
    sub_entry_frame.pack(expand=True)
    
    global add_title
    # Clear the entry_frame
    for widget in sub_entry_frame.winfo_children():
        widget.destroy()
    
    if columns == 'Location':
        global all_locations
        entries = []
        text = 'Enter the location:  '
        selected_option = StringVar()
        selected_option.set("Enter Location")
        tk.Label(sub_entry_frame, text=text).grid(row=0, column=0, padx=10, pady=5) 
        dropdown = tk.OptionMenu(sub_entry_frame, selected_option, *all_locations)
        dropdown.grid(row=0, column=1, padx=10, pady=5)
        entries.append(selected_option) 
        
        # Create a Search button
        confirm_btn = tk.Button(sub_entry_frame, text="Search Location",command=lambda: see_location(entries[0].get()))
        confirm_btn.grid(row=1, column=0, columnspan=2, pady=20)
        
        # Create a back button
        back_btn = tk.Button(sub_entry_frame, text="Back", command=back_main_pg)
        back_btn.grid(row=2, column=0, columnspan=2, pady=10)
    
    elif columns == 'Search for truck':
        global all_body_no
        entries = []
        text = ['Find the truck body number:  ', 'Enter the truck plate number:  ']
        selected_option = StringVar()
        selected_option.set("Body Number")
        tk.Label(sub_entry_frame, text=text[0]).grid(row=0, column=0, padx=10, pady=5) 
        dropdown = tk.OptionMenu(sub_entry_frame, selected_option, *all_body_no)
        dropdown.grid(row=0, column=1, padx=10, pady=5)
        entries.append(selected_option) 
        tk.Label(sub_entry_frame, text='or').grid(row=1, column=0,columnspan=2,padx=10, pady=5)
        tk.Label(sub_entry_frame, text=text[1]).grid(row=2, column=0, padx=10, pady=5) 
        entry = tk.Entry(sub_entry_frame)
        entry.grid(row=2, column=1, padx=10, pady=5)  
        entries.append(entry)
        
        # Create a Search button
        confirm_btn = tk.Button(sub_entry_frame, text="Search Truck",command=lambda: move_to_truck_pg([entry.get() for entry in entries]))
        confirm_btn.grid(row=3, column=0, columnspan=2, pady=20)
        
        # Create a back button
        back_btn = tk.Button(sub_entry_frame, text="Back", command=back_main_pg)
        back_btn.grid(row=4, column=0, columnspan=2, pady=10)
        
    
    elif columns == 'Change status or location':
        entries = []
        text = ['Enter the new status (ACTIVE, INACTIVE, SOLD):  ', 'Enter the new location (20 chars):  ']
        for idx, col in enumerate(text):
            tk.Label(sub_entry_frame, text=col).grid(row=2*idx, column=0, padx=10, pady=5) 
            entry = tk.Entry(sub_entry_frame)
            entry.grid(row=2*idx, column=1, padx=10, pady=5)  
            entries.append(entry)
        tk.Label(sub_entry_frame, text='or').grid(row=1, column=0,columnspan=2,padx=10, pady=5)
        
        # Create a Confirm button
        confirm_btn = tk.Button(sub_entry_frame, text="Confirm",command=lambda: submit_data([entry.get() for entry in entries], type='change'))
        confirm_btn.grid(row=3, column=0, columnspan=2, pady=20)
        
        # Create a back button
        back_btn = tk.Button(sub_entry_frame, text="Back", command=back_truck_pg)
        back_btn.grid(row=4, column=0, columnspan=2, pady=10)
        
        
    elif columns == 'Search for time':
        add_title = tk.Label(entry_frame, text="Search Repairs within Time frame", font=("Helvetica", 16))
        entries = []
        text = ['Starting Month (mm/yyyy):  ', 'Ending Month (mm/yyyy):  ']
        for idx, col in enumerate(text):
            tk.Label(sub_entry_frame, text=col).grid(row=2*idx, column=0, padx=10, pady=5) 
            entry = tk.Entry(sub_entry_frame)
            entry.grid(row=2*idx, column=1, padx=10, pady=5)  
            entries.append(entry)
        tk.Label(sub_entry_frame, text='or').grid(row=1, column=0,columnspan=2,padx=10, pady=5)
        
        # Create a Confirm button
        confirm_btn = tk.Button(sub_entry_frame, text="Confirm",command=lambda: submit_data([entry.get() for entry in entries], type='time'))
        confirm_btn.grid(row=3, column=0, columnspan=2, pady=20)
        
        # Create a back button
        back_btn = tk.Button(sub_entry_frame, text="Back", command=back_truck_pg)
        back_btn.grid(row=4, column=0, columnspan=2, pady=10)
    
    else:
        # Create Entry widgets for each column
        entries = []
        for idx, col in enumerate(columns):
            if (idx == 5 and columns == repair_entry_col):
                tk.Label(sub_entry_frame, text=col).grid(row=idx, column=0, padx=10, pady=5) 
                text_widget = tk.Text(sub_entry_frame, height=8, width=20, font='TkTextFont')
                text_widget.grid(row=idx, column=1, padx=10, pady=5)
                entries.append(text_widget)
            else: 
                tk.Label(sub_entry_frame, text=col).grid(row=idx, column=0, padx=10, pady=5) 
                entry = tk.Entry(sub_entry_frame)
                entry.grid(row=idx, column=1, padx=10, pady=5)  
                font_value = entry.cget("font")
                entries.append(entry)
            
        # Create a submit button
        submit_btn = tk.Button(sub_entry_frame, text="Submit", command=lambda: submit_data([entry.get("1.0", tk.END).strip() if isinstance(entry, tk.Text) else entry.get().strip() for entry in entries]))
        submit_btn.grid(row=len(columns), column=0, columnspan=2, pady=20)

        # Create a back button
        back_btn = tk.Button(sub_entry_frame, text="Back", command=back_main_pg)
        back_btn.grid(row=len(columns) + 1, column=0, columnspan=2, pady=10)

def show_by_location():
    global location_error, all_locations
    while not (all_locations) or not isinstance(all_locations, list):
        time.sleep(1)
    for widget in entry_frame.winfo_children():
        widget.destroy()
    show_frame(entry_frame)
    add_title = tk.Label(entry_frame, text="Search by Location", font=("Helvetica", 16))
    add_title.pack(pady=20)  
    setup_entry_form("Location")
    location_error = tk.Label(entry_frame, text="", fg='red', font=("Arial", 12))
    location_error.pack(pady=40)

def see_location(location):
    global location_error
    location = location.upper()
    while not all_locations:
        time.sleep(1)
    if not location:
        location_error.config(text="Error: Empty Location")
    elif len(location) > 20:
        location_error.config(text="Error: Location is too long")
    elif location not in all_locations:
        location_error.config(text="Error: Location not found")
    else:
        show_database(location=location)


# Create the main window
root = tk.Tk()
root.geometry("800x600")

# Main Frame
main_frame = tk.Frame(root)

# Create the main_frame title label
main_title = tk.Label(main_frame, text="Truck Database", font=("Helvetica", 16))
main_title.pack(pady=20)  

# Create a frame for main_frame buttons
main_button_frame = tk.Frame(main_frame)
main_button_frame.pack(expand=True)

# Create main_frame buttons and assign actions
main_buttons = [
    ("Show all trucks", lambda: show_database()),
    ("Show all active/inactive trucks", move_to_active_pg),
    ("Check a truck", move_to_truck_entry),
    ("Add a new truck", add_new_truck_pg),
    ("Add a new repair", add_new_repair_pg),
    ("Search all in a location", show_by_location)
]

for text, command in main_buttons:
    btn = tk.Button(main_button_frame, text=text, command=command)
    btn.pack(pady=10, padx=20, fill='x')  # Reduced vertical padding

# Active/Inactive Frame
active_frame = tk.Frame(root)

# Create the active_frame title label
active_title = tk.Label(active_frame, text="Choose the status", font=("Helvetica", 16))
active_title.pack(pady=20)  

# Create a frame for active_frame buttons
active_button_frame = tk.Frame(active_frame)
active_button_frame.pack(expand=True)

# Create active_frame buttons and assign actions
active_buttons = [
    ("Show all active trucks", lambda: show_database(status='active')),
    ("Show all inactive trucks", lambda: show_database(status='inactive')),
    ("Show all sold trucks", lambda: show_database(status='sold')),
]

for text, command in active_buttons:
    btn = tk.Button(active_button_frame, text=text, command=command)
    btn.pack(pady=10, padx=20, fill='x')  # Reduced vertical padding

back_btn = tk.Button(active_button_frame, text="Back", command=back_main_pg)
back_btn.pack(pady=60, padx=20, fill='x')

# Truck Repairs Frame
truck_frame = tk.Frame(root)

# Create the truck_frame title label
truck_title = tk.Label(truck_frame, text="Truck with plate number "+plate_no, font=("Helvetica", 16))
truck_title.pack(pady=20)  

# Create a frame for truck_frame buttons
truck_button_frame = tk.Frame(truck_frame)
truck_button_frame.pack(expand=True)

# Create truck_frame buttons and assign actions
truck_buttons = [
    ("Show current details", lambda: show_database(status='location', plate_no=plate_no if plate_no else None, body_no=body_no if body_no else None)),
    ("Show all repairs", lambda: show_database(plate_no=plate_no if plate_no else None, body_no=body_no if body_no else None)),
    ("Show repairs in a time frame", move_to_time_frame_pg),
    ("Change Status or Location", move_to_update_truck_pg)
]

for text, command in truck_buttons:
    btn = tk.Button(truck_button_frame, text=text, command=command)
    btn.pack(pady=10, padx=20, fill='x')  # Reduced vertical padding

back_btn = tk.Button(truck_button_frame, text="Back", command=back_main_pg)
back_btn.pack(pady=60, padx=20, fill='x')

# Entry frame
entry_frame = tk.Frame(root)  

# Stack frames on top of each other
for frame in (main_frame, active_frame, entry_frame, truck_frame):
    frame.grid(row=0, column=0, sticky='nsew')

# Configure grid weights
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Show main frame when app starts
show_frame(main_frame)

# Run the application
root.mainloop()
