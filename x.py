# This program is a task management system that allows users to log in and view all tasks, view their assigned tasks, and register
# new users. If the user is an admin, they also have the option to add a new task and view statistics for the number of registered
# users and number of tasks. The program reads user and task information from 'user.txt' and 'tasks.txt' files, respectively. 
# The program also includes a login system to ensure only authorized users have access to the task management system.

# ==============================================================================================================================

# The code below checks if the entered username and password match a valid combination in the user.txt file. 
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

# This code counts the number of registered users and tasks in the program and prints them out as statistics for 
# the admin user to view.
    if menu == 's':
        if is_admin:
            print_statistics()

# This part of code registers a new user if the menu option selected is 'r' and the current user is 'admin'. 
# It prompts the user to enter a new username and password, and checks that the password is confirmed correctly before writing 
# the new user to the 'user.txt' file
    if menu == 'r':
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

# This code checks if the user is an admin. If the user is an admin, it allows the user to input a username to assign 
# a task to and input details for the task. It then checks if the assigned user exists and, if they do, it writes the task details
# to a file and prints a message indicating that the task was added successfully.
    elif menu == 'a':
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

# This code reads the contents of 'tasks.txt', iterates through each line, splits the line on the delimiter ', ' 
# and formats the resulting split data into a multi-line string. It then prints this formatted string.
    elif menu == 'va':
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

# This part of code reads the contents of 'tasks.txt' and displays the contents relevant to the currently logged in user.
    elif menu == 'vm':
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

    elif menu == 'e':
        print("\nGoodbye!")
        break

else:
    print("\nInvalid input. Please try again.") 