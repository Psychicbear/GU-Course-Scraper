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
                'description': input('Enter the description/note for the course (leave blank for none): '),
                'assessments': {}
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
    def add_assignment(self, pos=None, assign_dict=None):
        if assign_dict is None:
            assign_type = Usr_In.matching(
                text['type_prompt'],
                ('project', 'workshop','multipart'),
                usr_help=text['type_help'],
                err_msg='Incorrect input, try again (tip: type is case sensitive)'
            )
        if pos is None:
            pos = len(self.assignments)
        else: assign_type = assign_dict['type']
        if assign_type == 'project':
            load = Project(pos, assign_dict)
        elif assign_type == 'workshop':
            pass
        elif assign_type == 'multipart':
            pass
        self.assignments.append(load)
        #Re-sorts assignments into correct order
        self.assignments.sort(key=lambda x:x.pos)

    def info(self):
        if self.note == '': self.note = 'No note given'
        print(f'{self.code} {self.name} - {self.note}')

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
        self.info = f'Assignment: {self.title}\nnote: {self.note}\nDue on: {self.due_date}\nMarked out of {self.max_mark}, it weighs {self.weight}\%\ of the course'
        print(self.info)

    #Exports the data into a dict for dumping into a JSON file
    def export(self):
        return {self.pos: {'title': self.title,'note':self.note, 'type':'project', 'max_mark': self.max_mark,
        'est_mark': self.est_mark, 'act_mark': self.act_mark, 'weight': self.weight,
        'submitted': self.submitted, 'marked': self.marked, 
        'due':{'D': self.due_date.day, 'M': self.due_date.month, 'Y': self.due_date.year}}}

class Workshop():
    def __init__(self, assign_dict=None):
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
            #Ask total weight of weeks
            weight = Usr_In.number_int('What is the total weight of all weeks combined?\n ?: ', err_msg='Expected whole number') / 100
            #Prompt how many weeks there are
            total_weeks = Usr_In.number_int('How many weeks are assessed?\n ?: ')
            #Ask which week assessed weeks start
            start_week = Usr_In.number_int('What week do these assessments start?\n ?: ')
            #Ask how many weeks have different value
            diff_weeks = []
            diff_weight = 0.0
            amt_diff_weeks = input('If any weeks are worth more, how many? (leave blank if none)\n ?: ')
            #Loop and ask for week and value
            if amt_diff_weeks != '':
                total = int(amt_diff_weeks)
                for i in range(total):
                    print(f'{i}/{total} different weeks')
                    current_week = Usr_In.number_int('Week number of different weight?\n ?: ')
                    current_weight = Usr_In.number_int('What is the weight of this week?\n ?: ', err_msg='Expected whole number') / 100
                    diff_weight += current_weight
                    diff_weeks.append([current_week,current_weight])
                reg_weight = (weight - diff_weight)/(total_weeks - amt_diff_weeks)
            else: reg_weight = weight/total_weeks
            #Generate each week
            weeks = {}
            for i in range(total_weeks):
                week_num = i+start_week
                if diff_weeks != []:
                    for j in diff_weeks:
                        if week_num in j: week_weight = j[1]
                        else: week_weight = reg_weight
                else: week_weight = reg_weight
                week_dict = {
                    'week': week_num
                }

#Submission class
#Is created for every instance where a mark and due date is used eg. Assignment, Workshop etc
#Takes a parent and optional existing data, substituting the existing data into the instance when provided
class Submission():
    def __init__(self, parent, existingData=False):
        self.parent = parent #The class in which this submission is contained within
        self.data = existingData #Existing object containing data, will push contained data to attributes
        self.dueDate = self.data['date'] if self.data else date #datetime format
        self.isSubmitted = self.data['submitted'] if self.data else False #Boolean to be changed once assignment submitted
        self.isMarked = self.data['submitted'] if self.data else False #Boolean to be changed once assignment marked
        self.totalMarks = self.data['total'] if self.data else Usr_In.number_int('Please enter the total marks of this item', err_msg = "Incorrect input, please ensure you're entering a whole number") #Int
        self.guessMarks = self.data['guess'] if self.data else 0 #Int for predicted marks
        self.actualMarks = self.data['actual'] if self.data else 0 #Int for actual marks when recieved
        self.weight = self.data['weight'] if self.data else Usr_In.number_int('Please enter weight of this item (whole number without percentage)') / 100 #2f float, percentage value of mark
        self.calculatedMark = self.data['calculated'] if self.data else 0.00 #Calculated total value of submission in relation to full class mark 

    def calculateMarks(self):
        pass
        #self.calculatedPercentage =  (self.guessMarks/self.totalMarks) if self.guessMarks


            