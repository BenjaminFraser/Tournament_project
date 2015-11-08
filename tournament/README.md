# **SWISS TOURNAMENT DATABASE - README** #

----------


## INTRODUCTION ##

The swiss tournament database is a database system generated through a an SQL file, which works in conjunction with a Python function file and a Python test file. The database allows the registering of players for a swiss style game tournament, followed by recording matches between players, including wins and losses. The players will also be sorted into order of rankings, based on total wins. 

----------


## REQUIREMENTS ##

This project provides you with the following required directory and files:

```
	vagrant/
	├── Vagrantfile
	├── Tournament/
		├── tournament_test.py
		├── tournament.py
		├── tournament.sql
		├── sample_data.py
```
- `Vagrantfile` contains the virtual machine configuration data to enable use of the database in PostgreSQL.
- `tournament.sql` is the setup file for the database schema.
- `tournament.py` contains a library of functions defined in Python for use with the database.
- `tournament_test.py` takes the functions defined within tournament.py, and tests the correct functionality of each functions purpose. 

You will need Git installed on your system to get the Virtual Machine running prior to using the database. You can download the required version of Git for your operating system using this [link](http://git-scm.com/downloads).

If you are on windows Git will provide you with a linux style terminal and shell called Git bash. If you are using a Mac system or Linux the regular terminal program will suffice. 

You will also need VirtualBox to run the Virtual Machine, where you must download the platform package relevant to your operating system. No extension pack or SDK is required with VirtualBox for the database, nor do you need to manually launch VirtualBox after installation. The link for download can be accessed [here](https://www.virtualbox.org). 

Finally, you shall need Vagrant installed to allow configuration of the virtual machine and allow file sharing between the host and VM. You can download Vagrant [here](https://www.vagrantup.com).

---------


## QUICK START ##

In order to get the tournament database up and running, follow the series of steps given below:

1 - Download the tournament database directory to obtain the directory and files listed above, and store these somewhere accessible so that you know the path to the tournament directory.

2 - You shall need Git, Vagrant and VirtualBox installed as instructed above in order to use the database.

3 - Using the terminal, navigate to the `/vagrant` directory in the downloaded fileset, and use the command `vagrant up`. If it is your first time running this it may take some time. Once it is up and running, type `vagrant ssh` in order to log in. You should now be operating within the Vagrant Virtual Machine. 

4 - Within the Vagrant VM, change directory to the tournament folder using `cd /vagrant/tournament`.

5 - You can now run the database in PostgreSQL within the VM and utilise the `psql` program. To setup the database initially, you must run the tournament.sql file using the psql program, which can be done by running: 
	`psql -f tournament.sql`
in the Virtual machine command line.

6 - The database can be tested for full functionality using the tournament_test.py file through the VM command line. Simply input `python tournament_test.py`. The functions tested against these tests are defined within tournament.py.

7 - If sample data for insertion into the tournaments is required, it can be loaded into the database through running the sample_data.py file using `python sample_data.py` from the VM `/tournament` directory.

--------

## CREATOR ##

Benjamin Fraser

--------
