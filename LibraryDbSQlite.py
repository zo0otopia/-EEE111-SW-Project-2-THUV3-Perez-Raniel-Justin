'''
This is the interface to an SQLite Database
'''

import sqlite3

class LibraryDbSQlite:
    # 'Initialize Database' ---------------------------------------------------------------------------------------------------------
    def __init__(self, dbName='Library_record.db'):
        super().__init__()
        self.dbName = dbName
        self.csvFile = self.dbName.replace('.db', '.csv')
        self.table_name = 'Library'
        self.create_table()
       

    def connect_cursor(self):
        self.conn = sqlite3.connect(self.dbName)
        self.cursor = self.conn.cursor()        

    def commit_close(self):
        self.conn.commit()
        self.conn.close()        

    # 'Create Table for Database' ---------------------------------------------------------------------------------------------------------
    def create_table(self):
        self.connect_cursor()
        self.cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {self.table_name} (
                    Book_ID TEXT PRIMARY KEY,
                    Title TEXT, 
                    Author TEXT,
                    Publisher TEXT,
                    Year TEXT,
                    Genre TEXT,
                    status TEXT)''')
        self.column_names = ['Book_ID','Title', 'Author', 'Publisher', 'Year', 'Genre', 'Status']
        self.commit_close()

    # 'Fetch Records' ---------------------------------------------------------------------------------------------------------
    def fetch_record(self):
        self.connect_cursor()
        self.cursor.execute(f'SELECT * FROM {self.table_name}')
        record =self.cursor.fetchall()
        self.conn.close()
        return record

    # 'Insert Records' ---------------------------------------------------------------------------------------------------------
    def insert_record(self, Book_ID, Title, Author, Publisher, Year, Genre, status):
        self.connect_cursor()
        self.cursor.execute(f'INSERT INTO {self.table_name} (Book_ID, Title, Author, Publisher, Year, Genre, status) VALUES (?, ?, ?, ?, ?, ?, ?)',
                    (Book_ID, Title, Author, Publisher, Year, Genre, status))
        self.commit_close()

    # 'Delete Records' ---------------------------------------------------------------------------------------------------------
    def delete_record(self, Book_ID):
        self.connect_cursor()
        self.cursor.execute(f'DELETE FROM {self.table_name} WHERE Book_ID = ?', (Book_ID,))
        self.commit_close()

    # 'Update Records' ---------------------------------------------------------------------------------------------------------
    def update_record(self, new_Title, new_Author, new_Publisher, new_Year, new_Genre, new_status, Book_ID):
        self.connect_cursor()
        self.cursor.execute(f'UPDATE {self.table_name} SET Title = ?, Author = ?, Publisher = ?, Year = ?, Genre = ?, status = ? WHERE Book_ID = ?',
                    (new_Title, new_Author, new_Publisher, new_Year, new_Genre, new_status, Book_ID))
        self.commit_close()

    # 'ID Exists' ---------------------------------------------------------------------------------------------------------
    def id_exists(self, Book_ID):
        self.connect_cursor()
        self.cursor.execute(f'SELECT COUNT(*) FROM {self.table_name} WHERE Book_ID = ?', (Book_ID,))
        result =self.cursor.fetchone()
        self.conn.close()
        return result[0] > 0

    # 'Export CSV' ---------------------------------------------------------------------------------------------------------
    def export_csv(self):
        with open(self.csvFile, "w") as filehandle:
            filehandle.write('Book ID, Title, Author, Publisher, Year, Genre, Status\n')
            dbEntries = self.fetch_record()
            for entry in dbEntries:
                print(entry)
                filehandle.write(f"{entry[0]},{entry[1]},{entry[2]},{entry[3]},{entry[4]},{entry[5]},{entry[6]}\n")
    
    # 'Import CSV' ---------------------------------------------------------------------------------------------------------
    def import_csv(self, file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
            
            entries = [line.strip().split(',') for line in lines[1:]] if len(lines) > 0 else []

            self.connect_cursor()
            for entry in entries:
                self.cursor.execute(f'INSERT INTO {self.table_name} (Book_ID, Title, Author, Publisher, Year, Genre, status) VALUES (?, ?, ?, ?, ?, ?, ?)', entry)
            self.commit_close()

    # 'Export JSON' ---------------------------------------------------------------------------------------------------------
    import json
    def export_json(self, file_path):
        with open(file_path, "w") as filehandle:
            dbEntries = self.fetch_record()
            json_entries = [{"Book_ID": entry[0], "Title": entry[1], "Author": entry[2], "Publisher": entry[3], "Year": entry[4], "Genre": entry[5], "Status": entry[6]} for entry in dbEntries]
            self.json.dump(json_entries, filehandle, indent=2)

# 'Test Function' ---------------------------------------------------------------------------------------------------------
def test_StudentDb():
    iStudentDb = LibraryDbSQlite(dbName='Library_record.db')

    for entry in range(31):
        iStudentDb.insert_record(f'{entry}ID', f'{entry}Title', f'{entry}Author', f'{entry}Publisher', f'{entry}Year', f'{entry}Genre', 'In Library')

    all_entries = iStudentDb.fetch_record()
    assert len(all_entries) == 31

