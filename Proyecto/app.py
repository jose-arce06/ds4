from flask import Flask, render_template, request, redirect, jsonify
from database import get_db
import scrapper_engine
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    with get_db() as conn:
        total_docs_row = conn.execute('SELECT COUNT(*) as total FROM documents').fetchone()
        total_docs = dict(total_docs_row)['total'] if total_docs_row else 0
        total_words_row = conn.execute('SELECT SUM(word_count) as total FROM documents').fetchone()
        total_words = dict(total_words_row)['total'] if total_words_row and total_words_row['total'] is not None else 0
        docs_by_year = conn.execute('SELECT year, COUNT(*) as qty FROM documents GROUP BY year ORDER BY year DESC').fetchall()
    return render_template('home.html', total_docs=total_docs, total_words=total_words, docs_by_year=docs_by_year) 


@app.route('/api/stats')
def api_stats():
    with get_db() as conn:
        total_docs = conn.execute('SELECT COUNT(*) FROM documents').fetchone()
    return jsonify(total_docs=total_docs)
@app.route('/scrapper')
def scrapper():
    with get_db() as conn:
        sources = conn.execute('SELECT * FROM sources').fetchall()
        docs_by_source = {}
        for source in sources:
            docs = conn.execute('SELECT filename FROM documents WHERE source_id = ?', (source['id'],)).fetchall()
            docs_by_source[source['id']] = [d['filename'] for d in docs]
    return render_template('scrapper.html', sources=sources, docs_by_source=docs_by_source)

@app.route('/scrapper/run/<int:source_id>', methods=['POST'])
def run_scrapper(source_id):
    with get_db() as conn:
        source = conn.execute('SELECT * FROM sources WHERE id = ?', (source_id,)).fetchone()
    if source:
        scrapper_engine.ejecutar_scraping_url(source['id'], source['url'])
    return redirect('/scrapper')

@app.route('/configuration', methods=['GET', 'POST'])
def configuration():
    with get_db() as conn:
        if request.method == 'POST':
            url = request.form.get('url', '').strip()
            if url:
                try:
                    conn.execute('INSERT INTO sources (url) VALUES (?)', (url,))
                    conn.commit()
                except:
                    pass  
            return redirect('/configuration')
        sources = conn.execute('SELECT url FROM sources').fetchall()
    return render_template('configuration.html', sources=sources)

@app.route('/search')
def search():
    query = request.args.get('q', '').strip()
    threshold = float(request.args.get('threshold', 0.0))
    results = []
    if query:
        with get_db() as conn:
            documents = conn.execute('SELECT original_url, content FROM documents').fetchall()
        for doc in documents:
            content = doc['content'] or ""
            bloques = [b.strip() for b in content.split('\n') if len(b.strip()) > 3]
            for bloque in bloques:
                similitud = scrapper_engine.calcular_similitud_levenshtein(query, bloque)
                if similitud >= threshold:
                    results.append({
                        'url': doc['original_url'],
                        'block': bloque,
                        'similarity': similitud
                    })
        results = sorted(results, key=lambda x: x['similarity'], reverse=True)
    return render_template('search.html', query=query, threshold=threshold, results=results)

if __name__ == '__main__':
    app.run(debug=True)