import sqlite3

DB = 'store.db'

def updateReorder():
    try:
        conn = sqlite3.connect(DB)
        cursor = conn.cursor()
        
        cursor.execute("SELECT pro_id FROM Products")
        pro_ids = [item[0] for item in cursor.fetchall()]
        reorder_status = 'False'

        for i in range(len(pro_ids)):
            pro_id = pro_ids[i]
            cursor.execute("UPDATE Products SET reorder_point = ? WHERE pro_id = ?", (reorder_status, pro_id))
            
        conn.commit()
        conn.close()

    except sqlite3.Error as e:
        print("Error accessing database", e)

def main():
    updateReorder()

if __name__ == "__main__":
    main()
