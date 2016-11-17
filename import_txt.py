import csv
import sqlite3
import glob
import os

def do_directory(dirname, db):
  for filename in glob.glob(os.path.join(dirname, '*.txt')):
    do_file(filename, db)

def do_file(filename, db):
  with open(filename) as f:
    with db:
      data = csv.DictReader(f)
      cols = data.fieldnames
      table=os.path.splitext(os.path.basename(filename))[0]

      sql = 'drop table if exists "{}"'.format(table)
      db.execute(sql)
      
      sql = 'create table "{table}" ( {cols} )'.format(
        table=table,
        cols=','.join('"{}"'.format(col) for col in cols))
      db.execute(sql)
      
      sql = 'insert into "{table}" values ( {vals} )'.format(
        table=table,
        vals=','.join('?' for col in cols))
      db.executemany(sql, (list(map(row.get, cols)) for row in data))

if __name__ == '__main__':
  database_file = '.\collarDB.db'
  txt_directory = 'M:\DatabaseTables'
  conn = sqlite3.connect(database_file)
  do_directory(txt_directory, conn)