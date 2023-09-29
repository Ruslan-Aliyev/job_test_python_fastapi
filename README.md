# Setup the Database

https://migueldoctor.medium.com/how-to-run-postgresql-pgadmin-in-3-steps-using-docker-d6fe06e47ca1

**Postgresql DB server**

```
docker pull postgres:latest
docker run --name my-own-postgres -e POSTGRES_PASSWORD=postgresmaster -p 5432:5432 -d postgres
```

Check
```
$ docker exec -it my-own-postgres bash
root@02a9356be657:/# psql -h localhost -U postgres
\list
```

**Postgresql client interface**

```
docker pull dpage/pgadmin4:latest
docker run --name my-pgadmin -p 82:80 -e 'PGADMIN_DEFAULT_EMAIL=pg@admin.com' -e 'PGADMIN_DEFAULT_PASSWORD=pgadminpass' -d dpage/pgadmin4
```

Check
```
$ docker ps -a

CONTAINER ID   IMAGE            COMMAND                  CREATED              STATUS              PORTS                         NAMES
705a483c1aba   dpage/pgadmin4   "/entrypoint.sh"         About a minute ago   Up About a minute   443/tcp, 0.0.0.0:82->80/tcp   my-pgadmin
02a9356be657   postgres         "docker-entrypoint.s…"   2 days ago           Up 2 minutes        0.0.0.0:5432->5432/tcp        my-own-postgres
```

Visit:  
http://localhost:82/  
http://localhost:82/login?next=%2F  

Login:  
`pg@admin.com`  
`pgadminpass`  

The first time when you log into PGAdmin, you will be greeted with a dashboard. Under the "Dashboard" tab, "Quick Links" section, click "Add New Server".  

A popup form will appear.   
Under the "General" tab, write something for "Name". I named it "group-one".    
Under the "Connection" tab, provide the IP Address. To know this, run this command `docker inspect {container-name}` (in this case: `docker inspect my-own-postgres`) in the terminal and see the value for `IPAddress`

After this, the left-hand-side menu will have this structure:
```
- Servers
-- group-one
--- Databases
----postgres
...
```

# Python, Poetry, Alembic, FastAPI

Download Python: https://www.python.org/downloads/  
Tick "Add Python to PATH" near the start of the installation wizard.  
Check by: `python --version`

Download Poetry: https://python-poetry.org/docs/#installation  
`(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -`  
Add `%APPDATA%\Python\Scripts` to `PATH` too.   
Check by: `poetry --version`

## Setup Python, Poetry and the simplest FastAPI GET request

https://medium.com/@caetanoog/start-your-first-fastapi-server-with-poetry-in-10-minutes-fef90e9604d9

Run: `uvicorn main:app --reload`   
Visit: http://127.0.0.1:8000  

### Potential problems

**Problem 1:** When running `uvicorn main:app --reload`,   
Error: `.ps1 is not digitally signed. The script will not execute on the system.`  

**Solution:**  
`Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`  
https://caiomsouza.medium.com/fix-for-powershell-script-not-digitally-signed-69f0ed518715  


**Problem 2:** When running `uvicorn main:app --reload`,   
Error: `uvicorn is not recognized as the name of a cmdlet`   

**Solution:**  
Run instead: `python -m uvicorn main:app --reload`    
More specifically, the `python` executable in the virtual environment folder: `C:/Users/ADMIN/AppData/Local/pypoetry/Cache/virtualenvs/uac-q0lvo1HA-py3.11/Scripts/python -m uvicorn main:app --reload`   

**To know the name of the virtual environment:**  
```
poetry env list
uac-q0lvo1HA-py3.11 (Activated)
```

Or:
```
poetry show -v
Using virtualenv: C:\Users\ADMIN\AppData\Local\pypoetry\Cache\virtualenvs\uac-q0lvo1HA-py3.11
```

**To remove an virtual environment:** `poetry env remove uac-q0lvo1HA-py3.11`

## Simple FastAPI CRUDs

https://apidog.com/blog/how-to-quickly-implement-crud-operations-with-fastapi/

## With JWT auth

- https://youtu.be/xZnOoO3ImSY?si=THyasQvQ0qqv_9Bz
  - https://github.com/ianrufus/youtube/tree/main/fastapi-jwt-auth

## With DB

- https://youtu.be/bfelC61XKO4?si=EOCMzQ3q6Tm7I-FB
  - https://github.com/serlesen/backend-flask/tree/chapter_10
- https://medium.com/@estretyakov/the-ultimate-async-setup-fastapi-sqlmodel-alembic-pytest-ae5cdcfed3d4

`Alembic` is a database migrations tool.  
`SQLAlchemy` is an ORM.  
`Alembic` works on top of `SQLAlchemy`.  

```
> poetry add alembic
Using version ^1.12.0 for alembic

Updating dependencies
Resolving dependencies...

...
  • Installing mako (1.2.4)
  • Installing sqlalchemy (2.0.21)
```

Create `alembic.ini`: `alembic init alembic`   
In it, set up the connection string: `sqlalchemy.url = postgresql://${DB_USER}:${DB_PASS}@${DB_HOST}/${DB_NAME}`   

- `DB_USER` and `DB_PASS` are what you setup during the "Postgresql DB server" stage
- `DB_HOST` is `localhost:5432`
  - Note: IP Address is not `0.0.0.0`, nor the IPAddress you got from `docker inspect my-own-postgres`
- `DB_NAME` is `postgres`

Create migration script: `alembic revision -m "create test table"`   
Complete migration file, then run: `alembic upgrade head`   

## ENV file

Better to put sensitive credentials in a env file:
- Generally: https://dev.to/jakewitcher/using-env-files-for-environment-variables-in-python-applications-55a1
- In Alembic: https://github.com/sqlalchemy/alembic/discussions/1149

## SQLAlchemy ORM

- https://codevoweb.com/build-a-crud-app-with-fastapi-and-sqlalchemy
