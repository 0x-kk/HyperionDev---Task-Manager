# This program is a task management system that allows users to log in and view all tasks, view their assigned tasks, and register
# new users. If the user is an admin, they also have the option to add a new task and view statistics for the number of registered
# users and number of tasks. The program reads user and task information from 'user.txt' and 'tasks.txt' files, respectively. 
# The program also includes a login system to ensure only authorized users have access to the task management system.

# ==============================================================================================================================

# The code below defines all necessary functions and checks if the entered username and password match a valid combination in the user.txt file. 
# If a match is found, it logs the user in. If not, it prompts the user to enter their credentials again until a match is found 
# or the user quits.

import datetime

def login():
    while True:
        entered_username = input("Enter your username: ")
        entered_password = input("Enter your password: ")

        with open('user.txt', 'r') as f:
            contents = f.read()

        lines = contents.split('\n')
        login_successful = False
        is_admin = False

        for line in lines:
            if ',' in line:
                username, password = line.split(',', maxsplit=1)
                username = username.strip()
                password = password.strip()
                if entered_username == username and entered_password == password:
                    login_successful = True
                    is_admin = (username == 'admin')
                    break
        if login_successful:
            print("\nLogin successful!")
            logged_in_user = entered_username
            return login_successful, is_admin, username
        else:
            print("\nLogin unsuccessful. Please try again.")

login_successful, is_admin, logged_in_user = login()

# This function reads the contents of the user.txt and tasks.txt files and prints a statement saying how many users and tasks there are.
def print_statistics():
    # Count the number of registered users
    with open('user.txt', 'r') as f:
        contents = f.read()
        users = contents.split("\n")
        num_users = 0
    for user in users:
        if ',' in user:
            num_users += 1
    # Count the number of tasks
    with open('tasks.txt', 'r') as f:
        contents = f.read()
        tasks = contents.split("\n")
        num_tasks = 0
        for task in tasks:
            if ',' in task:
                num_tasks += 1
    # Print the statistics
    print(f"\nThere are currently {num_users} registered users and {num_tasks} tasks assigned.")
    return

# This function allows the admin to register new users. It writes the login details to users.txt 
def register_user(username):
    if username == 'admin':
        new_user = input("Enter a new username: ")
        password = input("Enter a new password: ")
        while True:
            password_confirmation = input("Confirm password: ")
            if password == password_confirmation:
                break
        with open('user.txt', 'a') as file:
            file.write(f'\n{new_user}, {password}\n')
            print("\nNew user added successfully!")
    else:
        print("You do not have permission to register new users.")

# This function allows the admin to assign tasks to users. It checks if username is found in user.txt and if so, adds tasks details to tasks.txt
def add_task(username):
    if username == 'admin':
        assigned_to = input("\nEnter username of person task is assigned to: ")
        with open('user.txt', 'r') as f:
            contents = f.read()
            users = contents.split("\n")
            found = False
            for user in users:
                if ',' in user:
                    username, password = user.split(',', maxsplit=1)
                    username = username.strip()
                    password = password.strip()
                    if assigned_to == username:
                        found = True
                        break
            if found:
                title = input("Enter task name: ")
                description = input("Enter task description: ")
                due_date = input("Enter task due date: ")
                current_date = datetime.datetime.now().strftime('%d/%m/%Y')
                with open('tasks.txt', 'a') as file:
                    file.write(f"{assigned_to}, {title}, {description}, {current_date}, {due_date}, No\n")
                    print("\nTask added successfully!")
            else:
                print(f"\nUser '{assigned_to}' does not exist.")
    else:
        print("You do not have permission to add tasks.")

# This function prints the contents of tasks.txt in an organised way, allowing the user to see all existing tasks
def view_all_tasks():
    with open('tasks.txt', 'r') as tasks_read:
        data = tasks_read.readlines()
        for pos, line in enumerate(data, 1):
            split_data = line.split(', ')
            output = f'──────[{pos}]──────\n'
            output += '\n'
            output += f'Assigned to: \t\t{split_data[0]}\n'
            output += f'Task: \t\t\t{split_data[1]}\n'
            output += f'Description: \t\t{split_data[2]}\n'
            output += f'Assigned Date: \t\t{split_data[3]}\n'
            output += f'Due Date: \t\t{split_data[4]}\n'
            output += f'Is completed: \t\t{split_data[5]}\n'
            output += '\n'
            output += '────────────\n'

            print(output)

# This function prints tasks assigned only to the currently logged in user
def view_my_tasks(logged_in_user):
    with open('tasks.txt', 'r') as tasks_read:
        data = tasks_read.readlines()
        my_tasks = []
        for line in data:
            if line.startswith(logged_in_user + ', '):
                my_tasks.append(line)

        if my_tasks:
            for pos, line in enumerate(my_tasks, 1):
                split_data = line.split(', ')
                output = f'──────[{pos}]──────\n'
                output += '\n'
                output += f'Assigned to: \t\t{split_data[0]}\n'
                output += f'Task: \t\t\t{split_data[1]}\n'
                output += f'Description: \t\t{split_data[2]}\n'
                output += f'Assigned Date: \t\t{split_data[3]}\n'
                output += f'Due Date: \t\t{split_data[4]}\n'
                output += f'Is completed: \t\t{split_data[5]}\n'
                output += '\n'
                output += '────────────\n'
                print(output)
        else:
            print("\nYou have no tasks.")


# This part of the code shows the user two different menus and options depending on whether the logged in user is the admin or not.
while True:
    print("\n╔══════════════════════════════════════╗")
    # Non-admin user options
    if not is_admin:
        print("║ Select one of the following options: ║")
        print("╠══════════════════════════════════════╣")
        print("║ va - View all tasks                  ║")
        print("║ vm - View my tasks                   ║")
        print("║ e - Exit                             ║")
        print("╚══════════════════════════════════════╝")
        menu = input(": ").lower()
    # Admin user options
    else:
        print("║ Select one of the following options: ║")
        print("╠══════════════════════════════════════╣")
        print("║ r - Registering a user               ║")
        print("║ a - Adding a task                    ║")
        print("║ s - View statistics                  ║")
        print("║ va - View all tasks                  ║")
        print("║ vm - View my tasks                   ║")
        print("║ e - Exit                             ║")
        print("╚══════════════════════════════════════╝")
        menu = input(": ").lower()

# The code that follows allows the selection of a particular menu item and calls the relevant function
    if menu == 's':
        if is_admin:
            print_statistics()

    if menu == 'r':
        if is_admin:
            register_user(logged_in_user)

    if menu == 'a':
        if is_admin:
            add_task(logged_in_user)

    if menu == 'va':
        view_all_tasks()

    if menu == 'vm':
        view_my_tasks(logged_in_user)

    if menu == 'e':
        print("\nGoodbye!")
        break

else:
    print("\nInvalid input. Please try again.") 
