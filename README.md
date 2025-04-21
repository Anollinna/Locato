# Locato 
**Locato** is a platform for travelers and explorers that allows users to:
- discover interesting locations around the world,
- share their own favorite places,
- leave reviews and view ratings from others,
- save places they'd like to visit in the future.

## Test User Credentials

You can log in with the following test account to explore the app:
```text
Username: PieGas
Password: 121748pie
```
## Technologies Used

- Python 3.13
- Django 5.x
- SQLite
- Pillow — image processing 

## How to Run the Project Locally

### 1.Create and activate a virtual environment:
```text
python -m venv venv
source venv/bin/activate       # On Windows: venv\Scripts\activate
```
### 2.Install dependencies:
```text
pip install -r requirements.txt
```
Make sure that Pillow is included in requirements.txt. If not, run:
```text
pip install Pillow
pip freeze > requirements.txt
```
### 3.Apply database migrations:
```text
python manage.py migrate
```
### 4.Load fixtures
- Countries data:
```text
python manage.py loaddata countries.json
```
- Initial content:
```text
python manage.py loaddata data.json
```

### 5.Run the development server:
```text
python manage.py runserver
```
### 6.Open in your browser:
```text
http://127.0.0.1:8000/
```
