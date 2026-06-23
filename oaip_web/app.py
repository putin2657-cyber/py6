from flask import Flask, render_template, request, redirect, url_for, flash, session
from oaip.connect_db import ConnectDB
from oaip.validators import validate_login, validate_password

app = Flask(__name__, static_folder='static')
app.secret_key = 'replace-with-strong-secret'


def get_db():
    db = ConnectDB()
    return db


@app.route('/')
def index():
    return render_template('menu.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form.get('login', '').strip()
        parol = request.form.get('parol', '').strip()

        if not login or not parol:
            flash('Заполните все поля', 'warning')
            return redirect(url_for('login'))

        ok, msg = validate_login(login)
        if not ok:
            flash(msg, 'warning')
            return redirect(url_for('login'))

        ok, msg = validate_password(parol)
        if not ok:
            flash(msg, 'warning')
            return redirect(url_for('login'))

        db = get_db()
        if not db.con:
            flash('Ошибка подключения к базе данных', 'danger')
            return redirect(url_for('login'))

        try:
            db.cur.execute('SELECT id, login FROM user WHERE login = %s AND parol = %s', (login, parol))
            row = db.cur.fetchone()
        except Exception as e:
            flash(f'Ошибка авторизации: {e}', 'danger')
            db.close()
            return redirect(url_for('login'))

        db.close()
        if row:
            session['user'] = {'id': row[0], 'login': row[1]}
            flash('Вы авторизовались', 'success')
            return redirect(url_for('users'))
        else:
            flash('Неверный логин или пароль', 'warning')
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        login = request.form.get('login', '').strip()
        parol = request.form.get('parol', '').strip()

        if not login or not parol:
            flash('Заполните все поля', 'warning')
            return redirect(url_for('register'))

        ok, msg = validate_login(login)
        if not ok:
            flash(msg, 'warning')
            return redirect(url_for('register'))

        ok, msg = validate_password(parol)
        if not ok:
            flash(msg, 'warning')
            return redirect(url_for('register'))

        db = get_db()
        if not db.con:
            flash('Ошибка подключения к базе данных', 'danger')
            return redirect(url_for('register'))

        try:
            db.cur.execute('SELECT id FROM user WHERE login = %s', (login,))
            exists = db.cur.fetchone()
            if exists:
                flash('Такой пользователь уже есть', 'warning')
            else:
                db.cur.execute('INSERT INTO user (login, parol) VALUES (%s, %s)', (login, parol))
                db.con.commit()
                flash('Вы зарегистрированы', 'success')
                return redirect(url_for('login'))
        except Exception as e:
            db.con.rollback()
            flash(f'Ошибка регистрации: {e}', 'danger')
        finally:
            db.close()

    return render_template('register.html')


def require_login(func):
    from functools import wraps

    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user' not in session:
            flash('Требуется авторизация', 'warning')
            return redirect(url_for('login'))
        return func(*args, **kwargs)

    return wrapper


@app.route('/users')
@require_login
def users():
    db = get_db()
    try:
        db.cur.execute('SELECT id, login, parol FROM user ORDER BY id')
        rows = db.cur.fetchall()
    except Exception as e:
        flash(f'Ошибка получения списка: {e}', 'danger')
        rows = []
    finally:
        db.close()
    return render_template('users.html', users=rows, current=session.get('user'))


@app.route('/users/delete/<int:user_id>', methods=['POST'])
@require_login
def delete_user(user_id):
    db = get_db()
    try:
        db.cur.execute('DELETE FROM user WHERE id = %s', (user_id,))
        db.con.commit()
        flash('Пользователь удален', 'success')
    except Exception as e:
        db.con.rollback()
        flash(f'Ошибка удаления: {e}', 'danger')
    finally:
        db.close()
    return redirect(url_for('users'))


@app.route('/users/edit/<int:user_id>', methods=['GET', 'POST'])
@require_login
def edit_user(user_id):
    db = get_db()
    if request.method == 'POST':
        new_login = request.form.get('login', '').strip()
        new_parol = request.form.get('parol', '').strip()

        ok, msg = validate_login(new_login)
        if not ok:
            flash(msg, 'warning')
            return redirect(url_for('edit_user', user_id=user_id))
        ok, msg = validate_password(new_parol)
        if not ok:
            flash(msg, 'warning')
            return redirect(url_for('edit_user', user_id=user_id))

        try:
            db.cur.execute('UPDATE user SET login = %s, parol = %s WHERE id = %s', (new_login, new_parol, user_id))
            db.con.commit()
            flash('Данные обновлены', 'success')
            return redirect(url_for('users'))
        except Exception as e:
            db.con.rollback()
            flash(f'Ошибка обновления: {e}', 'danger')
        finally:
            db.close()

    try:
        db.cur.execute('SELECT id, login, parol FROM user WHERE id = %s', (user_id,))
        row = db.cur.fetchone()
    except Exception as e:
        flash(f'Ошибка: {e}', 'danger')
        db.close()
        return redirect(url_for('users'))
    db.close()
    if not row:
        flash('Пользователь не найден', 'warning')
        return redirect(url_for('users'))
    return render_template('edit.html', user=row)


@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Вы вышли', 'info')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)

