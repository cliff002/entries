from flask import Flask, render_template, request, redirect
import os
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# Connect to the database
conn = sqlite3.connect('entries.db', check_same_thread=False)
cursor = conn.cursor()

# Create the table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS entries (
        id INTEGER PRIMARY KEY,
        identifier TEXT,
        param1 TEXT,
        param2 TEXT,
        param3 TEXT,
        param4 TEXT,
        param5 TEXT,
        param6 TEXT
    )
''')

@app.route('/send', methods=['POST'])
def send():
    param1 = request.form['param1']
    param2 = request.form['param2']
    param3 = request.form['param3']
    param4 = request.form['param4']
    param5 = request.form['param5']
    param6 = request.form['param6']

    # Compose the email body
    body = f'The following information was entered: \n\n param1: {param1} \n param2: {param2} \n param3: {param3} \n param4: {param4} \n param5: {param5} \n param6: {param6}'

    # Use the operating system's built-in email client to send the email
    os.system(f'echo "{body}" | mail -s "Information entered" something@mail.com')
    
    # Save the information to the database
    cursor.execute('''
        INSERT INTO entries (identifier, param1, param2, param3, param4, param5, param6)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', ('rp-'+str(cursor.lastrowid+1),param1, param2, param3, param4, param5, param6))
    conn.commit()

    return redirect('/')

@app.route('/entry', methods=['GET', 'POST'])
def entry():
    if request.method == 'POST':
        identifier = request.form.get('search_identifier')
        if not identifier.startswith('rp-'):
            identifier = 'rp-' + identifier
        cursor.execute('''SELECT * FROM entries WHERE identifier=?''', (identifier,))
        entry = cursor.fetchone()
    else:
        entry = None
    return render_template('entries.html', entry=entry)

@app.route('/search', methods=['POST'])
def search():
    identifier = request.form.get('search_identifier')
    if not identifier.startswith('rp-'):
        identifier = 'rp-' + identifier
    cursor.execute('''SELECT * FROM entries WHERE identifier=?''', (identifier,))
    entry = cursor.fetchone()
    if entry:
        return redirect(url_for('entry', identifier=identifier))
    else:
        return 'No entry found with that identifier'

if __name__ == '__main__':
    app.run(debug=True)
