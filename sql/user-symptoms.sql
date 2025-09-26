CREATE TABLE IF NOT EXISTS symptoms_user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  symptom_id INTEGER NOT NULL,
  pain_level INTEGER NOT NULL,
  date TEXT NOT NULL,
  notes TEXT,
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at TEXT NOT NULL DEFAULT (datetime('now')),
  FOREIGN KEY (symptom_id) REFERENCES symptoms(id)
);