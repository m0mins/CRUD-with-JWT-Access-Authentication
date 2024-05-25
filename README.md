# Create
1. Create a virtual environment with python 3.10.12
2. Create .env with the same configuration of settings and given database requirements name

# Activation
1. Activate your virtual environment

# Run
1. pip install -r requirements.txt
2. python manage.py makemigrations taskApp(app name)
3. python manage.py migrate
4. python manage.py runserver

# How it Works and What inside it 
1. Set the Role(is_super,is_admin,is_staff,is_user) in User Role Table by hard coded
2. Create a Super User and update it's role id
3. Every User will be registered as a user
4. Here has been added JWT Token for Authentication
4. Only Super user able to update user role
5. Super user able to do everything  (create,update,delete,details) of TODO task
6. Admin also can everything of TODO task except Delete
7. Staff able to do update and details of TODO task
8. Others user only can Read the tasks
9. Here has been added pagination
10. When someone trying to see the list of tasks , of course has to provide page and limit in params
11. Database Migration Script
12. And Also have sql query to convert postgresql data to json data format