import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%d-%m-%Y"

class Task:
    def __init__(self, username = None, title = None, description = None, due_date = None, assigned_date = None, completed = None):
        '''
        Inputs:
        username: String
        title: String
        description: String
        due_date: DateTime
        assigned_date: DateTime
        completed: Boolean
        '''
        self.username = username
        self.title = title
        self.description = description
        self.due_date = due_date
        self.assigned_date = assigned_date
        self.completed = completed

    def from_string(self, task_str):
        '''
        Convert from string in tasks.txt to object
        '''
        tasks = task_str.split(", ")
        username = tasks[0]
        title = tasks[1]
        description = tasks[2]
        due_date = datetime.strptime(tasks[3], DATETIME_STRING_FORMAT)
        assigned_date = datetime.strptime(tasks[4], DATETIME_STRING_FORMAT)
        completed = True if tasks[5] == "Yes" else False
        self.__init__(username, title, description, due_date, assigned_date, completed)


    def to_string(self):
        '''
        Convert to string for storage in tasks.txt
        '''
        str_attrs = [
            self.username,
            self.title,
            self.description,
            self.due_date.strftime(DATETIME_STRING_FORMAT),
            self.assigned_date.strftime(DATETIME_STRING_FORMAT),
            "Yes" if self.completed else "No"
        ]
        return ", ".join(str_attrs)

    def display(self):
        '''
        Display object in readable format
        '''
        disp_str = f"Task: \t\t {self.title}\n"
        disp_str += f"Assigned to: \t {self.username}\n"
        disp_str += f"Date Assigned: \t {self.assigned_date.strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {self.due_date.strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {self.description}\n"
        return disp_str



# Read and parse tasks.txt
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]


task_list = []
for t_str in task_data:
    curr_t = Task()
    curr_t.from_string(t_str)
    task_list.append(curr_t)

# Read and parse user.txt

# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")
        

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

# Keep trying until a successful login
logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist. Please enter a valid username")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Incorrect password")
        continue
    else:
        print("Login Successful!")
        logged_in = True

#create function to verify whether date entered is in correct format
def verify_date(input_date):

    while True:
        try:
            valid_date = datetime.strptime(
                input_date, DATETIME_STRING_FORMAT)
            return valid_date
        except ValueError:
            input_date = input(
                "Incorrect date format. Please enter as DD-MM-YYYY: ")
            continue

#check whether entry contains characters that would break the program
def validate_string(input_str):
    
    if "," in input_str:
        print("Your input cannot contain a ',' character")
        return False
    return True

#check if username or password contain invalid characters
def check_username_and_password(username, password):

    if ";" in username or ";" in password:
        print("Username or password cannot contain ';'.")
        return False
    return True

#check if user is within the system
#if not, display error message
def verify_username(user_name):

    while user_name not in username_password.keys():
        user_name = input(
            print("User does not exist. Please enter a valid username"))
    return user_name

#write username and password to user.txt file as they are added
def write_usernames_to_file(username_dict):

    with open("user.txt", "w") as out_file:
        user_data = []
        for k in username_dict:
            user_data.append(f"{k};{username_dict[k]}")
        out_file.write("\n".join(user_data))
        out_file.close

#write tasks to tasks.txt file as they are added
def write_tasks_to_file():

    with open("tasks.txt", "w") as task_file:
        task_file.write("\n".join([t.to_string() for t in task_list]))
    task_file.close()

#function to check if user enters a valid task number
def check_task(num, min, max):
    
    while num < min or num > max:
        num = int(input("Invalid entry. Please choose another task: "))
    return num

#function to lookup specific tasks if the user wants to edit them
def lookup_task():
   
    task_description = [t.description for t in task_list]
    due_dates = [t.due_date for t in task_list]

    global due_date_dictionary
    due_date_dictionary = {}
    for i in range(len(due_dates)):
        due_date_dictionary[i] = due_dates[i]

    global description_dictionary
    description_dictionary = {}
    for i in range(len(task_description)):
        description_dictionary[i] = task_description[i]

    global description_lookup
    description_lookup = {}
    for i in range(len(task_description)):
        description_lookup[task_description[i]] = i

