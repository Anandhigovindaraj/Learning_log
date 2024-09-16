ame : "ll_project"
type : "python:3.12.3"


relationships:
   database : "db:postgresql"


 # The configuration of the app when it's exposed to the web.
web:

  upstream:
       socket_family: unix

  commands:
       start: "gunicorn-w 4-b unix:$SOCKET ll_project.wsgi:application"

  locations:
       "/":
            passthru: true

       "/static":
         root: "static"
         expires : 1h
         allow : true 

  # The size of the persistent disk of the application (in MB)
disk : 512
    
  # Set a local read/write mount for logs.
mounts :
   "logs":
         source : local
         source_path : logs

  # The hooks executed at various points in the lifecycle of the application.
hooks :
    build : |
       pip install --upgrade pip
       pip install -r requirements.txt
       pip install -r requirements_remote.txt


       mkdir logs
       python manage.py collectstatic
       rm -rflogs
    
    deploy : |
       python manage.py migrate
