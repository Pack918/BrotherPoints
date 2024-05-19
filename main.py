import tkinter as tk
from tkinter import messagebox, ttk

# Initialize current_user variable
current_user = None

# Function to authenticate user
def authenticate(username, password):
    if username == "admin" and password == "12345":
        return "admin"
    with open("user_accounts.txt", "r") as file:
        for line in file:
            stored_username, stored_password, _ = line.strip().split(",")
            if stored_username == username and stored_password == password:
                return stored_username
    return None

# Function to display account balance
def display_balance(username):
    with open("user_accounts.txt", "r") as file:
        for line in file:
            stored_username, _, balance = line.strip().split(",")
            if stored_username == username:
                return int(balance)

# Function to update user balance
def update_balance(username, points):
    updated_lines = []
    with open("user_accounts.txt", "r") as file:
        for line in file:
            stored_username, stored_password, balance = line.strip().split(",")
            if stored_username == username:
                balance = str(int(balance) + points)
            updated_lines.append(f"{stored_username},{stored_password},{balance}\n")
    
    with open("user_accounts.txt", "w") as file:
        file.writelines(updated_lines)

    update_leaderboard()  # Update leaderboard after balance change

# Function to update leaderboard
def update_leaderboard():
    leaderboard_text.delete("1.0", tk.END)  # Clear current leaderboard
    with open("user_accounts.txt", "r") as file:
        accounts = [line.strip().split(",") for line in file if line.strip().split(",")[0] != "admin"]

    sorted_accounts = sorted(accounts, key=lambda x: int(x[2]), reverse=True)
    for i, account in enumerate(sorted_accounts):
        leaderboard_text.insert(tk.END, f"{i+1}. {account[0]}: {account[2]}\n")

# Function to logout
def logout():
    global current_user
    current_user = None
    admin_frame.pack_forget()

# Function to handle sending points
def send_points():
    recipient = recipient_var.get()
    points = int(transfer_entry.get())
    if points <= 0:
        messagebox.showerror("Error", "Please enter a positive number of points to transfer.")
        return
    if recipient == current_user:
        messagebox.showerror("Error", "You cannot transfer points to yourself.")
        return
    if recipient == "None":
        messagebox.showerror("Error", "Please select a recipient.")
        return
    if display_balance(current_user) < points:
        messagebox.showerror("Error", "Insufficient balance.")
        return
    update_balance(current_user, -points)
    update_balance(recipient, points)
    messagebox.showinfo("Success", f"{points} points successfully transferred to {recipient}.")
    balance_label.config(text=f"Balance: {display_balance(current_user)}")
    update_leaderboard()  # Refresh leaderboard after balance transfer

# Create main window
root = tk.Tk()
root.title("Fraternal Points Management System")

# Increase window size
root.geometry("400x300")

# Set background color to blue
root.configure(bg="#b3e0ff")

# Create login frame
login_frame = tk.Frame(root)
login_frame.pack()

# Create GUI components for login
tk.Label(login_frame, text="Leaderboard").pack()
leaderboard_text = tk.Text(login_frame, height=10, width=30)
leaderboard_text.pack()

# Update leaderboard initially
update_leaderboard()

tk.Label(login_frame, text="Username:").pack()
username_entry = tk.Entry(login_frame)
username_entry.pack()

tk.Label(login_frame, text="Password:").pack()
password_entry = tk.Entry(login_frame, show="*")
password_entry.pack()

# Function to handle login
def login():
    global current_user
    current_user = authenticate(username_entry.get(), password_entry.get())
    if current_user:
        if current_user == "admin":
            admin_frame.pack()  # Show admin frame
            update_user_list()
        else:
            user_frame.pack()  # Show user frame
            username_label.config(text=current_user)
            balance_label.config(text=f"Balance: {display_balance(current_user)}")
            create_recipient_list()
    else:
        messagebox.showerror("Error", "Invalid username or password")

# Allow pressing Enter key to login
root.bind("<Return>", lambda event: login())

login_button = tk.Button(login_frame, text="Login", command=login)
login_button.pack()

# Create admin frame
admin_frame = tk.Frame(root)

# Create GUI components for admin frame
admin_label = tk.Label(admin_frame, text="Admin Panel", font=("Helvetica", 16))
admin_label.pack()

user_list_label = tk.Label(admin_frame, text="Select User:")
user_list_label.pack()

user_list_var = tk.StringVar(admin_frame)
user_list = tk.Listbox(admin_frame, selectmode="single", listvariable=user_list_var, height=10, width=30)
user_list.pack()

selected_user_var = tk.StringVar(admin_frame)
selected_user_var.set("None")

points_label = tk.Label(admin_frame, text="Points:")
points_label.pack()
points_var = tk.Entry(admin_frame)
points_var.pack()

# Function to handle adding or removing points for admin
def admin_action(action):
    if action == "Add":
        points = int(points_var.get())
    elif action == "Remove":
        points = -int(points_var.get())

    selected_username = user_list.get(user_list.curselection())
    update_balance(selected_username, points)
    messagebox.showinfo("Success", f"{points} points {'added to' if action=='Add' else 'removed from'} {selected_username} successfully!")
    update_user_list()

admin_buttons_frame = tk.Frame(admin_frame)
admin_buttons_frame.pack()

add_button = tk.Button(admin_buttons_frame, text="Add", command=lambda: admin_action("Add"))
add_button.pack(side="left")

remove_button = tk.Button(admin_buttons_frame, text="Remove", command=lambda: admin_action("Remove"))
remove_button.pack(side="left")

logout_button = tk.Button(admin_frame, text="Logout", command=logout)
logout_button.pack()

# Create user frame
user_frame = tk.Frame(root)

# Create GUI components for user frame
username_label = tk.Label(user_frame, text="")
username_label.pack()

balance_label = tk.Label(user_frame, text="")
balance_label.pack()

transfer_frame = tk.Frame(user_frame)
transfer_frame.pack()

recipient_label = tk.Label(transfer_frame, text="Recipient:")
recipient_label.pack(side="left")

recipient_var = tk.StringVar(user_frame)
recipient_var.set("None")

# Retrieve list of recipients excluding "admin"
recipients = [line.strip().split(",")[0] for line in open("user_accounts.txt", "r") if line.strip().split(",")[0] != "admin"]

recipient_list = ttk.Combobox(transfer_frame, textvariable=recipient_var, values=recipients, width=10)
recipient_list.pack(side="left")

transfer_label = tk.Label(transfer_frame, text="Points:")
transfer_label.pack(side="left")

transfer_entry = tk.Entry(transfer_frame, width=10)
transfer_entry.pack(side="left")

transfer_button = tk.Button(transfer_frame, text="Transfer", command=send_points)
transfer_button.pack(side="left")

# Function to update user list for admin
def update_user_list():
    user_list.delete(0, tk.END)
    with open("user_accounts.txt", "r") as file:
        users = [line.strip().split(",")[0] for line in file if line.strip().split(",")[0] != "admin"]
    for user in users:
        user_list.insert(tk.END, user)

# Function to create recipient list for user
def create_recipient_list():
    recipient_list['values'] = ["None"] + [line.strip().split(",")[0] for line in open("user_accounts.txt", "r") if line.strip().split(",")[0] != current_user]

# Run the GUI
root.mainloop()
