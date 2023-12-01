# -*- coding: utf-8 -*-
import json

# getpass and input are simple ways to get user input
import getpass

import requests
import pandas as pd
from builtins import input
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Static settings
# Using a base urls is useful for switching between test and production environments easily
BASE_URL = 'https://sju.instructure.com'
PER_PAGE = 100

# User input settings
# token should be treated as a password (not visible when typed)
token = '<YOUR INDIVIDUAL TOKEN>'
while not token:
    token = getpass.getpass('Enter your access token:')
auth_header = {'Authorization': 'Bearer ' + token} # setup the authorization header to be used later

# require the course state to be provided
course_state = 'available'
enrollment_state = 'active'
start_date = '2023-01-01T00:00:00Z'
#while not course_state in ['unpublished', 'available', 'completed', 'deleted']:
    #course_state = input("Select a course state [unpublished, available, completed, deleted]:")

# Your Google Calendar API setup
scopes = ['https://www.googleapis.com/auth/calendar']
flow = InstalledAppFlow.from_client_secrets_file('<secret token file name>', scopes=scopes)
credentials = flow.run_local_server(port=8080)
service = build('calendar', 'v3', credentials='<secret token file name>')

# Google Calendar ID (replace with your own calendar ID)
calendar_id = 'primary'

# Function to create a Google Calendar event
def create_event(service, calendar_id, summary, due_date):
    event = {
        'summary': summary,
        'description': 'Assignment Due',
        'start': {
            'dateTime': due_date.isoformat(),
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': (due_date + timedelta(hours=1)).isoformat(),
            'timeZone': 'UTC',
        },
    }


print("Finding courses...")
print("-----------------------------")
# continue to make requests until all data has been received
page = 1
courses = []
while True:
    # request urls should always be based of the base url so they do not
    # need to be changed when switching between test and production environments
    request_url = BASE_URL + '/api/v1/courses'
    params = {
        "per_page": str(PER_PAGE),
        "page": str(page),
        "enrollment_state[]": [enrollment_state],
        "state[]": [course_state],
        "include[]": ['total_students']
    }
    r = requests.get(request_url, headers=auth_header, params=params)

    # always take care to handle request errors
    r.raise_for_status() # raise error if 4xx or 5xx

    data = r.json()
    if len(data) == 0:
        break

    courses += data

    print("Finished processing page: "+str(page))
    page+=1

if len(courses) == 0:
    print("No courses found to report on.")
    exit()

# from here, a simple table is printed out
# using pandas for convenience
print("Report for "+str(len(courses)) + " courses.")
print("-----------------------------")

courses_df = pd.DataFrame(courses)
result = courses_df.to_string(
    columns=['id', 'name', 'course_code', 'workflow_state', 'start_at', 'end_at', 'total_students']
)
print(result)

# List to store assignments from specified courses
# List to store assignments from specified courses
assignments = []
count = 0

# Iterate over the filtered courses
for course in specific_course_ids:
    # Make a request to get assignments for the current course
    assignments_url = BASE_URL + f'/api/v1/courses/{specific_course_ids[count]}/assignments'
    assignments_params = {"per_page": str(PER_PAGE)}
    assignments_request = requests.get(assignments_url, headers=auth_header, params=assignments_params)
    assignments_request.raise_for_status()
    
    # Add assignments to the list
    assignments = assignments_request.json()
    
    # Print the assignments
    if assignments:
        assignments_df = pd.DataFrame(assignments)
        assignments_result = assignments_df.to_string(
            columns=['id', 'name', 'due_at', 'points_possible']
        )
        print(f"Assignments for {specific_course_ids[count]}:")
        print("-----------------------------")
        print(assignments_result)
        print("\n")
    else:
        print("No assignments found.")

    count = count + 1
