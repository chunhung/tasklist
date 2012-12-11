import sys
import re

import date_op

class task_db:
    prefix = '/home/arnose/Dropbox/todotxt'
    todo_file = prefix+'/todo.txt'
    done_file = prefix+'/done.txt'
    digits = 2

    def __init__(self, conf=None):
        self.read_file()

    def get_task(self, tid):
        return self.todos['list'][tid] if ( tid < len(self.todos['list']) ) else None

    def get_digits(self):
        return self.digits
    
    def get_due(self, tid):
        return self.todos['due'][tid] if ( tid in self.todos['due'] ) else None

    def get_num_tasks(self):
        return len(self.todos['list'])

    def replace_task(self, tid, due_date, next_due):
        return self.todos['list'][tid].replace(due_date, next_due)

    def is_recur(self, tid):
        recur_pattern = self.get_pattern('recur')
        recur = recur_pattern.findall(self.todos['list'][tid])
        return recur[0] if ( len(recur) > 0 ) else None

    def do_task(self, tid):
        recur = self.is_recur(tid)
        due_date = self.get_due(tid)
        next_due = None

        self.__task_done(tid)

        if ( recur != None ):
            if ( recur == 'bimonthly' ):
                next_due = date_op.add(due_date, None, 2, None)
            elif ( recur == 'monthly' ):
                next_due = date_op.add(due_date, None, 1, None)
            elif ( recur == 'biweekly' ):
                next_due = date_op.add(due_date, None, None, 14)

            new_task = self.replace_task(tid, due_date, next_due)
            self.add_task(new_task)

    def __task_done(self, tid):
        task = self.get_task(tid)
        done = 'x ' + str(date_op.today()) + ' ' + task

        f = open(self.done_file, 'a')
        f.write(done+'\n')
        f.close()

        f = open(self.todo_file, 'w')
        for line in self.todos['list']:
            if ( task in line ):
                pass
            else:
                f.write(line+'\n')

    def add_task(self, task):
        task = self.__get_date_pattern(task)
        f = open(self.todo_file, 'a')
        f.write(task+'\n')
        f.close()

        # Following operations are not needed if todo is called every time
        # However, if the todo is a recursive operation waiting for command
        # It is necessary to update the memory information
        task_prop = self.__parse_task(task)
        tid = len(self.todos['list'])
        for prj in task_prop['prjs']:
            if prj not in self.todos['prjs']:
                self.todos['prjs'][prj] = set()
            self.todos['prjs'][prj].add(tid)
        for con in task_prop['cons']:
            if con not in self.todos['cons']:
                self.todos['cons'][con] = set()
            self.todos['cons'][con].add(tid)
        for due in task_prop['dues']:
            self.todos['due'][tid] = due
        for pri in task_prop['pris']:
            self.todos['pri'][tid] = pri
        self.todos['list'].append(task)
        if ( 10**(self.digits-1) < tid ):
            self.digits += 1

    def __get_date_pattern(self, task):
        today = date_op.today()
        date_pattern = {
            'today':today,
            'next week':date_op.add(today, None, None, 7),
            'next month':date_op.add(today, None, 1, None),
            'next year':date_op.add(today, 1, None, None)}
        for key in date_pattern.keys():
            value = date_pattern[key]
            replace = re.sub('\ '+key+'\ ', '\ '+value+'\ ', task)
            if ( replace != task ):
                return replace
                break

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
    
    def __parse_task(self, task):
        prj_pattern = self.get_pattern('prj')
        due_pattern = self.get_pattern('due')
        con_pattern = self.get_pattern('con')
        pri_pattern = self.get_pattern('pri')
        prjs = prj_pattern.findall(task)
        dues = due_pattern.findall(task)
        cons = con_pattern.findall(task)
        pris = pri_pattern.findall(task)

        return {'prjs':prjs, 'dues':dues, 'cons':cons, 'pris':pris}

    def read_file(self):
        with open(self.todo_file, 'r') as f:
            lines = f.read().splitlines()
            
        prj_dict = dict()
        due_dict = dict()
        con_dict = dict()
        pri_dict = dict()

        for i, line in enumerate(lines):
            task_prop = self.__parse_task(line)
            for prj in task_prop['prjs']:
                if prj not in prj_dict:
                    prj_dict[prj] = set()
                prj_dict[prj].add(i)
            for con in task_prop['cons']:
                if con not in con_dict:
                    con_dict[con] = set()
                con_dict[cont].add(i)
            for due in task_prop['dues']:
                due_dict[i] = due
            for pri in task_prop['pris']:
                pri_dict[i] = pri

        self.todos = {'list':lines, 'prjs':prj_dict, 'due':due_dict, 'pri':pri_dict}
        total = len(lines)
        digits = 1
        while ( total >= 10 ):
            total /= 10
            digits += 1
        self.digits = digits

    def get_prjs(self):
        return self.todos['prjs']

    def get_prjs_tasks(self, prjs=None, operator=None):
        tasks = set()
        if ( prjs == None ):
            prjs = self.get_prjs()
        for prj in prjs:
            if ( (prj in self.todos['prjs']) and len(self.todos['prjs'][prj]) > 0 ):
                if ( operator == 'inter' ):
                    if ( len(tasks) == 0 ):
                        tasks = self.todos['prjs'][prj]
                    else:
                        tasks = tasks.intersection(self.todos['prjs'][prj])
                else: # union or one prj only
                    tasks = tasks.union(self.todos['prjs'][prj])
        return tasks

    def get_done(self):
        with open(self.done_file, 'r') as f:
            lines = f.read().splitlines()
        return lines

    def get_dues(self, end_date=None):
        if ( end_date != None ):
            today = date_op.today()
            if ( end_date == 'today' ):
                end_date = today
            elif ( 'week' in end_date ):
                end_date = date_op.add(today, None, None, 6)
            elif ( 'month' in end_date ):
                end_date = date_op.add(today, None, 1, None)
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
