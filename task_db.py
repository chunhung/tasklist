import sys
import re

class task_db:
    todo_file = '/home/arnose/Dropbox/todotxt/todo.txt'
    done_file = '/home/arnose/Dropbox/todotxt/done.txt'
    digits = 2

    def __init__(self, conf=None):
        self.read_file()

    def get_task(self, tid):
        return self.todos['list'][tid]

    def get_digits(self):
        return self.digits
        
    def get_pattern(self, pattern_type):
        if ( pattern_type == 'prj' ):
            return re.compile('(?<=\ \+)[A-Za-z0-9]*')
        elif ( pattern_type == 'due' ):
            return re.compile('(?<=\ \^)[0-9]{4}-[0-1][0-9]-[0-3][0-9]')
        elif ( pattern_type == 'con' ):
            return re.compile('(?<=\ \@)[A-Za-z0-9]*')
        elif ( pattern_type == 'recur' ):
            return re.compile('(?<=\ \*)[A-Za-z]*')
        elif ( pattern_type == 'pri' ):
            return re.compile('^\([A-Z]*\)')
    
    def read_file(self):
        with open(self.todo_file, 'r') as f:
            lines = f.read().splitlines()
            
        prj_pattern = self.get_pattern('prj')
        due_pattern = self.get_pattern('due')
        con_pattern = self.get_pattern('con')
        pri_pattern = self.get_pattern('pri')
        prj_dict = dict()
        due_dict = dict()
        con_dict = dict()
        pri_dict = dict()
        for i, line in enumerate(lines):
            prjs = prj_pattern.findall(line) # Use sets for storing projects 
            dues = due_pattern.findall(line) # Array
            cons = con_pattern.findall(line)
            pris = pri_pattern.findall(line)
            for prj in prjs:
                if prj not in prj_dict:
                    prj_dict[prj] = set()
                prj_dict[prj].add(i)
            for con in cons:
                if con not in con_dict:
                    con_dict[con] = set()
                con_dict[cont].add(i)
            for due in dues:
                due_dict[i] = due
            for pri in pris:
                pri_dict[i] = pri

        self.todos = {'list':lines, 'prjs':prj_dict, 'due':due_dict, 'pri':pri_dict}
        total = len(lines)
        digits = 1
        while ( total >= 10 ):
            total /= 10
            digits += 1
        self.digits = digits

        def __get_prjs(self):
        return self.todos['prjs']

    def __get_prjs_tasks(self, prjs=None, operator=None):
        tasks = set()
        if ( prjs == None ):
            prjs = self.__get_prjs()
        for prj in prjs:
            if ( len(self.todos['prjs'][prj]) > 0 ):
                if ( operator == 'inter' ):
                    if ( len(tasks) == 0 ):
                        tasks = self.todos['prjs'][prj]
                    else:
                        tasks = tasks.intersection(self.todos['prjs'][prj])
                else: # union or one prj only
                    tasks = tasks.union(self.todos['prjs'][prj])
        return tasks

    def __get_dues(self, end_date=None):
        if ( end_date != None ):
            if ( end_date == 'today' ):
                end_date = date_op.today()
            else:
                end_date = date_op.get_date(end_date)

        tasks = set()

        for key,value in sorted(self.todos['due'].iteritems(), key=lambda(k,v):(v,k)):
            if ( end_date != None ):
                due_date = date_op.get_date(self.todos['due'][key])
                if ( date_op.compare(due_date, end_date) <= 0 ):
                    tasks.add(key)
            else:
                tasks.add(key)

        return tasks

    def __get_cons(self, cons):
        pass

    def __get_pris(self, pris):
        pass