## Tech Times

[![Actions Status](https://github.com/behnambm/tech-times/workflows/Tech%20Times%20CI/badge.svg
)](https://github.com/behnambm/tech-times/actions)


> Tech Times is an open-source blogging web application written in Python and Django where users can read and write articles about Tech.
>
> Additionally, this is my graduation project for 2021.

Tech Times like NYTimes 😜


### Visit live version
https://behnambm.pythonanywhere.com

### How to run locally 
```
git clone https://github.com/behnambm/tech-times.git
cd tech-times
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
mv .env.sample .env  # change the variables and set the proper values
python manage.py migrate
python manage.py collectstatic
python manage.py createsuperuser  # this is optional, and used to access admin panel in django 
python manage.py runserver
and finally go to: http://127.0.0.1:8000
```

<details>
<summary>More detail</summary>

- CI: Github Actions
- Hosting: PythonAnywhere
- Database: MySql
- SMTP provider: Google Mail
</details> 