tasklist
========

A todo-txt compatible task management with similar notation as Remember the Milk(RTM). Written in Python.

Format
======

The task format may contain the following notation for further operatios.
* @ : Context
* ^ : Due Date
* + : Project
* \* : Recursive interval

In order to be compatible with todo.txt, all new added tasks are appended in todo.txt and anything done will be removed and appended in done.txt.

Feature
=======

* Due Date
  * List the tasks in the sections of "Overdue", "Today", "Within the Week", and "In the Future"
  * Only list the tasks with the due dates which are "Overdue", or "Overdue" and "Today" or "Overdue", "Today", and "Within the Week"
* Recursive
  * When "Do" something and if it is recursive, the new task will be added with the due date plus the interval, such as, "yearly", "bimonthly", "monthly", "biweekly", and "weekly".
* Project
  * Shows the tasks in the sections of projects
  * Shows the tasks of the specified projects
* Context
  * Shows the tasks with the union or intersection of contexts

Todo
====
* Remove done tasks and move done tasks to done.txt