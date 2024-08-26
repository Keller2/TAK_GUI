import subprocess
import json
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
import csv
import time

with open('Support_files/config.json', 'r') as file:
    settings_data = json.load(file)

def deadend():
    print('dead end method')
    
def restart_method():
    try:
        subprocess.run(['sudo', 'systemctl', 'restart', 'takserver'])
    except Exception as e:
        print(f"error: {e}")

def example_clear_method():
    #dep method
    main_container.forget()
    information = ttk.Frame(master=gui)
    information.pack()
    #Update 2 lines above
    
def show_new_user_menu():
    clear_frame(main_container)
    new_user_menu = ttk.Frame(master=gui)
    new_user_menu.pack()
    title2 = ttk.Label(master=new_user_menu, text='New User', font='Calibri 16 bold')
    title2.pack(pady=2)
    input = ttk.Button(master = new_user_menu, text = 'Manual Entry', command=lambda: show_new_user_manual_entry(new_user_menu))
    from_file = ttk.Button(master = new_user_menu, text = 'Create from file', command = new_user_from_file)
    input.pack(pady=5)
    from_file.pack(pady=5)
    back_button = ttk.Button(master=new_user_menu, text='Back', command=lambda: show_main_frame(new_user_menu))
    back_button.pack(pady=5)
    
    #filename = askopenfilename()
    
def show_new_user_manual_entry(prior_frame=None):
    clear_frame(prior_frame)
    new_user_manual = ttk.Frame(master=gui)
    new_user_manual.pack()
    title2 = ttk.Label(master=new_user_manual, text='Manual Entry', font='Calibri 16 bold')
    title2.pack(pady=2)

    username_input = ttk.Entry(master=new_user_manual, textvariable=username_str)
    username = ttk.Label(master=new_user_manual, text='Username', font='Calibri 12 bold')
    username.pack(pady=2)
    username_input.pack(pady=2)

    team_input = ttk.Entry(master=new_user_manual, textvariable=team_str)
    team_name = ttk.Label(master=new_user_manual, text='Team', font='Calibri 12 bold')
    team_name.pack(pady=2)
    team_input.pack(pady=2)
    team_input.focus_force()
    
    # Create a frame for the buttons to be placed side by side
    button_frame = ttk.Frame(master=new_user_manual)
    button_frame.pack(pady=1)
    
    Create_ITAK = ttk.Button(master=button_frame, text='ITAK', command=ITAK_Package)
    Create_ITAK.pack(side='right', padx=5)
    Create_ATAK = ttk.Button(master=button_frame, text='ATAK', command=ATAK_Package)
    Create_ATAK.pack(side='left', padx=5)
    Create_Certs = ttk.Button(master=button_frame, text='WinTAK', command = WinTAK_Package)
    Create_Certs.pack(side='left', padx=5)

    back_button = ttk.Button(master=new_user_manual, text='Back', command=lambda: show_main_frame(new_user_manual))
    back_button.pack(pady=5)
    username_input.focus_set()

    
    
def new_user_from_file():
    filename = askopenfilename()
    if len(filename) < 1:
        
        return
    with open(filename, mode='r') as file:
        reader = csv.reader(file, delimiter=",")
        next(reader)
        for row in reader:
            i: int
            i = 0
            newUserName = ""
            deviceType = ""
            for element in row:

                if i == 0:
                        part1 = element
                elif i == 1:
                        part2 = element
                        newUserName = part1 + "-" + part2[0]
                elif i == 2:
                        deviceType = element
                elif i == 3:
                        userTeam = element  
                i+=1       
            print(newUserName)  
            if(deviceType == "IOS"):
                ITAK_Package(newUserName, userTeam)
                time.sleep(25)            
            elif(deviceType == "Android"):
                ATAK_Package(newUserName, userTeam)
                time.sleep(25)
            elif(deviceType == "WinTAK"):
                WinTAK_Package(newUserName, userTeam)
                time.sleep(25)
            else:
                print("ERROR Device Type Not Specified")
    
def delete_user_menu(prior_frame=None):
    clear_frame(main_container)
    delete_user_manual = ttk.Frame(master=gui)
    delete_user_manual.pack()
    title2 = ttk.Label(master = delete_user_manual, text='Delete User', font='Calibri 16 bold')
    title2.pack(pady=4)

    username_input = ttk.Entry(master = delete_user_manual, textvariable = delete_username_str)
    username_input.pack(pady=4)
    
    Delete_User = ttk.Button(master=delete_user_manual, text='Revoke & Delete', command = Delete_Package)
    Delete_User.pack(pady=4)
    back_button = ttk.Button(master=delete_user_manual, text='Back', command=lambda: show_main_frame(delete_user_manual))
    back_button.pack(pady=5)
    username_input.focus_set()
    
def Delete_Package():
    try:
        subprocess.run(['sh', 'Support_files/delete.sh', settings_data['username'], delete_username_str.get()])
    except Exception as e:
        messagebox.showwarning("Warning", "{e}")
        exit()
        #print(f"error: {e}")
           
def ITAK_Package(username=None, team=None):
    if username is None and team is None:
        try:
            subprocess.run(['sh', 'Support_files/itak.sh', settings_data['username'], username_str.get(), team_str.get()])
        except Exception as e:
            (f"error: {e}")
    else:
        try:
            subprocess.run(['sh', 'Support_files/itak.sh', settings_data['username'], username, team])
        except Exception as e:
            print(f"error: {e}")
            
def WinTAK_Package(username=None, team=None):
    if username is None and team is None:
        try:
            subprocess.run(['sh', 'Support_files/cert.sh', settings_data['username'], username_str.get(), team_str.get()])
        except Exception as e:
            (f"error: {e}")
    else:
        try:
            subprocess.run(['sh', 'Support_files/cert.sh', settings_data['username'], username, team])
        except Exception as e:
            print(f"error: {e}")
        
