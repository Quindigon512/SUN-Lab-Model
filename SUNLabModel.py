#######################################################
# Author:   Quinn Trate
# Class:    CMPSC 487w Software Engineering
# Date:     September 13, 2023
# Language: Python
# Database: Google Firebase
# Purpose:  Models the SUN Lab with Card Swipes
#           and Allows Admins to View Logs and
#           Activate/Deactivate Accounts
#######################################################

import firebase_admin
from firebase_admin import db, credentials, initialize_app
import customtkinter
from customtkinter import *
from datetime import datetime

# Authenticate Firebase
cred = credentials.Certificate('credentials.json')
firebase_admin.initialize_app(cred, {'databaseURL': 'https://sun-lab-history-default-rtdb.firebaseio.com/'})

# Reference to Root Node
ref = db.reference("/")

# Global Variables
currentID = ""
currentName = ""
currentStatus = ""
currentType = ""

# Command for Submit Button for Logging In
def enter():
    global currentID, currentName, currentStatus, currentType
    entryID = txtEntry.get()
    userRef = db.reference('Users')
    userData = userRef.get()
    if userData and entryID in userData:# and userData[ID]['ID'] == ID:
        currentID = entryID
        currentName = userData[entryID]['name']
        currentStatus = userData[entryID]['status']
        currentType = userData[entryID]['type']
        loginFrame.pack_forget()
        if currentType == 'Admin':
            welcomeAdminFrame.pack(pady = 20, padx = 60, fill = "both", expand = True)
        else:
            welcomeFrame.pack(pady = 20, padx = 60, fill = "both", expand = True)
    else:
        print("Failed. ID is not in Database.")
        
