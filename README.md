# Python Back-End :egypt:

## Any Django Project :telescope: 

```
python3 -m venv env
```
```
source ./env/bin/activate
```
```
python3 -m pip install django
``` 
```
python3 -m pip install djangorestframework
```
```
pip freeze > requirements.txt
```
```
django-admin startproject project .
manage.py runserver 8001
python3 manage.py createsuperuser
```
```
$ pwd
```

# Django Back-end 🔭

        
## First step :heart: 
                     
 - After creating new folder :  
    - From inside the folder, open the terminal and write the following command to open the folder in vs code  :
        
``` Shell
code .
```   
   
 - How to install a virtual environment (venv) : 
    -  Write the following command in the terminal. :
   
``` Shell
pip3 install virtualenv
```      
           
 - You’ll set up a new virtual environment using your command line. :  
```
python3 -m venv 'the_name_of_virtual_environment'
```  
```                                 
virtualenv  'the_name_of_virtual_environment'   
```       
 - Run or activate virtual enironment :- then install django :- using the following command line: 
```
source ./name_of_virtual_environment/bin/activate                      
```             
 - install django after activating venv :- by using the following command line 
```
           python3 -m pip install django  
```     
 - to update pip :- write the following command line :-
```
          python3 -m pip install --upgrade pip      
```

 - to know version of [python] and [Django] inside venv :- after activating venv :- from following command line:-
```
          python3 --version
          python -m django --version
```        
          
 - if you want to update [Django] or [python] :- from command use :- selection version is optional :-
``` 
pip install --upgrade django ==3.9.5   
```
``` 
sudo apt upgrade python 
```    
 - Pin your dependencies :- write all packages or libraries in requirements.txt :- using line command :-
```
python -m pip freeze > requirements.txt  
```    
         
 - to know libraries which installed on env :-
```
pip freeze
```     
     
  - to save libraries in text file :- another method:=
```
pip freeze > requirements.txt   
```                               
                               
## Next step ❤️ 
                      
 - Set up a Django project  or create project of django :-  from command line :- 
```
django-admin startproject  'the name of project '
```
```
django-admin startproject  'the name of project ' . 
```          
           
 - **In order to create an App** , enter the following command in the terminal: 
```   
python3 manage.py startapp  name_of_app    
```          
 - After create app : add App in [settings] in [INSTALLED_APPS]  
   
 - should inside folder which contain file(manage.py) then :- write the following 2 commands
```
python manage.py migrate
pythin manage.py runserver   
```       
  - if you want change port :- write any port from 8000 to 8999 :- for example
```
python3 manage.py runserver 8001  
```       
   
 - To deactivate virtual environment :- write the following commend in terminal :- 
```
deactivate
```         
 - to install rest framework :- write in command :- 
```
pip install djangorestframework      
```
 - after constructing admin ,model , urls ,serializer ,views for apps :- write the two commands :- 
```
python manage.py makemigrations 
python manage.py migrate 
```       
 - to create super user :- 
```
python manage.py createsuperuser
```
   
 