import sys
import re
import getopt
import time

import date_op

class todotxt:
    todo_file = '/home/arnose/Dropbox/todotxt/todo.txt'
    done_file = '/home/arnose/Dropbox/todotxt/done.txt'
    digits = 2
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


    def show_prjs(self):
        for prj in self.todos['prjs']:
            print '+'+prj
            i = 0
            for tid in self.todos['prjs'][prj]:
                print int(tid)+1, self.todos['list'][tid]
                i += 1
            print 'There are', i, 'tasks in', prj
            print

    def show_tasks(self):
        i = 1
        for task in self.todos['list']:
            print i, task
            i += 1

    def show_dues(self, end_date=None):
        period = {'overdue':0, 'today':0, 'week':0, 'future':0}
        for key,value in sorted(self.todos['due'].iteritems(), key=lambda(k,v):(v,k)):
            due_date = self.todos['due'][key]
            if ( date_op.before_today(due_date) ):
                if ( period['overdue'] == 0 ):
                    print "\nOverdue"
                period['overdue'] += 1
            elif ( date_op.equal_today(due_date) ):
                if ( period['today'] == 0 ):
                    if ( end_date == 'overdue' ):
                        break
                    else:
                        print "\nToday"
                period['today'] += 1
            elif ( date_op.after_today(due_date) and date_op.compare(due_date, date_op.within(None, None, 7)) == -1 ):
                if ( period['week'] == 0):
                    if ( end_date == 'today' ):
                        break;
                    else:
                        print "\nWithin a Week"
                period['week'] += 1
            else:
                if ( period['future'] == 0 ):
                    if ( end_date == 'week' ):
                        break;
                    else:
                        print "\nIn the future"
                period['future'] += 1
            print key+1,self.todos['list'][key]
        print 'Overdue: ', period['overdue'], ' Today: ', period['today'], ' This Week: ', period['week'], ' Week Away: ', period['future']

    def do_sth(self, tid):
        tid = int(tid)-1
        if ( tid in self.todos['list'] ):
            print 'The number of tasks is', len(self.todos['list'])
            print 'Invalid task id'
            quit()
        recur = re.findall('(?<=\ \*)[A-Za-z]*', self.todos['list'][tid]);
        due_date = self.todos['due'][tid] if tid in self.todos['due'] else None
        next_due = None
        if ( len(recur) > 0 ):
            if ( recur[0] == 'bimonthly' ):
                next_due = date_op.add(due_date, None, 2, None)
            elif ( recur[0] == 'monthly' ):
                next_due = date_op.add(due_date, None, 1, None)
            elif ( recur[0] == 'biweekly' ):
                next_due = date_op.add(due_date, None, None, 14)
            new_task = self.todos['list'][tid].replace(due_date, next_due)
            print new_task

    def add_task(self, task):
        f = open(self.todo_file, 'a')
        f.write(task)
        f.close() 

    def print_tasks(self, tasks, ordered='due'):
        if ( ordered == 'id' ):
            for key in sorted(tasks):
                print str(key+1).zfill(self.digits),self.todos['list'][key]
        elif ( ordered == 'pri' ):
            pass
        elif ( ordered == 'due' ):
            period = {'nodue':0, 'overdue':0, 'today':0, 'week':0, 'future':0}
            due_dates = dict()
            nodue_tasks = set()
            for task in tasks:
                if task in self.todos['due']:
                    due_dates[task] = self.todos['due'][task]
                else:
                    nodue_tasks.add(task)
                    period['nodue'] += 1
            if ( period['nodue'] > 0 ):
                print "\nNo Due Date"
                self.print_tasks(nodue_tasks, 'id')
            for key,value in sorted(due_dates.iteritems(), key=lambda(k,v):(v,k)):
                due_date = self.todos['due'][key]
                if ( date_op.before_today(due_date) ):
                    if ( period['overdue'] == 0 ):
                        print "\nOverdue"
                    period['overdue'] += 1
                elif ( date_op.equal_today(due_date) ):
                    if ( period['today'] == 0 ):
                        print "\nToday"
                    period['today'] += 1
                elif ( date_op.after_today(due_date) and date_op.compare(due_date, date_op.within(None, None, 7)) == -1 ):
                    if ( period['week'] == 0):
                        print "\nWithin a Week"
                    period['week'] += 1
                else:
                    if ( period['future'] == 0 ):
                        print "\nIn the future"
                    period['future'] += 1
                print str(key+1).zfill(self.digits),self.todos['list'][key]
            print 'No Due Date: ', period['nodue'], ' Overdue: ', period['overdue'], ' Today: ', period['today'], ' This Week: ', period['week'], ' Week Away: ', period['future']
        elif ( ordered == 'con' ):
            pass
        elif ( ordered == 'prj' ):
            pass