#function for adding new user
def new_user():

    if curr_user != 'admin':
        print("Error - Registering new users requires admin privileges")
        return
    username = input("New Username: ")

    while username in username_password.keys():
        username = input("This username is already in use. Please try another: ")

    password = input("New Password: ")

    if not check_username_and_password(username, password):
        return

    check_password = input("Confirm Password: ")

    if password != check_password:
        print("Passwords do not match.")
        return
        
    else:
        print("New user added!")

        username_password[username] = password
        write_usernames_to_file(username_password)
        return

#function for adding new task
def new_task():

    user_task = verify_username(input("Name of person assigned to task: "))

    while True:
        task_title = input("Title of Task: ")
        if validate_string(task_title):
            break

    while True:
        task_description = input("Description of Task: ")
        if validate_string(task_description):
            break



    task_due_date = verify_date(input("Due date of task (DD-MM-YYYY): "))
    curr_date = date.today()
    new_task = Task(user_task, task_title, task_description, task_due_date, curr_date, False)
    task_list.append(new_task)

    write_tasks_to_file()
    print("Task added successfully.")

#function to view all added tasks
def view_all_tasks():

    print("------------------------------------------")

    if len(task_list) == 0:
        print("There are no current tasks.")
        print("------------------------------------------")

    for t in task_list:
        print(t.display())
        print("------------------------------------------")

#function to view tasks of current user 
def view_mine():

    has_task = False

    lookup_task()
    for t in task_list:
        if t.username == curr_user:
            has_task = True
            print(f"Task Number: {description_lookup[t.description]}\n")
            print(t.display())
            print("------------------------------------------\n")

    if not has_task:
        print("You have no tasks.")
        print("------------------------------------------")
        return

    #give user choice if they want to edit task or return to menu    
    user_task_choice = check_task(int(input(
        "\nPlease enter the number of the task to edit, or enter -1 to return to main menu: ")), -1, len(task_list) - 1)

    if user_task_choice == -1:
        return

    else:
        for t in task_list:
            #not allow user to edit task that isn't assigned to them
            if t.username != curr_user and t.description == description_dictionary[user_task_choice] and t.due_date == due_date_dictionary[user_task_choice]:
                print("You may not edit a task that is not assigned to you.")
                return
        
        #ask user if they want to mark task as complete or edit tasks' username or due date
        edit_task = check_task(int(
            input(f"\nTo mark task {user_task_choice} complete, enter 1.\nTo edit task {user_task_choice}, enter 2: ")), 1, 2)


    if edit_task == 1:
        for t in task_list:
            if t.username == curr_user and t.description == description_dictionary[user_task_choice] and t.due_date == due_date_dictionary[user_task_choice]:
                setattr(t, 'completed', True)

    elif edit_task == 2:
        for t in task_list:
            if t.username == curr_user and t.description == description_dictionary[user_task_choice] and t.due_date == due_date_dictionary[user_task_choice]:
                
                #prevent user from editing a completed task
                if t.completed == True:
                    print("Sorry, you can't edit a completed task.")
                    return
                else:
                    edit_choice = check_task(int(input("Enter 1 to edit username. Enter 2 to edit due date. :")), 1, 2)
                    if edit_choice == 1:
                        new_name = verify_username(input(f"Enter new username for task {user_task_choice} :"))
                        setattr(t, 'username', new_name)
                        return
                    elif edit_choice == 2:
                        new_due_date = verify_date(input(f"Enter new due date of task {user_task_choice} (DD-MM-YYYY): "))
                        setattr(t, 'due_date', new_due_date)

    write_tasks_to_file()
    print("Task successfully edited.")

