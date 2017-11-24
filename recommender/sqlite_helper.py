import sqlite3

class SQLiteHelper(object):




   def item_in_context(self, item, context):
       sql = "select count(*) from ratings where item_id=%s and time=%s" % (item, context)
       db = sqlite3.connect("data.sqlite")
       cursor = db.cursor()
       cursor.execute(sql) 
       res = cursor.fetchone()[0]
       return res

if __name__=='__main__':
    sqlite = SQLiteHelper()
    print(sqlite.item_in_context(60,53))
    print(sqlite.item_in_context(60,5))


