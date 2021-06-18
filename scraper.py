#Goals
#Web GET website with request
#Request different teaching period based on date
#Parses response html and prompts for campus
#Gets courseID of selected campus course and goes to different pages
#Reads assignments with mark weighting
#Presents it all to the viewer
import requests
from datetime import datetime, date, time, timedelta
from bs4 import BeautifulSoup as soup, SoupStrainer
url = 'https://app.griffith.edu.au/course-profile-search/'
html_RAW = requests.get(url).text
site = soup(html_RAW, 'html.parser')
#print(site.prettify())
#8 Mar Tri1S, June 7 Tri2E, 12 July Tri2S, Nov 1 Tri1E
smt_tri = [datetime(2021,3,8),datetime(2021,6,7),datetime(2021,7,12),datetime(2021,11,1)]

class Course():
    def __init__(self, pID):
        self.pID = pID
        self.url = 'https://courseprofile.secure.griffith.edu.au/student_section_loader.php'
    
    def profile_request(self,section):
        params = {'section': section, 'profileId': self.pID}
        html_RAW = requests.get(url=self.url, params=params).text
        return soup(html_RAW, 'html.parser')

    def add_assignments(self):
        pass

class Assignment():
    def __init__(self, title, weight, marked):
        self.title = title
        self.type = 'base'
        self.weight = weight

    def parseDate(self, date):
        
        


def main(courseCode):
    pass

def semesterSelect(site):
    tri_time = site.find(string='Trimester 2 2020').find_parent('option')['value']
    return tri_time

def courseRequest(url, semcode):
    campus_list = []
    params = {'course_code': input('Enter a course code: '), 'semester': semcode}
    r = soup(requests.get(url=url,params=params).text, 'html.parser', parse_only=SoupStrainer('table'))
    #print(r.prettify())
    campus_prompt = 'Which campus is your course?\n'
    j = 0
    for i in r.find_all('td'):
        if 'Campus' in i.string and i.string not in campus_list:
            campus_list.append(i.string)
            campus_prompt += f'{i.string}({j}) '
            j+=1
    campus = ''
    while not campus: 
        try: 
            campus = campus_list[int(input(campus_prompt + '\nEnter number: '))]
        except:
            campus = ''
            print('Invalid number, try again')
    campus = r.find(string=campus).find_parents('tr')[0]
    profileID = campus.find('a')
    profileID = get_profileID(profileID['href'])
    print(profileID)
    return profileID

def get_profileID(url):
    return ''.join(url[-6:])

def scrape_course(pID):
    pass

profileID = courseRequest(url,semesterSelect(site))
test = Course(profileID)
print(test.profile_request('5'))