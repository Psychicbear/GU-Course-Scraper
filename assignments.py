import errorHandling as Usr_In, json
from datetime import datetime, date, time, timedelta
def loadText(section):
    with open('UI_text.json') as file:
        data = json.load(file)
        return data[section]
text = loadText('assignments')

regex = {'date': '^(19|20)\d\d[- /.](0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])$',
        'weight': '^((100)|([1-9][0-9])|([1-9]))$'}
courseJSON = {}
def saveJSON():
    with open('test.json',mode='w') as outfile:
        json.dump(courseJSON, outfile, indent=4)
        return

class NewCourse():
    def __init__(self):
        self.code = Usr_In.specific('Enter the course code:\nEg. 1701ICT\nCode: ','^\d{4}\w{3}$',err_msg='Syntax error, try again!')
        self.name = input('Enter the name of the course: ')
        self.note = input('Enter the description/note for the course (leave blank for none): ')
        self.assignments = []
    
    def add_assignment(self):
        assign_type = Usr_In.matching(
            text['type_prompt'],
            ('project', 'workshop','multipart'),
            usr_help=text['type_help'],
            err_msg='Incorrect input, try again (tip: type is case sensitive)'
            )
        name = input('What is the name of the assignment?: ')
        note = input('Give a description/note for assignment (blank to skip)')
        if assign_type == 'project':
            due = Usr_In.specific(
                text['proj_due'],
                regex['date'],
                err_msg='Invalid date, try again!'
                ).split('-')
            due = date(int(due[0]),int(due[1]),int(due[2]))
            marks = Usr_In.number_int('What is the assignment marked out of? (number): ', err_msg='Expected whole number')
            weight = Usr_In.specific(
                text['proj_weight_prompt'],
                regex['weight'],
                usr_help=text['proj_weight_help'],
                err_msg='Incorrect range, try again!'
                )
            weight = int(weight)/100
        self.assignments.append(NewProject(name,note,due,marks,weight,len(self.assignments)))
        self.assignments[0].info()
    
    def export(self):
        course = {self.code: {'course_code': self.code, 'name': self.name, 'description': self.note, 'assessments':{}}}
        for i in self.assignments:
            course[self.code]['assessments'].update(i.export())
        courseJSON.update(course)
        saveJSON()


class NewProject():
    def __init__(self,name,note,due,marks,weight,pos):
        self.name = name
        self.type = 'project'
        self.note = note
        self.due_date = due
        self.max_mark = marks
        self.est_mark = 0
        self.act_mark = 0
        self.weight = weight
        self.submitted = False
        self.marked = False
        self.pos = 'A' + str(pos)
    
    def setDueDate(self, due):
        due = due.split('-')
        return date(int(due[2]),int(due[1]),int(due[0]))

    def info(self):
        self.info = f'Assignment: {self.name}\nnote: {self.note}\nDue on: {self.due_date}\nMarked out of {self.max_mark}, it weighs {self.weight}\%\ of the course'
        print(self.info)

    def export(self):
        return {self.pos: {'title': self.name, 'type':self.type, "max_mark": self.max_mark,
        'est_mark': self.est_mark, 'act_mark': self.act_mark, 'weight': self.weight,
        'submitted': self.submitted, 'marked': self.marked, 
        'due':{'D': self.due_date.day, 'M': self.due_date.month, 'Y': self.due_date.year}}}

classtest = NewCourse()
classtest.add_assignment()
#courseJSON.update(classtest.export())