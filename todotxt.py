import sys
import re

import date_op
import task_view
import task_db

class todotxt:
    def __init__(self):
        self.task_db = task_db()
        
    def show_prjs(self, prjs=None, operator=None):
        if ( prjs == None ):
            prjs = self.__get_prjs()
        tasks = self.__get_prjs_tasks(prjs, operator)
        self.print_tasks(tasks, 'due')

    def show_tasks(self):
        self.print_tasks(self.__get_prjs_tasks(), 'due')

    def show_dues(self, end_date=None):
        # TODO
        # We need to verify end_date is a valid string format for date
        # It is better to support only month and day as the same year is assumed
        # when the month and day is after today

        self.print_tasks(self.__get_dues(end_date))

    def do_sth(self, tid):
        tid = int(tid)-1
        if ( tid in self.todos['list'] ):
            print 'The number of tasks is', len(self.todos['list'])
            print 'Invalid task id'
            quit()
        recur_pattern = self.get_pattern('recur')
        recur = recur_pattern.findall(self.todos['list'][tid])
        due_date = self.todos['due'][tid] if tid in self.todos['due'] else None
        next_due = None
        print 'x', date_op.today(), self.todos['list'][tid]
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