import date_op

class task_view:
    order = ['id', 'pri', 'due', 'con', 'prj']

    def printout(self, tasks, order, task_db):
        if ( order in self.order ):
            getattr(self, 'by_'+order)(tasks, task_db)

    def export(self, tasks, order, format):
        pass

    def by_due(self, tasks, task_db):
        period = {'nodue':0, 'overdue':0, 'today':0, 'week':0, 'future':0}
        due_dates = dict()
        nodue_tasks = set()
        for task in tasks:
            task_due = task_db.get_due(task)
            if ( task_due != None):
                due_dates[task] = task_due
            else:
                nodue_tasks.add(task)
                period['nodue'] += 1

        if ( period['nodue'] > 0 ):
            print "\nNo Due Date"
            getattr(self, 'by_id')(nodue_tasks, task_db)

        for key,value in sorted(due_dates.iteritems(), key=lambda(k,v):(v,k)):
            due_date = due_dates[key]
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
            self.__print_task(key, task_db)
            
        print 'No Due Date: ', period['nodue'], ' Overdue: ', period['overdue'], ' Today: ', period['today'], ' This Week: ', period['week'], ' Week Away: ', period['future']

    def by_pri(self, tasks, task_db):
        pass

    def by_id(self, tasks, task_db):
        for key in sorted(tasks):
            self.__print_task(key, task_db)

    def by_con(self, tasks, task_db):
        pass

    def by_prj(self, tasks, task_db):
        pass

    def __print_task(self, key, task_db):
        print str(key+1).zfill(task_db.get_digits()),task_db.get_task(key)