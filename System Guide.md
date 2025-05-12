System Guide for Paws in Motion application.

First, in order to run the application, the initial requirements will have to be installed.

Initial requirements:
- Python installation
- Flyway installation
- MySQL database

Next, a python environment will have to be created in the server that will host the application.
Please see python documentation for instructions on setting up python environment.

Next, the required python libraries will have to be installed in the python environment using 'pip install' command.
Please see python documentation for full instructions on the 'pip install' command.
Note that these python libraries are included in a 'requirements.txt' file in the repository. Some IDEs may allow for batch installing from this file.

Required Python Libraries:
- fastapi
- uvicorn
- pydantic
- sqlalchemy
- mysql-connector-python
- Jinja2
- djlint
- datetime
- python-multipart
- geopy

Next, please refer to MySQL documentation to prepare a database for holding the application data.
Next, please refer to Flyway documentation to install Flyway.

Once MySQL and Flyway installations are complete, within the application code, navigate to 'flyway/conf/flyway.conf' to access the Flyway configuration file.
Enter your MySQL database connection details into this configuration file.

Next, follow Flyway documentation instructions to run these Flyway commands with the SQL files contained in 'flyway/sql':
- .\run_flyway.cmd baseline
- .\run_flyway.cmd info
- .\run_flyway.cmd migrate
- .\run_flyway.cmd info

The baseline command will record what your database looks like before running other commands.
The initial info command should show all 'flyway/sql' files as 'Pending'.
The migrate command will create the application's SQL tables in your MySQL database.
The second info command should confirm all 'flyway/sql' files statuses as 'Success'.

Finally, the application can be started by navigating to the 'src' folder and running the command:
- python app.py 

FOR GIT BASH USERS
uvicorn app:app --reload