# Repeating ToDos

General Idea:
* Get a list of repeating todos that you can check off and then they pop up again based on recurrence.

Good to have features:
* See dashboard with tracking like stuff completed on time etc

Next Steps:
* Current State: API for task templates is ready and tasks are being created from task_templates
* Extend/Update created tasks for a task template:
  * ~~Just find the last created instance, and move ahead with it.~~
  * ~~To do this, you need to update the get_dates_from_* functions to use start_date instead of datetime.now()~~
  * Write API Endpoint for this
* ~~Add checks in task_template apis that the correct user is accessing~~
* Add endpoints to update status of task instances with user verification checks
* Create react dashboard
* Dockerize this stuff

User views:
* Monthly:
  * Show all monthly tasks with dates
  * Show all weeks with num tasks in that week
* Monthly 2:
  * Show dates in months with each date having:
    * A task if any monthly task exists in it
    * Num tasks in that day
  * Show weekly stats in the week counter towards left of calendar
* Weekly:
  * Show all days where each day has a weekly task + count of daily tasks in that day
* Daily:
  * Show any weekly tasks falling on that day and all daily tasks for it
