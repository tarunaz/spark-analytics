# Role to start a simple spark test example

## Start a new analytic job pod
Upload a job config to start a simple sample spark job.

### Pausing job
After starting the job, by default setting the playbook will pause
until the job is finished. If don't want playbook to
be paused, pass the variable 'oshinko_wait_job=false' to the role.


