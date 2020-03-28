# FAMILY LIBRARY DJANGO REST VUE

This is the first trial for the reimplementation of my Django Family Library web app with a Django REST backend and an integrated Vue.JS template frontend.


## Requirements

- Python >= 3.6
- Django >= 2.2.4
- djangorestframework >= 3.10.2
- django-cors-headers >= 3.2.1
- djangorestframework-jwt >= 1.11.0


## Initialization

From inside the project's folder, and using your virtualenv of choice:

```shell
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

 ## REST Refactoring 
 
1. Initialize:
    - Create the new project: `django-admin startproject family-library-django-rest-vue`
    - Copy over folder for `library` django app
    - Add `library` to `INSTALLED_APPS` in `setting.py`
    - Create this `README` file
    - Install dependencies: `pip install djangorestframework django-filter`
    - Add `rest_framework`, `rest_framework.authtoken`, `django_filters` to `INSTALLED_APPS` in `setting.py`
    - Migrate models: `python manage.py migrate`
2. Creating:
    - Add `library/serializers.py` and create serializer for each model class
    - Create `library/viewsets.py`
    - Create `library/renderers.py` to render model data to JSON
    - In the `/family-library-django-rest-vue/` subfolder:
        - Create `routers.py`
        - In `urls.py` import `routers.py` and include it in `urlpatterns`
3. Test run: `python manage.py runserver`
4. Adapting `views.py`:
    - link up renderer and serializer for each view
    - adapt `urls.py` to new views

## Vue Integration

- Create `library/templates/library/index.html` to hold the Vue app
- Add `vuejs` imports to `index.html`
- Register the new template view in `urls.py`
- Add `Vue` constructor script to template
- Add constructor elements: `delimiter`, `el`, `http`, `methods`, `mounted`
- Create `CRUD` methods for models
- Add function calls to `mounted`






