import mysql.connector

class db:
    mydb = None
    
    @staticmethod
    def connect():
        if not db.mydb:
            db.mydb = mysql.connector.connect(
                host="82.157.251.139",
                user="win",
                password="123-09qwe",
                database="cspj"
            )
        print("connected")
