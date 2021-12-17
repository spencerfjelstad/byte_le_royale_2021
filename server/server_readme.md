# BYTE LE ROYALE SERVER

## General Setup and overview

This byte-le royale server consists of four parts

1. Postgres SQL database
2. Submission Runner
2. Python Flask API
3. Python Client

The general process is as follows
1. Teams submit clients through the Python client
2. the Client posts the files to the API, which checks for validity and illegal keywords
3. API stores the files in the submission and code file table
4. Submission Runner, which runs every X minutes, creates a new group run
5. Submission Runner gathers the latest submissions from the submission and code tables, runs them against eachother
6. Each run is is inserted in to the run table, with the results and group run id
7. Process finishes, Teams get results through API, which calls the associated function/stored procedures
8. Process repeats

Please note that not all of the functionality needs to be implemented. Only what you want to!

Which will be covered in the following sections.

## Postgres SQL Database

### Set up

#### PLEASE NOTE

The Postgres SQL database has creation scripts to facilitate the simple creation of a new database. Submission Runner gathers the latest submissions from the submission and code tables, runs them against eachother

You should first load the default creation script, then modify and back up into the script using the PGadmin backup tool

1. Create a new database using PGAdmin, 
    1. Log into PG Admin on ACM left Ubuntu. Password is available in the ACM credentials file on the google drive 
    2. create a database under the byte-le-royale group.
    3. be sure to select set tablespace = dbspace. dbspace is the 4tb partition. If this isn't available, see https://stackoverflow.com/questions/9876132/postgresql-creating-database-in-a-specified-location/9876229
2. copy, paste and run the dump.sql file in the query tool. This will create all of the tables and stored procedures
3. copy, paste and run the small_data_insert.sql file, this will insert basic data you need.
4. Modify the database schema as needed.
    1. You will likely need to change the run table, as this has the scoring information which changes from game to game
        1. To see a PvE score based example, see byte-le-royale 2021 branch server
        2. To see a PvP place based example, see byte-le-royale 2022 main branch
    2. The stored procedures / functions will also need to change. Notably insert_run, get_leaderboard, get_stats_for_submission, get_team_score_over_time

### Overview of tables

Please note that Postgres has a ERD diagram tool. Right click the database -> Generate ERD. This will be helpful!

#### University
##### uni_id int, uni_name
Just a table of university names and primary keys

#### Team_Type
##### team_type_id int, team_type_name varchar, eligible bool
Team type is given to the team table so we can determine who can win prizes. eligible is if they are eligible to win prizes.

#### team
##### team_id uuid, team_name varchar, FK uni_id int, FK team_type_id int
Team table for storing teams

#### submission
##### FK team_id uuid, PK submission_id, valid boolean, submit_time timestamp
A submission table, inserts occur every time a team uploads a code file through the client. 

#### code_file
##### FK submission_id int, file_text varchar
This is where python code files are stored. (This is a valid way to do it, as Postgres will store it as a file anyway https://newbedev.com/are-there-performance-issues-storing-files-in-postgresql)

#### group_run
##### PK group_run_id int, start_run timestamp, launcher_version varchar(10)
Group run is a table that groups runs together. The launcher version is useful for determining what version of a launcher a run ran on (duh)

#### run
##### FK submission_id int, PK run_id int, score int, FK group_run_id int, run_time timestamp, FK seed_id int
A run table, for storing each run of a game. Runs that occured together have the same group_run_id. seed_id is is FK for the seed that the run used


#### logs
##### FK run_id, log_text varchar
Table to store game logs for a given run, if you desire

#### errors
##### FK run_id int, error_text varchar
Error table for storing errors that may have occured for each run, if desired

#### seed
##### PK seed_id int, seed varchar
The seed that a given run used. To save space, N seeds will be generated for each group run, with each client being run against the seed. 

### BACK UP DATABASE SCHEMA
To back up the database schema you've altered
1. Right click database
2. Select the dump.sql file in db_dump 
3. Select Format plain
4. Go to Dump Options -> select only schema
5. Click Go


## CLIENT RUNNER

The client runner fetches programs from the database, runs them, and stores their results in the database. 

If the client runner is interupted, the results will be removed from the database using a transaction.
The transaction will be commited once the runner finishes the group run.

If you get an error message like "TCP id already in use" run recover_and_end_transaction.py to rollback and end the transaction. Only one TCP transaction is allowed at a time, having two would be bad!

(Note, by default no TCP transactions are allowed. This must be changed in postgresql.conf)

## SET UP

set up for the client runner is pretty simple

1. Allow "executing files as a program" for all files in the runner folder
2. Change database credentials
3. Change line 121 so the game gets the correct score from the logs

run the program! fix any errors that occur

## UPDATING CLIENT RUNNER

When you make changes to the game during the course of the competition, you must update the client runner!

1. stop the client runner
2. run python3 launcher.pyz update
3. run ./build.sh or ./build.bat
4. start the client runner

That's it!

(I'm sure I'll figure more to add here)


## API







server can be hosted with the command 'gunicorn -b 134.129.91.223:8000 Server:app' for production 