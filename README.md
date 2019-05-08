#config the project
= project run  on sqliteDB so dont need to change any thing
= the folder have the envirment (env) so dont need to install the package
= Auth Login Username : iti , password : iti
# need To internt to run the project

#Run The project
= First you need to active env so first sure you stop in folder 
and follow this
if linux:
     source env/bin/activate
if windows
    may be need to create env 
    1- cd your_project , pip install virtualenv
    2- virtualenv env
    3-\env\Scripts\activate.bat

= second run server
    cd Task/
    python manage.py runserver
 # to go the dasboard 
    you shoud login 
    user name : iti
    password  : iti
 or create super user  for you
    cd Task/
    python manage.py createsuperuser
    write user name and password
 