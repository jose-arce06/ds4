import sqlite3

DATABASE = 'search_engine.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        # Tabla para las URLs raíz ingresadas en Configuration
        conn.execute('''
            CREATE TABLE IF NOT EXISTS sources (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT UNIQUE NOT NULL,
                status TEXT DEFAULT 'no escrapeada'
            )
        ''')
        # Tabla para guardar los documentos individuales indexados
        conn.execute('''
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_id INTEGER,
                filename TEXT NOT NULL,
                original_url TEXT,
                year INTEGER,
                content TEXT,
                word_count INTEGER,
                FOREIGN KEY (source_id) REFERENCES sources(id)
            )
        ''')
        conn.commit()

init_db()