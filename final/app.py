from flask import Flask, render_template, request, redirect, session, url_for, flash
import sqlite3
from passlib.hash import pbkdf2_sha256

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def get_db_connection():
    conn = sqlite3.connect('music_database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Hash the password
        hashed_password = hash_password(password)
        
        # Check if username already exists
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
            existing_user = cursor.fetchone()
        
        if existing_user:
            return 'Username already exists. Please choose a different username.'
        
        # Store username and hashed password in the database
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
            conn.commit()
        
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Retrieve the hashed password from the database
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
            hashed_password = cursor.fetchone()
        
        if hashed_password and verify_password(password, hashed_password[0]):
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return 'Invalid username or password'
    
    return render_template('login.html')

def hash_password(password):
    # Hash the password using PBKDF2
    return pbkdf2_sha256.hash(password)

def verify_password(plain_password, hashed_password):
    # Check if the provided password matches the hashed password
    return pbkdf2_sha256.verify(plain_password, hashed_password)

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        username = session['username']
        # Fetch songs from the database for the logged-in user
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT s.id, s.title, s.artist, s.url 
                FROM songs s
                JOIN users u ON s.user_id = u.id
                WHERE u.username = ?
            ''', (username,))
            songs = cursor.fetchall()
        message = "You have not added any songs yet!" if not songs else ""
        return render_template('dashboard.html', username=username, songs=songs, message=message)
    return redirect(url_for('login'))

@app.route('/add-song', methods=['POST'])
def add_song():
    if 'username' in session:
        title = request.form['title']
        artist = request.form['artist']
        url = request.form['url']
        username = session['username']
        
        # Proceed to add the song to the database
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO songs (title, artist, url, user_id) VALUES (?, ?, ?, (SELECT id FROM users WHERE username = ?))',
                           (title, artist, url, username))
            conn.commit()
        return redirect(url_for('dashboard'))

@app.route('/delete-song/<int:song_id>')
def delete_song(song_id):
    if 'username' in session:
        # Delete the song from the database
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM songs WHERE id = ?', (song_id,))
            conn.commit()
        return redirect(url_for('dashboard'))

@app.route('/search', methods=['GET', 'POST'])
def search():
    if 'username' in session:
        username = session['username']
        query = request.form.get('query')
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT s.id, s.title, s.artist, s.url 
                FROM songs s
                JOIN users u ON s.user_id = u.id
                WHERE u.username = ? AND (s.title LIKE ? OR s.artist LIKE ?)
            ''', (username, f'%{query}%', f'%{query}%'))
            songs = cursor.fetchall()
        message = "No results found!" if not songs else ""
        return render_template('dashboard.html', username=username, songs=songs, message=message)
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'username' in session:
        if request.method == 'POST':
            new_username = request.form['new_username']
            new_password = request.form['new_password']
            
            # Hash the new password
            hashed_password = hash_password(new_password)
            
            username = session['username']
            # Update username and password in the database
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('UPDATE users SET username = ?, password = ? WHERE username = ?', (new_username, hashed_password, username))
                conn.commit()
            
            session['username'] = new_username
            return redirect(url_for('dashboard'))
        
        return render_template('profile.html', username=session['username'])
    
    return redirect(url_for('login'))

@app.route('/change-username', methods=['POST'])
def change_username():
    if 'username' in session:
        new_username = request.form['new_username']
        username = session['username']
        
        # Check if the new username already exists
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE username = ?', (new_username,))
            existing_user = cursor.fetchone()
        
        if existing_user:
            flash('Username already exists. Please choose a different username.', 'error')
            return redirect(url_for('profile'))
        
        # Update the username in the database
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET username = ? WHERE username = ?', (new_username, username))
            conn.commit()
        
        session['username'] = new_username
        flash('Username successfully updated', 'success')
        return redirect(url_for('profile'))
    return redirect(url_for('login'))


@app.route('/change-password', methods=['POST'])
def change_password():
    if 'username' in session:
        new_password = request.form['new_password']
        username = session['username']
        
        # Hash the new password
        hashed_password = hash_password(new_password)
        
        # Update the password in the database
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET password = ? WHERE username = ?', (hashed_password, username))
            conn.commit()
        
        flash('Password successfully updated', 'success')
        return redirect(url_for('profile'))
    return redirect(url_for('login'))

@app.route('/delete-profile', methods=['POST'])
def delete_profile():
    if 'username' in session:
        username = session['username']
        password = request.form['password']
        
        # Retrieve the hashed password from the database
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
            hashed_password = cursor.fetchone()
        
        # Verify the provided password
        if hashed_password and verify_password(password, hashed_password['password']):
            # Delete the user from the database
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM users WHERE username = ?', (username,))
                conn.commit()
            
            # Clear session data
            session.pop('username', None)

            flash('Your profile has been successfully deleted.', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid password. Profile not deleted.', 'error')
            return redirect(url_for('profile'))
    else:
        flash('You must be logged in to delete your profile.', 'error')
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)