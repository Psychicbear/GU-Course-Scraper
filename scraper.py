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
#Predictive Trimester Suggestion
smt_tri = {'Tri1Start': datetime(2021,3,8),'Tri2Plan': datetime(2021,6,7),'Tri2Start': datetime(2021,7,12), 'Tri1Plan': datetime(2021,11,1)}

#Course class, takes a dict which MUST include {pID: str, saved: boolean, course_code: str}
class Course():
    def __init__(self, data):
        self.pID = data['pID']
        self.code = data['course_code']
        self.url = 'https://courseprofile.secure.griffith.edu.au/student_section_loader.php'
        self.loadCourse(data)
    
    #Requests specified section of course profile
    def profile_request(self,section):
        params = {'section': section, 'profileId': self.pID}
        html_RAW = requests.get(url=self.url, params=params).text
        return soup(html_RAW, 'html.parser')
    
    #Takes the data dict and loads relevent data if possible
    def loadCourse(self, dd):
        if dd['saved'] is True:
            self.name = dd['name']
            self.staff= dd['staff']
            self.assessments = dd['assessments']
            print('Course loaded')
            self.present_info()
        else:
            self.set_name()
            self.get_contact()

    #WIP Parses section 5, creates an assignment class, currently only Basic(), appends complete course to Course.assignments list 
    def add_assignments(self):
        pass
    
    #Parses section 1 of profile, slices just name out of the h1 containing course info overview and passes result to Course.name
    def set_name(self):
        page = self.profile_request('1')
        for i in page.find_all('h1'):
            if self.code in i.string:
                 title = ''.join(i.string[:i.string.index(self.code)])
                 self.name = title
        
    #Parses section 1 of profile, checks every table after "Course Staff" and appends contents to Course.staff
    def get_contact(self):
        page = self.profile_request('1')
        staff = page.find(id='course-staff').find_all_next('table')
        for i in staff:
            member = {}
            print(i.find_parent('Phone'))
        print(staff)

    #Used to present course overview to user
    def present_info(self):
        print(f'Course: {self.name}')


#Basic Project assignment, takes assignment title, it's weight as float decimal, 'marked out of' as int in max_mark
class Base():
    def __init__(self, data):
        self.title = data['title']
        self.max_mark = data['max_mark']
        self.est_mark = data['est_mark']
        self.act_mark = data['act_mark']
        self.weight = data['weight']
        self.submitted = data['submitted']
        self.marked = data['marked']
        self.duedate = date(data['due']['Y'],data['due']['M'],data['due']['D'])
        
    def estimate_mark(self):
        while True:
            try:
                mark = int(input('Enter your estimated mark: '))
                if mark < 0 or mark > self.max_mark:
                    raise Exception('Invalid mark range')
            except: 
                print(f'Invalid mark, try again.\nTip: {self.max_mark} is your max mark, make sure your mark is within this!')
                continue
            else: break
        self.est_mark = mark

    def prcnt_mark(self):
        if self.act_mark > 0:
            return str(self.act_mark / self.max_mark) + '%'
        else: return str(self.est_mark / self.max_mark) + '%' 
        
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
    #Adds campus names along with allocated numbers to prompt
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
    return Course({'pID': profileID, 'saved': False, 'course_code': params['course_code']})

def get_profileID(url):
    return ''.join(url[-6:])

def scrape_course(pID):
    pass

#profileID = courseRequest(url,semesterSelect(site))
#testfull = courseRequest(url, semesterSelect(site))
test = Course({'pID': '115818', 'saved': False, 'course_code':'1805ICT'})#Tests course scraper
#test.get_contact()
print(test.name)
#print(test.profile_request('1'))
