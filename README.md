# Website of online games
Project is built on Python(Django)

## There are: 
### Criss cross game(BETA)
You chose a room and wished sign X or O, then tell your friend your room due which they could join .

### Drawing battle(BETA)
There is a big canvas where everyone could remain one's picture. There are several main colors: 
red, green, blue and black. Also one could erase all drawings.

### Drawing sandbox
You have one minute to draw your picture and after that time the picture will be downloaded on your PC.

## Ranking
There is ranking system among players. Winning in some game adds score to you.

## How to launch?
+ Make virtual environment and activate it
```python
python3 -m venv name_of_your_env && source name_of_your_env/bin/activate
```

+ Install all dependencies
```python
pip install -r requirements.txt
```

+ Launching the application
```python
python manage.py runserver
```