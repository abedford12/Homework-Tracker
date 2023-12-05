import tkinter as tk

import requests

from CanvasComms import Canvas


def collect_user_info():
    root = tk.Tk()
    root.title("User Information Collection")

    # Declare submit_button, reset_button, and submit as global vars
    global submit_button
    global reset_button
    global submit
    global crn_entries
    global calendar_pathway_entry  # New entry widget for Google Calendar Pathway


    submit_button = None  # Initialize submit_button
    reset_button = None  # Initialize reset_button
    submit = None  # Initialize submit
    crn_entries = []  # Initialize crn_entries as a global variable

    def update_crn_entries(*args):
        global submit_button  # Reference the global variable
        global reset_button  # Reference the global variable
        global submit  # Reference the global variable
        global crn_entries  # Reference the global variable
        num_courses = int(num_courses_var.get())

        # Clear previous CRN entry fields
        for entry in crn_entries:
            entry.destroy()

        # Create new CRN entry fields
        crn_entries.clear()
        for i in range(num_courses):
            crn_label = tk.Label(root, text=f"CRN for Course {i + 1}:")
            crn_label.pack()
            crn_entry = tk.Entry(root)
            crn_entry.pack()
            crn_entries.append(crn_entry)

        
        # Clear previous Google Calendar Pathway entry field
        calendar_pathway_entry.destroy()

        # Create new CRN entry fields
        crn_entries.clear()
        for i in range(num_courses):
            crn_label = tk.Label(root, text=f"CRN for Course {i + 1}:")
            crn_label.pack()
            crn_entry = tk.Entry(root)
            crn_entry.pack()
            crn_entries.append(crn_entry)

        # Create new Google Calendar Pathway entry field
        calendar_pathway_label = tk.Label(root, text="Google Calendar Pathway:")
        calendar_pathway_label.pack()
        calendar_pathway_entry = tk.Entry(root)
        calendar_pathway_entry.pack()

        # Create the submit button if it doesn't exist
        if submit_button is None:
            submit_button = tk.Button(root, text="Submit", command=submit, height=2, width=10, bg="green")

        # Create the reset button if it doesn't exist
        if reset_button is None:
            reset_button = tk.Button(root, text="Reset", command=reset, height=2, width=10, bg="red")

        # Hide the dropdown menu
        num_courses_dropdown.pack_forget()

        # Pack the reset button after the CRN entry fields
        reset_button.pack(side=tk.TOP, anchor=tk.CENTER, pady=5)

        # Pack the submit button after the CRN entry fields
        submit_button.pack(side=tk.TOP, anchor=tk.CENTER, pady=5)
        
    #TODO Add instructions for google pathway
    
    # Canvas Instructions text
    instructions_text = """
    Steps for accessing Canvas API:
    1) In Canvas, go to Account -> Settings.
    2) Scroll down to 'Approved Integrations'.
    3) Click 'New Access Token' and create a name and expiration date.
       Set the expiration date as the end of your semester.
    """
    canvas_instructions = tk.Label(root, text=instructions_text)
    canvas_instructions.pack()

    # Canvas Information
    canvas_token_label = tk.Label(root, text="Canvas Access Token:")
    canvas_token_label.pack()
    canvas_token_entry = tk.Entry(root)
    canvas_token_entry.pack()

    # Number of Courses Dropdown
    num_courses_label = tk.Label(root, text="Number of Courses:")
    num_courses_label.pack()

    # Create a variable to hold the selected number of courses
    num_courses_var = tk.StringVar(root)
    num_courses_var.set("1")  # Default value

    # Dropdown menu with options 1 through 8
    num_courses_dropdown = tk.OptionMenu(root, num_courses_var, *range(1, 9), command=update_crn_entries)
    num_courses_dropdown.pack()

    def submit():
        # Function to collect and process the submitted data
        # TODO: MOVE CRN AND TOKEN DATA TO BACKEND UPON SUBMISSION
        canvas_token = canvas_token_entry.get()
        num_courses = int(num_courses_var.get())
        crns = [entry.get() for entry in crn_entries]
        google_calendar_pathway = calendar_pathway_entry.get()
        root.destroy()  # Closes window upon entry

        # Code added to send collected data into our database
        # List of Urls in order to access APIS
        urlFindUser = "http://127.0.0.1:8000/users/CAT_retrieve/"
        urlCreateUser = "http://127.0.0.1:8000/users/create/{create_user}"
        urlCRNToDatabase = "http://127.0.0.1:8000/courses/create/{create_course}"

        # Adds Canvas token info into find user
        urlFindUser += canvas_token
        response = requests.get(urlFindUser)

        # After using a get, response.status_code=200 means a user with the canvas code exists
        if response.status_code == 200:
            userIDInfo = response.json()["user_uid"]
            for i in range(num_courses):
                courseCreate = {
                    "courseName": "None linked",
                    "profFName": "None linked",
                    "profLName": "None linked",
                    "crn": crns[i],
                    "uid": userIDInfo
                }
                requests.post(urlCRNToDatabase, json=courseCreate)

        # response.status_code == 404 means user doesn't exist so a user is created new
        if response.status_code == 404:
            userCreate = {
                "username": "None linked",
                "canvasAccessToken": canvas_token,
                "googleCalendarAccessToken": "None linked"}
            requests.post(urlCreateUser, json=userCreate)

            # Creates all courses and attatches them to their respective user
            response = requests.get(urlFindUser)
            userIDInfo = response.json()["user_uid"]
            for i in range(num_courses):
                courseCreate = {
                    "courseName": "None linked",
                    "profFName": "None linked",
                    "profLName": "None linked",
                    "crn": crns[i],
                    "uid": userIDInfo
                }
                requests.post(urlCRNToDatabase, json=courseCreate)

        # Perform actions with the collected data (e.g., store in a database)

        print("Canvas Token:", canvas_token)
        print("Number of Courses:", num_courses)
        print("CRNs:", crns)
        print("Google Calendar Pathway:", google_calendar_pathway)
        
        # Calls CanvasComms, bringing over the token that was submitted
        # Canvas(canvas_token)

    def reset():
        # Function to reset the page
        for widget in root.winfo_children():
            widget.pack_forget()

        # Re-add canvas_instructions, canvas_token_label, and canvas_token_entry
        canvas_instructions.pack()
        canvas_token_label.pack()
        canvas_token_entry.pack()

        # Show the dropdown menu
        num_courses_dropdown.pack()

    root.mainloop()


if __name__ == "__main__":
    collect_user_info()
