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


def Canvas(canvas_token, google_calendar_pathway):
    # Static settings
    # Using a base urls is useful for switching between test and production environments easily
    BASE_URL = 'https://sju.instructure.com'
    PER_PAGE = 100

    # Using the function call and the database we are able to pull all the information over
    tokenTest = canvas_token

    # path to api find user using canvas token
    urlFindUser = "http://127.0.0.1:8000/users/CAT_retrieve/"

    # Adds Canvas token info into find user
    urlFindUser += canvas_token
    response = requests.get(urlFindUser)
    userIDInfo = response.json()["user_uid"]

    # path to api list crns using a user id
    urlFindCRNS = "http://127.0.0.1:8000/courses/crn_list/{course_id}"

    # Add the userid to find the array of crns
    response = requests.get(url=urlFindCRNS, params={'user_id': userIDInfo})
    userCRNInfo = response.json()

    print(canvas_token)
    print(response)
    print(userIDInfo)
    print(userCRNInfo)

    # User input settings
    # token should be treated as a password (not visible when typed)
    token = '9605~UEXFdzx0ntDdmzvS48S5rPeQvQcTpUZAQoKVWDlOl44NhxCtKpyseQZ54myEUsE3'
    token = canvas_token
    while not token:
        token = getpass.getpass('Enter your access token:')
    auth_header = {'Authorization': 'Bearer ' + token}  # setup the authorization header to be used later

    # require the course state to be provided
    course_state = 'available'
    enrollment_state = 'active'
    start_date = '2023-01-01T00:00:00Z'

    # Your Google Calendar API setup
    json_key_path = '/Users/benutter/Downloads/client_secret_917639123664-80d60u1gg7dtacmba7k8d0p0f1p386ju.apps.googleusercontent.com.json'
    #json_key_path = 'C:\\Users\\woulv\\Downloads\\client_secret_499867656717-sii1um3p5eb9evc6pvlq5317l4diu02t.apps.googleusercontent.com.json'
    json_key_path = google_calendar_pathway
    scopes = ['https://www.googleapis.com/auth/calendar']
    flow = InstalledAppFlow.from_client_secrets_file(json_key_path, scopes=scopes)
    credentials = flow.run_local_server(port=8080)

    service = build('calendar', 'v3', credentials=credentials)

    # Google Calendar ID (replace with your own calendar ID)
    calendar_id = 'primary'

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
        r.raise_for_status()  # raise error if 4xx or 5xx

        data = r.json()
        if len(data) == 0:
            break

        courses += data

        print("Finished processing page: " + str(page))
        page += 1

    if len(courses) == 0:
        print("No courses found to report on.")
        exit()

    # from here, a simple table is printed out
    # using pandas for convenience
    print("Report for " + str(len(courses)) + " courses.")
    print("-----------------------------")

    courses_df = pd.DataFrame(courses)
    result = courses_df.to_string(
        columns=['id', 'name', 'course_code', 'workflow_state', 'start_at', 'end_at', 'total_students']
    )
    print(result)

    # List of specific course IDs you want to retrieve assignments from
    specific_course_ids = [37714, 37709, 37676, 36886, 37681]  # Replace these with your desired course IDs
    specific_course_ids = userCRNInfo
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
            for index, assignment in assignments_df.iterrows():
                assignment_name = assignment['name']
                due_date_str = assignment['due_at']

                if due_date_str:
                    # Convert due_date_str to a datetime object
                    due_date = datetime.strptime(due_date_str, '%Y-%m-%dT%H:%M:%SZ')

                    # Create an event in Google Calendar
                    event = {
                        'summary': assignment_name,
                        'description': f'Assignment due: {assignment_name}',
                        'start': {'dateTime': due_date.isoformat(), 'timeZone': 'UTC'},
                        'end': {'dateTime': (due_date + timedelta(hours=1)).isoformat(), 'timeZone': 'UTC'},
                    }

                    # Insert the event
                    event = service.events().insert(calendarId='primary', body=event).execute()

                    print(f'Event created: {event.get("htmlLink")}')

        else:
            print("No assignments found.")

        count = count + 1
