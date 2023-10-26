import requests

# Replace with your Canvas API endpoint and access token
# THIS WILL NOT WORK WITHOUT REPLACING WITH YOUR OWN ACCESS TOKEN
# Make sure 'Bearer' is in front of it as well
base_url = "https://sju.instructure.com/api/v1/"
headers = {
    "Authorization": "Bearer CANVAS_ACCESS_TOKEN" 
}

# Make a GET request to retrieve a list of courses
response = requests.get(base_url + "courses", headers=headers)

# Check the response status code
if response.status_code == 200:
    courses = response.json()
    # Filter and display only actively enrolled courses
    for course in courses:
        enrollments = course.get("enrollments", [])
        for enrollment in enrollments:
            if enrollment.get("enrollment_state") == "active":
                print("Course Name:", course["name"])
                print("Course Code:", course["course_code"])
                print("Course ID:", course["id"])
                print("------------------------------")
else:
    print("Error:", response.status_code)
