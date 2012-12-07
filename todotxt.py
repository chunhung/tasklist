import sys

from task_view import task_view
from task_db import task_db

class todotxt:
    def __init__(self):
        self.task_db = task_db()
        self.task_view = task_view()
        
    def show_prjs(self, prjs=None, operator=None):
        if ( prjs == None ):
            prjs = self.task_db.get_prjs()
            print "Existed Projects: "
            for prj in prjs:
                print prj
            quit()
        tasks = self.task_db.get_prjs_tasks(prjs, operator)
        self.print_tasks(tasks, 'due')

    def show_tasks(self):
        self.print_tasks(self.task_db.get_prjs_tasks(), 'id')

    def show_dues(self, end_date=None):
        # TODO
        # We need to verify end_date is a valid string format for date
        # It is better to support only month and day as the same year is assumed
        # when the month and day is after today
        self.print_tasks(self.task_db.get_dues(end_date))

    def do_sth(self, tid):
        tid = int(tid)-1
        if ( self.task_db.get_task(tid) == None ):
            print 'The number of tasks is', self.task_db.get_num_tasks()
            print 'Invalid task id'
            quit()
        recur = self.task_db.is_recur(tid)
        due_date = self.task_db.get_due(tid)
        next_due = None
        print 'x', date_op.today(), self.task_db.get_task(tid)
        if ( recur != None ):
            if ( recur == 'bimonthly' ):
                next_due = date_op.add(due_date, None, 2, None)
            elif ( recur == 'monthly' ):
                next_due = date_op.add(due_date, None, 1, None)
            elif ( recur == 'biweekly' ):
                next_due = date_op.add(due_date, None, None, 14)

            new_task = self.task_db.replace_task(tid, due_date, next_due)
            print new_task

    def add_task(self, task):
        f = open(self.todo_file, 'a')
        f.write(task)
        f.close() 

    def print_tasks(self, tasks, order='due'):
        self.task_view.printout(tasks, order, self.task_db)
