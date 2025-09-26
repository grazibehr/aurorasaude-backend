from data_base import get_conn

def get_sintomas():
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, type FROM symptoms ORDER BY type ASC")
        rows = cur.fetchall()
        
        return [{"id": r[0], "type": r[1]} for r in rows]
