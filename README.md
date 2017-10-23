# Project: Logs Analysis 
## Desciption
Python3 script using SQL to query a PostgreSQL database for 3 answers, they are:
1. The 3 most popular articles
2. The most popular authors
3. Days with requests containing more than 1% errors

## Technology
* Python3
* PostgreSQL
* VirtualBox with Vagrant

## Deploy code
1. Install VirtualBox: https://www.virtualbox.org/wiki/Download_Old_Builds_5_1
2. Install Vagrant: https://www.vagrantup.com/downloads.html
3. Download VM configuration: https://d17h27t6h515a5.cloudfront.net/topher/2017/August/59822701_fsnd-virtual-machine/fsnd-virtual-machine.zip
4. In terminal cd into "vagrant" directory.
5. Start virtual machine in terminal by running "vagrant up"
6. Log-in to virtual machine in terminal by running "vagrant ssh"
7. Download PostgreSQL database "News": https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip
8. The following views must be created in database, as they are referenced by ReportingTool.py script (Remember to delete "").
* "CREATE view entries_view as
select date(time) as date1,
count(id) as visitors_daily
from log group by date1;"
* "CREATE view errors_view as
select date(time) as date2,
count(status) as error_daily
from log where status = '404 NOT FOUND' 
group by date2;"
9. Copy "News" database to vagrant folder.
10. Connect with database by running in terminal "psql -d news -f newsdata.sql" (done once)
11. Clone this repository to "vagrant" directory.
12. Execute python script by running in terminal "python3 ReportingTool.py"
13. Enjoy!