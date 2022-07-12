# Stuyspec DB migration scripts 

The python scripts used to migrate the [Stuyvesant Spectator](https://github.com/stuyspec)'s old databse to the rewrite's database. 


## Run Locally

Clone the project

```bash
  git clone https://github.com/leomet07/stuyspec_db_migrate_scripts
```

Go to the project directory

```bash
  cd stuyspec_db_migrate_scripts
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Run any one of the scripts!

For example, to migrate the staff table (from a staff.json file), run the following:

```bash
  python migrate_staff.py
```


## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`MONGODB_URI` - A mongoDB connection URI


