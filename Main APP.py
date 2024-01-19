from LibraryDbSQlite import LibraryDbSQlite
from LibraryGui import LibraryGui

def main():
    db = LibraryDbSQlite('Library_record.db')
    app = LibraryGui(dataBase=db)
    app.mainloop()

if __name__ == "__main__":
    main()