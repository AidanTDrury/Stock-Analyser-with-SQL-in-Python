import pyodbc 
cnxn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                      "Server=localhost;"
                      "Database=Quant;"
                      "Trusted_Connection=yes;")


cursor = cnxn.cursor()
