# modules/user_symptoms/repository.py
from typing import Optional, List, Dict

# --- Helpers ---
_ORDER_SQL = {
    "date_desc": "su.date DESC, su.id DESC",
    "date_asc":  "su.date ASC, su.id ASC",
    "id_desc":   "su.id DESC",
    "id_asc":    "su.id ASC",
}

def _linha_para_dict(row) -> Dict:
    return {
        "id":           row[0],
        "user_id":      row[1],
        "symptom_id":   row[2],
        "symptom_name": row[3],
        "pain_level":   row[4],
        "date":         row[5],
        "notes":        row[6],
    }

# --- Catálogo ---
def existe_sintoma(conn, symptom_id: int) -> bool:
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM symptoms WHERE id = ?", (symptom_id,))
    return cur.fetchone() is not None

# --- Create ---
def insere_usuario_sintoma(conn, user_id: int, symptom_id: int, pain_level: int, date: str, notes: Optional[str]) -> int:
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO symptoms_user (user_id, symptom_id, pain_level, date, notes)
        VALUES (?, ?, ?, ?, ?)
        """,
        (user_id, symptom_id, pain_level, date, notes),
    )
    conn.commit()
    return cur.lastrowid

# --- Read one ---
def busca_usuario_sintoma_por_id(conn, user_id: int, record_id: int) -> Optional[Dict]:
    cur = conn.cursor()
    cur.execute(
        """
        SELECT su.id, su.user_id, su.symptom_id, s.type AS symptom_name,
               su.pain_level, su.date, su.notes, su.created_at, su.updated_at
        FROM symptoms_user su
        JOIN symptoms s ON s.id = su.symptom_id
        WHERE su.user_id = ? AND su.id = ?
        LIMIT 1
        """,
        (user_id, record_id),
    )
    row = cur.fetchone()
    return _linha_para_dict(row) if row else None

# --- List ---
def lista_usuario_sintomas(conn, user_id: int, query) -> List[Dict]:
    sql = [
        """
        SELECT su.id, su.user_id, su.symptom_id, s.type AS symptom_name,
               su.pain_level, su.date, su.notes, su.created_at, su.updated_at
        FROM symptoms_user su
        JOIN symptoms s ON s.id = su.symptom_id
        WHERE su.user_id = ?
        """
    ]
    params = [user_id]

    if getattr(query, "symptom_id", None) is not None:
        sql.append("AND su.symptom_id = ?")
        params.append(query.symptom_id)

    data_ini = getattr(query, "date_from", None) or getattr(query, "date_ini", None)
    data_fim = getattr(query, "date_to", None) or getattr(query, "date_fim", None)

    if data_ini:
        sql.append("AND su.date >= ?")
        params.append(data_ini)
    if data_fim:
        sql.append("AND su.date <= ?")
        params.append(data_fim)

    ordem = getattr(query, "order", "date_desc")
    sql.append("ORDER BY " + _ORDER_SQL.get(ordem, _ORDER_SQL["date_desc"]))

    pagina = int(getattr(query, "page", 1) or 1)
    limite = int(getattr(query, "page_size", 0) or 0)
    if limite > 0:
        offset = (pagina - 1) * limite
        sql.append("LIMIT ? OFFSET ?")
        params.extend([limite, offset])

    cur = conn.cursor()
    cur.execute(" ".join(sql), tuple(params))
    rows = cur.fetchall()
    return [_linha_para_dict(r) for r in rows]

def conta_usuario_sintomas(conn, user_id: int, query) -> int:
    sql = ["SELECT COUNT(*) FROM symptoms_user su WHERE su.user_id = ?"]
    params = [user_id]

    if getattr(query, "symptom_id", None) is not None:
        sql.append("AND su.symptom_id = ?")
        params.append(query.symptom_id)

    data_ini = getattr(query, "date_from", None) or getattr(query, "date_ini", None)
    data_fim = getattr(query, "date_to", None) or getattr(query, "date_fim", None)

    if data_ini:
        sql.append("AND su.date >= ?")
        params.append(data_ini)
    if data_fim:
        sql.append("AND su.date <= ?")
        params.append(data_fim)

    cur = conn.cursor()
    cur.execute(" ".join(sql), tuple(params))
    return cur.fetchone()[0]

# --- Update ---
def atualiza_usuario_sintoma(conn, user_id: int, record_id: int, body: dict) -> Optional[Dict]:
    sets = []
    params = []

    if body.get("pain_level") is not None:
        sets.append("pain_level = ?")
        params.append(body["pain_level"])
    if body.get("date") is not None:
        sets.append("date = ?")
        params.append(body["date"])
    if body.get("notes") is not None:
        sets.append("notes = ?")
        params.append(body["notes"])

    if not sets:
        return None

    params.extend([user_id, record_id])
    cur = conn.cursor()
    cur.execute(
        f"""
        UPDATE symptoms_user
        SET {", ".join(sets)}
        WHERE user_id = ? AND id = ?
        """,
        tuple(params),
    )
    conn.commit()
    if cur.rowcount == 0:
        return None

    cur.execute(
        """
        SELECT su.id, su.user_id, su.symptom_id, s.type AS symptom_name,
               su.pain_level, su.date, su.notes, su.created_at, su.updated_at
        FROM symptoms_user su
        JOIN symptoms s ON s.id = su.symptom_id
        WHERE su.user_id = ? AND su.id = ?
        """,
        (user_id, record_id),
    )
    row = cur.fetchone()
    return _linha_para_dict(row) if row else None

def deleta_usuario_sintoma(conn, user_id: int, symptom_id: int) -> bool:
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM symptoms_user WHERE user_id = ? AND id = ?",
        (user_id, symptom_id),
    )
    conn.commit()
    return cur.rowcount > 0