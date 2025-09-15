import sqlite3

def update_fromID(id, title, content):
    con = sqlite3.connect('banco.db')
    cur = con.execute(
        "UPDATE note SET title = ?, content = ? WHERE id = ?",
        (title, content, id))
    con.commit()
    con.close()