# sql_upload_python
Small piece of code to upload CSVs to ms-sql sqlserver

## Build the SQL server

Pull the docker container from microsoft

```shell
$ docker pull mcr.microsoft.com/mssql/server:latest
```

Run the image:

```shell
$ docker run \
-e 'ACCEPT_EULA=Y' \
-e 'SA_PASSWORD=Password1!' \
-e 'MSSQL_PID=Express' \
--name sqlserver \
-p 1433:1433 -d mcr.microsoft.com/mssql/server:latest
```

Find the server's IP address

```shell
$ docker inspect sqlserver --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $INSTANCE_ID
```

Use this IP address in the csvupload.py file under \_\_init\_\_

### Enter the docker

Enter the terminal of the container
```shell
$ docker exec -it sqlserver "bash"
```
enter the database:
```shell
$ /opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P "Password1!" -d heroes
```

From here you can perform your regular SQL queries.

# Use UploadToSQL()

in the init of the class you will find the details needed to setup a connection. Edit this to adjust your situation.

```Python
serverip = "localhost"
port = "1433"
user = "SA"
pwd = "Password1!"
db = "heroes"
```

After you have set this up you can simple use:

```Python
# create an object
loader = UploadToSQL()

# load the csv
loader.load_csv("test_data/test.csv")

# drop if the table already exists
loader.drop_sql_table("test_csv")

# Create the table
loader.create_sql_table("test_csv")

# Upload the CSV
loader.csv_file_to_sql()
```