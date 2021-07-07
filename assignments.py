import errorHandling as Usr_In, json
from datetime import datetime, date, time, timedelta
def loadText(section):
    with open('UI_text.json') as file:
        data = json.load(file)
        return data[section]
text = loadText('assignments')

regex = {'date': '^(19|20)\d\d[- /.](0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])$',
        'weight': '^((100)|([1-9][0-9])|([1-9]))$'}

#Class which manages Course, pass the dict entry of the course to load, otherwise it will automatically
#create a new course dict
class Course():
    def __init__(self, course_dict=None):
        if course_dict is None:
            course_dict = {
                'course_code': Usr_In.specific('Enter the course code:\nEg. 1701ICT\nCode: ','^\d{4}\w{3}$',err_msg='Syntax error, try again!'),
                'name': input('Enter the name of the course: '),
                'note': input('Enter the description/note for the course (leave blank for none): '),
                'assessments': None
            }
        self.code = course_dict['course_code']
        self.name = course_dict['name']
        self.note = course_dict['description']
        self.assignments = []
        #Loads assignments, passes all found dicts through to add_assignment() with their key being the pos
        for key in course_dict['assessments']:
            assign = course_dict['assessments'][key]
            self.add_assignment(key,assign)
    
    #Adds assignment to course, creates a new assignment or loads existing if you pass down a dict and pos
    #Pos is used to order the assignments to make sure the order isn't different every time you view them like in a dict
    def add_assignment(self,pos=len(self.assignments), assign_dict=None):
        if assign_dict is None:
            assign_type = Usr_In.matching(
                text['type_prompt'],
                ('project', 'workshop','multipart'),
                usr_help=text['type_help'],
                err_msg='Incorrect input, try again (tip: type is case sensitive)'
            )
        else: assign_type = assign_dict['type']
        if assign_type == 'project':
            load = Project(pos, assign_dict)
        elif assign_type == 'workshop':
            pass
        elif assign_type == 'multipart':
            pass
        self.assignments.append(load)
        #Re-sorts assignments into correct order
        #How to into sort dict again? something like key=var.get() or something idk 

    #Exports the course to JSON format, bringing assignments with it
    def export(self):
        course = {self.code: {'course_code': self.code, 'name': self.name, 'description': self.note, 'assessments':{}}}
        for i in self.assignments:
            course[self.code]['assessments'].update(i.export())
        return course

#Class for handling project type assessment tasks (one due date), can take a dict to load existing project
#or it will automatically create dict for new assignment
class Project():
    def __init__(self, pos, assign_dict=None):
        if assign_dict is None:
            assign_dict = {
                'title': input('What is the name of the assignment?: '),
                'note': input('Give a description/note for assignment (blank to skip)'), 
                'max_mark': Usr_In.number_int('What is the assignment marked out of? (number): ', err_msg='Expected whole number'),
                'est_mark': 0, 
                'act_mark': 0, 
                'weight': Usr_In.specific(
                    text['proj_weight_prompt'],
                    regex['weight'],
                    usr_help=text['proj_weight_help'],
                    err_msg='Incorrect range, try again!'
                ),
                'submitted': False, 
                'marked': False, 
                'due':  {}
            }
            due = Usr_In.specific(
                    text['proj_due'],
                    regex['date'],
                    err_msg='Invalid date, try again!'
                ).split('-')
            assign_dict['due'].update({'D': int(due[2]), 'M': int(due[1]), 'Y': int(due[0])})
        #Using dict to assign data
        self.title = assign_dict['title']
        self.note = assign_dict['note']
        self.max_mark = assign_dict['max_mark']
        self.est_mark = assign_dict['est_mark']
        self.act_mark = assign_dict['act_mark']
        self.weight = int(assign_dict['weight'])/100
        self.submitted = assign_dict['submitted']
        self.marked = assign_dict['marked']
        self.due_date = date(assign_dict['due']['Y'],assign_dict['due']['M'],assign_dict['due']['D'])
        self.pos = pos
    
    #Prints some basic information about the contained data
    def info(self):
        self.info = f'Assignment: {self.name}\nnote: {self.note}\nDue on: {self.due_date}\nMarked out of {self.max_mark}, it weighs {self.weight}\%\ of the course'
        print(self.info)

    #Exports the data into a dict for dumping into a JSON file
    def export(self):
        return {self.pos: {'title': self.name, 'type':self.type, 'max_mark': self.max_mark,
        'est_mark': self.est_mark, 'act_mark': self.act_mark, 'weight': self.weight,
        'submitted': self.submitted, 'marked': self.marked, 
        'due':{'D': self.due_date.day, 'M': self.due_date.month, 'Y': self.due_date.year}}}