def ATAK_Package():
    user=username_str.get()
    team=team_str.get()

    f1 = open('Support_files/cfg_reference.txt', 'r')
    f2 = open('Support_files/config.pref', 'w')
    for line in f1:
        words = line.strip()
        print(words)
        if words =='<entry key="locationCallsign" class="class java.lang.String">CALLSIGN</entry>':
            f2.write('    <entry key="locationCallsign" class="class java.lang.String">'+ user +'</entry>\n')
        elif words == '<entry key="locationTeam" class="class java.lang.String">TEAM</entry>':
            f2.write('    <entry key="locationTeam" class="class java.lang.String">'+ team +'</entry>\n')
        else:
            f2.write(line)
            
    f1.close()
    f2.close()
    
    try:
        subprocess.run(['sh', 'Support_files/atak.sh', settings_data['username'], username_str.get(), team_str.get()])
    except Exception as e:
        print(f"error: {e}")
        
def ATAK_Package(username = None, team2= None):
    if username is None or team2 is None:
        f1 = open('Support_files/cfg_reference.txt', 'r')
        f2 = open('Support_files/config.pref', 'w')
        for line in f1:
            words = line.strip()
            #print(words) #Debug
            if words =='<entry key="locationCallsign" class="class java.lang.String">CALLSIGN</entry>':
                f2.write('    <entry key="locationCallsign" class="class java.lang.String">'+ username_str.get() +'</entry>\n')
            elif words == '<entry key="locationTeam" class="class java.lang.String">TEAM</entry>':
                f2.write('    <entry key="locationTeam" class="class java.lang.String">'+ team_str.get() +'</entry>\n')
            else:
                f2.write(line)
                
        f1.close()
        f2.close()
        try:
            subprocess.run(['sh', 'Support_files/atak.sh', settings_data['username'], username_str.get(), team_str.get()])
        except Exception as e:
            print(f"error: {e}")
    else:
        f1 = open('Support_files/cfg_reference.txt', 'r')
        f2 = open('Support_files/config.pref', 'w')
        for line in f1:
            words = line.strip()
            #print(words) #Debug
            if words =='<entry key="locationCallsign" class="class java.lang.String">CALLSIGN</entry>':
                f2.write('    <entry key="locationCallsign" class="class java.lang.String">'+ username +'</entry>\n')
            elif words == '<entry key="locationTeam" class="class java.lang.String">TEAM</entry>':
                f2.write('    <entry key="locationTeam" class="class java.lang.String">'+ team2 +'</entry>\n')
            else:
                f2.write(line)
                
        f1.close()
        f2.close()
        try:
            subprocess.run(['sh', 'Support_files/atak.sh', settings_data['username'], username, team2])
        except subprocess.CalledProcessError as e:
            messagebox.showwarning("Warning", "{e}")
            exit()
        except FileNotFoundError as e:
            print(f"Command failed: {e}")
    
    
def show_information():
    main_container.forget()
    information = ttk.Frame(master=gui)
    title2 = ttk.Label(master=information, text='Use Disclamer', font='Calibri 16 bold')
    title2.pack()
    disclaimer = ttk.Label(master=information, text='The TAK capability suite is a United States Government (USG) owned product. Use of these USG owned products outside of test and evaluation require the proper authority to operate (ATO) paperwork granted by your organization’s headquarters (HQ). Before installing and/or using any of the products, ensure you are within the guidelines of your organization.', font='Calibri 8', wraplength=300, justify="center")
    tak_admin_portal_disclaimer = ttk.Label(master=information, text='The TAK Admin GUI is a 3rd Party software that uses built in scripts that are native to TAK. Please ensure you understand the code running within the program before use. TAK Admin GUI is not authorised for critical TAK setups.', font='Calibri 8', wraplength=300, justify="center")
    disclaimer.pack()
    tak_admin_portal_disclaimer.pack()
    back_button = ttk.Button(master=information, text='Back', command=lambda: show_main_frame(information))
    back_button.pack(pady=5)
    information.pack()
    
def show_settings():
    try:
        subprocess.run(['nano', 'Support_files/config.json'])
    except Exception as e:
        
        print(f"error: {e}")
    
    

def show_main_frame(current_frame=None):
    if current_frame:
        current_frame.pack_forget()
    main_container.pack()
    
def clear_frame(current_frame=None):
    if current_frame:
        current_frame.pack_forget()

# Creating window
gui = tk.Tk()
gui.title('Tak Admin GUI')
gui.geometry('400x230')

username_str = tk.StringVar()
team_str = tk.StringVar()
delete_username_str = tk.StringVar()

# Main container
main_container = ttk.Frame(master=gui)
main_container.pack()

# Main title
main_menu = ttk.Label(master = main_container, text = 'TAK Admin Portal', font = 'Calibri 20 bold')
main_menu.pack()
title_options = ttk.Frame(master = main_container)
create_users = ttk.Button(master = title_options, text = 'Create Users', command = show_new_user_menu)
remove_users = ttk.Button(master = title_options, text = 'Delete Users', command = delete_user_menu)
restart_tak = ttk.Button(master = title_options, text = 'Restart Tak Program', command = restart_method)
about = ttk.Button(master = title_options, text = 'Disclaimer', command = show_information)
settings = ttk.Button(master = title_options, text = 'Settings', command = show_settings)
create_users.pack(pady=5)
remove_users.pack(pady=5)
restart_tak.pack(pady=5)
about.pack(pady=5)
settings.pack(pady=5)
title_options.pack()

if settings_data['display_warning_on_start'] == "true":
    messagebox.showwarning("Warning", "Please set up the GUI in settings before use!")


#Run
gui.mainloop() 