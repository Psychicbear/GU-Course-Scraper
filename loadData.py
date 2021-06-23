#Tests the input of JSON course
import json
from scraper import Course
from datetime import date
user = ''
courses = []
with open('sampleprofile.json') as file:
    data = json.load(file)
    user = data['settings']['user']
    print(data['courses'])
    for key in data['courses']:
        courses.append(Course(data['courses'][key])) 
print(f'Welcome {user}, your courses: ')
print(courses[0].name)