#function to generate a report of total tasks, tasks completed, incomplete, overdue and create external text file to add report to
def generate_task_report():

    complete_tasks = 0
    incomplete_tasks = 0
    tasks_overdue = 0

    for t in task_list:
        if t.completed == True:
            complete_tasks += 1
        else:
            incomplete_tasks += 1
        if t.completed == False and t.due_date < datetime.now():
            tasks_overdue += 1

    task_report_file = open("task_overview.txt", "w")
    task_report_file.write(f'''
-----------------------------------------
            TASK OVERVIEW
-----------------------------------------

Total Tasks:            {len(task_list)}
Completed Tasks:        {complete_tasks}
Uncompleted Tasks:      {incomplete_tasks}
Overdue Tasks:          {tasks_overdue}
Incomplete Task %:      {round(incomplete_tasks/len(task_list) * 100, 1)}%
Overdue Task %:         {round(tasks_overdue/len(task_list)* 100, 1)}%

-----------------------------------------''')
    task_report_file.close()

#function to generate user report text file
def generate_user_report():

    user_task_info = []
    for user in username_password.keys():

        user_tasks = 0
        tasks_complete = 0
        tasks_incomplete = 0
        overdue = 0

        for t in task_list:
            if t.username == user:
                user_tasks += 1
                if t.completed == True:
                    tasks_complete += 1
                else:
                    tasks_incomplete += 1
                if t.completed == False and t.due_date < datetime.now():
                    overdue += 1

        user_task_info.append([user, user_tasks,
                              tasks_complete, tasks_incomplete, overdue])

    user_report = f'''
-----------------------------------------
            USER OVERVIEW
-----------------------------------------

Registered Users:       {len(username_password.keys())}
Total Tasks:            {len(task_list)}

-----------------------------------------'''

    for i in range(len(username_password.keys())):
#calculations for tasks completed, incomplete and overdue
        user_data = f'''

User:                       {user_task_info[i][0]}
User Tasks:                 {user_task_info[i][1]}
Percentage of Total Tasks:  {round(user_task_info[i][1]/len(task_list) * 100, 1)}%
Complete Task Percentage:   {round(user_task_info[i][2]/user_task_info[i][1] * 100, 1) if user_task_info[i][1] else "-"}%
Incomplete Task Percentage: {round(user_task_info[i][3]/user_task_info[i][1] * 100, 1) if user_task_info[i][1] else "-"}%
Overdue Task Percentage:    {round(user_task_info[i][4]/user_task_info[i][1] * 100, 1) if user_task_info[i][1] else "-"}%

-----------------------------------------'''

        user_report += user_data

    user_report_file = open("user_overview.txt", "w")
    user_report_file.write(user_report)
    user_report_file.close()


#function to display user report and task overview in python display
def display_stats():

    task_report_file = open("task_overview.txt", 'r')
    user_report_file = open("user_overview.txt", 'r')
    print(task_report_file.read())
    print(user_report_file.read())
    task_report_file.close()
    user_report_file.close()


#########################
# Main Program
#########################


while True:
    # Get input from user
    print()
    if curr_user == 'admin':
        menu = input('''
------------------------------------------
Select one of the following options:
------------------------------------------
    r  -  Register a user
    a  -  Add a task
    va -  View all tasks
    vm -  View my tasks
    gr -  Generate reports
    ds -  Display statistics
    e  -  Exit
------------------------------------------
 : ''').lower()
    else:
        menu = input('''
------------------------------------------
Select one of the following options:
------------------------------------------
    r  -  Register a user
    a  -  Add a task
    va -  View all tasks
    vm -  View my tasks
    e  -  Exit
------------------------------------------
 : ''').lower()

    if menu == 'r':
        new_user()
        continue

    elif menu == 'a':
        new_task()
        continue

    elif menu == 'va':
        view_all_tasks()
        continue

    elif menu == 'vm':
        view_mine()
        continue

    elif menu == 'gr' and curr_user == 'admin':
        generate_task_report()
        generate_user_report()
        print("------------------------------------------\n")
        print("Report files created.\n")
        print("------------------------------------------")
        continue

    elif menu == 'ds' and curr_user == 'admin':
        display_stats()
        continue

    elif menu == 'e':
        print('Goodbye!')
        exit()

    else:  # Default case
        print("Not an available option, try again.")
