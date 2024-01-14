### How to build and run the system
You can use Docker to run the project in the context of Postgres, or just run it using your own computer environment (it will fall back to the SQLite database).

- With Docker container (it will automatically build and run the system)
```sh
docker compose up --build
```

- Raw system environment
```sh
pip install -r requirements.txt
python manager.py runserver server
```

### Extra steps
You will also need a superuser to access the dashboard. There are two commands to update some choice data, one for "Grupos de Serviço" and another for "Estabelecimentos"
```sh
python manager.py createsuperuser
python manager.py update_grupos
python manager.py update_estabelecimentos
```

You can use the default login page to log in to the superuser account. Have a good time!
