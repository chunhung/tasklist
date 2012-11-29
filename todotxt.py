import sys
import re
import getopt
import time

import date_op

class todotxt:
    filename = ''
    def read_file(self):
        with open(self.filename, 'r') as f:
            lines = f.read().splitlines()
            
        prj_pattern = re.compile('(?<=\ \+)[A-Za-z0-9]*')
        due_pattern = re.compile('(?<=\ \^)[0-9]{4}-[0-1][0-9]-[0-3][0-9]');
        con_pattern = re.compile('(?<=\ \@)[A-Za-z0-9]*')
        prj_dict = dict();
        due_dict = dict();
        con_dict = dict();
        for i, line in enumerate(lines):
            prjs = prj_pattern.findall(line) # Use sets for storing projects 
            dues = due_pattern.findall(line) # Array
            cons = con_pattern.findall(line)
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

        self.todos = {'list':lines, 'prjs':prj_dict, 'due':due_dict}

    def __get_prjs(self, prjs, operator=None):
        tasks = set()
        for prj in prjs:
            if ( len(self.todos['prjs'][prj]) > 0 ):
                if ( operator == 'inter' ):
                    if ( len(tasks) == 0 ):
                        tasks = self.todos['prjs'][prj]
                    else:
                        tasks.intersection(self.todos['prjs'][prj])
                else: # union or one prj only
                    tasks.union(self.todos['prjs'][prj])
        return tasks

    def __get_dues(self, end_date):
        tasks = set()
        today = date.today()
        period = {'overdue':0, 'today':0, 'week':0, 'future':0}
        for key,value in sorted(self.todos['due'].iteritems(), key=lambda(k,v):(v,k)):
            due_date = datetime.datetime.strptime(self.todos['due'][key], '%Y-%m-%d').date()

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
        print 'Do', self.todos['list'][tid]
        print recur, due_date, next_due

    def add_task(self, task):
        f = open(self.filename, 'a')
        f.write(task)
        f.close() 
