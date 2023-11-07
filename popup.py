# Data collection popup
# Need to add submission and connection to table storage

import tkinter as tk
from tkinter import simpledialog

def collect_user_info():
    root = tk.Tk()
    root.title("User Information Collection")

    # Canvas Instructions
    instructions_text = """
    Steps for accessing Canvas API:
    1) In Canvas, go to Account -> Settings.
    2) Scroll down to 'Approved Integrations'.
    3) Click 'New Access Token' and create a name and expiration date.
    """
    canvas_instructions = tk.Label(root, text=instructions_text)
    canvas_instructions.pack()

    # Canvas Information
    canvas_label = tk.Label(root, text="Canvas Information:")
    canvas_label.pack()

    canvas_username_label = tk.Label(root, text="Canvas Username:")
    canvas_username_label.pack()
    canvas_username_entry = tk.Entry(root)
    canvas_username_entry.pack()

    canvas_password_label = tk.Label(root, text="Canvas Password:")
    canvas_password_label.pack()
    canvas_password_entry = tk.Entry(root, show="*") # standard practice to hide pw
    canvas_password_entry.pack()

    # Google Calendar Information
    google_label = tk.Label(root, text="Google Calendar Information:")
    google_label.pack()

    google_client_id_label = tk.Label(root, text="Client ID:")
    google_client_id_label.pack()
    google_client_id_entry = tk.Entry(root)
    google_client_id_entry.pack()

    google_client_secret_label = tk.Label(root, text="Client Secret:")
    google_client_secret_label.pack()
    google_client_secret_entry = tk.Entry(root)
    google_client_secret_entry.pack()

    google_redirect_uri_label = tk.Label(root, text="Redirect URI:")
    google_redirect_uri_label.pack()
    google_redirect_uri_entry = tk.Entry(root)
    google_redirect_uri_entry.pack()

    # Store the collected information in variables or take further actions as needed

    root.mainloop()

if __name__ == "__main__":
    collect_user_info()
