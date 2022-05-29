# Archive
The project in hand is an archive manager system that enables the user to download an
SQL file from a given link and place a tgz archive format of the file in a remote server.
Upon launching the setup file all dependencies needed for the project are installed and a
crontab file is created to automate the execution of the project’s script. The system also
allows the user to personalise its configuration through a configuration file, thus allowing
the user to specify the link of the SQL file, duration of historization, and to enable or
disable receiving notifications on a Mattermost server. This project is written in python,
and ideally to be executed and used on a linux based OS.
