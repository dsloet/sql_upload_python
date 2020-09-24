import pymssql
import pandas as pd


class UploadToSQL:
    """Uploading CSV-files to ms sql
    """

    def __init__(self):
        """initialisation using pymssql to connect to your server
        """
        # Example dict, update where necessary
        self.sql_dict = {"object": "VARCHAR(254)",
                         "int64": "INT",
                         "float64": "FLOAT"}

        serverip = "localhost"
        port = "1433"
        user = "SA"
        pwd = "Password1!"
        db = "heroes"
        server = serverip + ":" + port
        self.conn = pymssql.connect(
            server=server, user=user, password=pwd, database=db, as_dict=True
        )
        self.cursor = self.conn.cursor()

    def create_sql_table(self, table_name: str):
        """Creates the table
        First, use the load_csv method. That will create the col_names
        and col_types needed for table creation.

        PARAMETERS:
        -----------
        table_name: str
            Name of the table to be created in the database.

        """
        self.table_name = table_name
        main_string = self._create_main_string()
        full_string = f"CREATE TABLE {self.table_name} ({main_string})"
        print(full_string)
        self.cursor.execute(full_string)
        print(f"Successfully created {table_name}")

    def drop_sql_table(self, table_name: str):
        """Deletes existing table in the database.

        PARAMETERS:
        -----------
        table_name: str
            Name of the table to be deleted

        """
        query = f"DROP TABLE {table_name}"
        self.cursor.execute(query)
        self.conn.commit()
        print(f"Dropped table {table_name}")

    def _one_row_csv_to_sql(self):
        """TEST Uploads CSV

        Use this method to test your upload. It only uploads the
        first row of your CSV file.

        """
        # single row:
        list_to_string = str(list(self.df.iloc[0].values))
        list_to_string = list_to_string.replace("[", "").replace("]", "")
        query = f"INSERT into {self.table_name} VALUES ({list_to_string})"
        print(query)
        self.cursor.execute(query)
        self.conn.commit()
        print(f"Successfully loaded 1 row to table {self.table_name}")

    def csv_file_to_sql(self):
        """Full CSV file upload.
        Upload the full CSV file to the sql database.

        """
        n = len(self.df)
        for i in range(n):
            list_to_string = str(list(self.df.iloc[i].values))
            list_to_string = list_to_string.replace("[", "").replace("]", "")
            query = f"INSERT into {self.table_name} VALUES ({list_to_string})"
            self.cursor.execute(query)
            self.conn.commit()
        print("CSV file uploaded")

    def _create_main_string(self):
        """Helper function to create the main string.

        """
        li = []
        n = range(len(self.col_names))
        for i in n:
            x = f"{self.col_names[i]} {self.col_types[i]},"
            li.append(x)
        return " ".join(li)

    def load_csv(self, csv_file: str):
        """Load the CSV into a pandas dataframe
        Method that loads the data and extracts the necessary
        meta-data for the SQL upload.

        PARAMETERS:
        -----------
        csv_file: str
            Path to your csv file.

        """
        self.df = pd.read_csv(csv_file)
        self.col_names = self.df.columns
        self.col_types = [self.sql_dict[str(x)] for x in self.df.dtypes]
        self.mapping = [self.col_names, self.col_types]