# Command for Swiping In Button
def swipeIn():
    global currentID, currentStatus
    swipeCode = txtWelcome.get()
    txtWelcome.delete('0', END)
    if currentStatus == 'Active':
        if currentID and swipeCode == f"%A{currentID}":
            accessRef = db.reference('Access')
            accessRef.push({
                'ID': currentID,
                'inout': 'In',
                'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            print("Added a 'Swipe In' Entry to Database")
        else:
            print("Error. Please Swipe Again.")
    else:
        print("Error. User Account is Deactivated.")
  
# Command for Swiping Out Button
def swipeOut():
    global currentID, currentStatus
    swipeCode = txtWelcome.get()
    txtWelcome.delete('0', END)
    if currentStatus == 'Active':
        if currentID and swipeCode == f"%A{currentID}":
            accessRef = db.reference('Access')
            accessRef.push({
                'ID': currentID,
                'inout': 'Out',
                'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            print("Added a 'Swipe Out' Entry to Database")
        else:
            print("Error. Please Swipe Again.")
    else:
        print("Error. User Account is Deactivated.")
    
# Command for Swiping In Admin Button
def swipeAdminIn():
    global currentID, currentName, currentStatus, currentType
    swipeCode = txtWelcomeAdmin.get()
    txtWelcomeAdmin.delete('0', END)
    if currentStatus != 'Deactivated':
        if currentID and swipeCode == f"%A{currentID}":
            accessRef = db.reference('Access')
            accessRef.push({
                'ID': currentID,
                'inout': 'In',
                'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            print("Added a 'Swipe In' Entry to Database")
        else:
            print("Error. Please Swipe Again.")
    else:
        print("Error. User Account is Deactivated.")
   
# Command for Swiping In Admin Button
def swipeAdminOut():
    global currentID, currentName, currentStatus, currentType
    swipeCode = txtWelcomeAdmin.get()
    txtWelcomeAdmin.delete('0', END)
    if currentStatus != 'Deactivated':
        if currentID and swipeCode == f"%A{currentID}":
            accessRef = db.reference('Access')
            accessRef.push({
                'ID': currentID,
                'inout': 'Out',
                'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            print("Added a 'Swipe Out' Entry to Database")
        else:
            print("Error. Please Swipe Again.")
    else:
        print("Error. User Account is Deactivated.")
    
# Command for Leaving Welcome Portal
def switchUser():
    #currentID = None
    #currentName = None
    #currentStatus = None
    #currentType = None
    welcomeFrame.pack_forget()
    loginFrame.pack(pady = 20, padx = 60, fill = "both", expand = True)
    txtEntry.delete('0', END)
   
# Command for Leaving Admin Welcome Portal
def switchAdmin():
    currentID = None
    currentName = None
    currentStatus = None
    currentType = None
    welcomeAdminFrame.pack_forget()
    loginFrame.pack(pady = 20, padx = 60, fill = "both", expand = True)
    txtEntry.delete('0', END)
  
# Command for Displaying Users
def manageUsers():
    welcomeAdminFrame.pack_forget()
    manageFrame.pack(pady = 20, padx = 60, fill = "both", expand = True)
    userRef = db.reference('Users')
    userData = userRef.get()
    if userData:
        for userID, userInfo in userData.items():
            name = userInfo.get('name', '')
            status = userInfo.get('status', '')
            txtManage.insert(END, f"ID:  {userID} \t\tName:  {name} \t\t\t\tStatus:  {status}")
            txtManage.insert(END, "\n\n")
            btnStatus = customtkinter.CTkButton(master = manageFrame, text = f"Change Status for {name}", command = lambda id = userID: toggleStatus(id))
            btnStatus.pack(pady = 12, padx = 10)
   
# Command for Managing Users (Activating and Reactivating Accounts)
def toggleStatus(userID):
    userRef = db.reference(f'Users/{userID}')
    userInfo = userRef.get()
    currentStatus = userInfo.get('status', '')
    userRef.update({'status': 'Active' if currentStatus == 'Deactivated' else 'Deactivated'})
    txtManage.delete(1.0, END)
    manageFrame.pack_forget()
    manageUsers()
    
# Command for Back Button on Manage Users Screen
def manageBack():
    manageFrame.pack_forget()
    welcomeAdminFrame.pack(pady = 20, padx = 60, fill = "both", expand = True)

# Command for Viewing the Log of Swipes 
def viewLogs():
    welcomeAdminFrame.pack_forget()
    logFrame.pack(pady = 20, padx = 60, fill = "both", expand = True)
    accessRef = db.reference('Access')
    accessData = accessRef.get()
    if accessData:
        for accessId, accessInfo in accessData.items():
            userID = accessInfo.get('ID', ' ')
            inout = accessInfo.get('inout', ' ')
            timestamp = accessInfo.get('time', ' ')
            txtLogs.insert(END, f"ID:   {userID} \t\tIn/Out:  {inout} \t\tTimestamp:   {timestamp}")
            txtLogs.insert(END, "\n")
  
# Command for Applying the Filters
def applyFilter():
    accessRef = db.reference('Access')
    accessData = accessRef.get()
    if accessData:
        txtLogs.delete(1.0, END)
        filterID = varID.get()
        filterDate = varDate.get()
        for accessID, accessInfo in accessData.items():
            userID = accessInfo.get('ID', '')
            inout = accessInfo.get('inout', '')
            timestamp = accessInfo.get('time', '')
            if filterID and userID != filterID:
                continue
            if filterDate and not timestamp.startswith(filterDate):
                continue
            txtLogs.insert(END, f"ID:   {userID} \t\tIn/Out:  {inout} \t\tTimestamp:   {timestamp}")
            txtLogs.insert(END, "\n")
  
# Command for Back Button on View Logs Screen
def logBack():
    logFrame.pack_forget()
    welcomeAdminFrame.pack(pady = 20, padx = 60, fill = "both", expand = True)
   
# Command for Close Button on the Login Screen
def close():
    root.destroy()


# Set Up for GUI
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")
root = customtkinter.CTk()
root.geometry("800x575")

# Login Screen
loginFrame = customtkinter.CTkFrame(master = root)
loginFrame.pack(pady = 20, padx = 60, fill = "both", expand = True)
lblLogin = customtkinter.CTkLabel(master = loginFrame, text = "Enter 9 Digit ID:")
lblLogin.pack(pady = 12, padx = 10)
txtEntry = customtkinter.CTkEntry(master = loginFrame)
txtEntry.pack(pady = 12, padx = 10)
btnSubmit = customtkinter.CTkButton(master = loginFrame, text = "Enter", command = enter)
btnSubmit.pack(pady = 12, padx = 10)
btnClose = customtkinter.CTkButton(master = loginFrame, text = "Close", command = close)
btnClose.pack(pady = 12, padx = 10)

# Welcome Screen
welcomeFrame = customtkinter.CTkFrame(master = root)
lblWelcome = customtkinter.CTkLabel(master = welcomeFrame, text = "Welcome to the Sun Lab! What would you like to do?")
lblWelcome.pack(pady = 12, padx = 10)
txtWelcome = customtkinter.CTkEntry(master = welcomeFrame)
txtWelcome.pack(pady = 12, padx = 10)
btnSwipeIn = customtkinter.CTkButton(master = welcomeFrame, text = "Swipe In", command = swipeIn)
btnSwipeIn.pack(pady = 12, padx = 10)
btnSwipeOut = customtkinter.CTkButton(master = welcomeFrame, text = "Swipe Out", command = swipeOut)
btnSwipeOut.pack(pady = 12, padx = 10)
btnSwitchUser = customtkinter.CTkButton(master = welcomeFrame, text = "Switch User", command = switchUser)
btnSwitchUser.pack(pady = 12, padx = 10)

# Welcome Screen for Admin
welcomeAdminFrame = customtkinter.CTkFrame(master = root)
lblWelcomeAdmin = customtkinter.CTkLabel(master = welcomeAdminFrame, text = "Welcome to the Sun Lab Backdoor. What would you like to do?")
lblWelcomeAdmin.pack(pady = 12, padx = 10)
txtWelcomeAdmin = customtkinter.CTkEntry(master = welcomeAdminFrame)
txtWelcomeAdmin.pack(pady = 12, padx = 10)
btnSwipeAdminIn = customtkinter.CTkButton(master = welcomeAdminFrame, text = "Swipe In", command = swipeAdminIn)
btnSwipeAdminIn.pack(pady = 12, padx = 10)
btnSwipeAdminOut = customtkinter.CTkButton(master = welcomeAdminFrame, text = "Swipe Out", command = swipeAdminOut)
btnSwipeAdminOut.pack(pady = 12, padx = 10)
btnSwitchAdmin = customtkinter.CTkButton(master = welcomeAdminFrame, text = "Switch User", command = switchAdmin)
btnSwitchAdmin.pack(pady = 12, padx = 10)
btnManageUsers = customtkinter.CTkButton(master = welcomeAdminFrame, text = "Manage Users", command = manageUsers)
btnManageUsers.pack(pady = 12, padx = 10)
btnViewLogs = customtkinter.CTkButton(master = welcomeAdminFrame, text = "View Logs", command = viewLogs)
btnViewLogs.pack(pady = 12, padx = 10)

# Manage Users Screen
manageFrame = customtkinter.CTkFrame(master = root)
lblManage = customtkinter.CTkLabel(master = manageFrame, text = "SUN Lab Logs")
lblManage.pack(pady = 12, padx = 10)
btnManageBack = customtkinter.CTkButton(master = manageFrame, text = "Back", command = manageBack)
btnManageBack.pack(pady = 12, padx = 10)
txtManage = customtkinter.CTkTextbox(master = manageFrame, wrap = WORD, width = 500, height = 160)
txtManage.pack()

# View Logs Screen
logFrame = customtkinter.CTkFrame(master = root)
lblLog = customtkinter.CTkLabel(master = logFrame, text = "SUN Lab Logs")
lblLog.pack(pady = 12, padx = 10)
btnLogBack = customtkinter.CTkButton(master = logFrame, text = "Back", command = logBack)
btnLogBack.pack(pady = 12, padx = 10)
txtLogs = customtkinter.CTkTextbox(master = logFrame, wrap = WORD, width = 500, height = 160)
txtLogs.pack()
lblFilterID = customtkinter.CTkLabel(master = logFrame, text="Filter by ID:")
lblFilterID.pack(pady = 12, padx = 10)
varID = StringVar()
txtFilterID = customtkinter.CTkEntry(master = logFrame, textvariable = varID)
txtFilterID.pack(pady = 12, padx = 10)
lblFilterDate = customtkinter.CTkLabel(master = logFrame, text = "Filter by Date (YYYY-MM-DD):")
lblFilterDate.pack(pady = 12, padx = 10)
varDate = StringVar()
txtFilterDate = customtkinter.CTkEntry(master = logFrame, textvariable = varDate)
txtFilterDate.pack(pady = 12, padx = 10)
btnFilter = customtkinter.CTkButton(master = logFrame, text = "Filter", command = applyFilter)
btnFilter.pack(pady = 12, padx = 10)

# Run GUI
root.mainloop()
