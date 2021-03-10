import sqlite3
import datetime

conn = sqlite3.connect('users.db')
cur = conn.cursor()


def create_table_user():
    cur.execute("""CREATE TABLE IF NOT EXISTS users(
	   	id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
		user_id INTEGER NOT NULL,
		confirmed TEXT DEFAULT 0);
	""")

    conn.commit()


def get_info_payment(user_id):
    result = c.execute(
        f"SELECT * FROM payment_query WHERE user_id=:id", {'id': user_id})
    return result.fetchone()


def confirm_user(user_id):
    check_new_user(user_id)

    cur.execute("UPDATE users SET confirmed = 1 WHERE user_id = :id", {
                'id': user_id})
    conn.commit()


def delete_payment_request(user_id):
    cur.execute(f"DELETE FROM payment_query WHERE user_id = :id",
                {'id': user_id})


def check_new_user(user_id):
    result = cur.execute(
        f"SELECT * FROM users WHERE user_id=:id", {'id': user_id}).fetchone()

    if result is not None:
        return True

    else:
        cur.execute(f"INSERT INTO users VALUES(?, ?, ?)",
                    (None, user_id, False))
        conn.commit()

        return True


def check_user(user_id):

    result = cur.execute(f"SELECT confirmed FROM users WHERE user_id=:id", {
                         'id': user_id}).fetchone()

    if result is not None:
        return bool(int(result[0]))
    else:
        return False


def get_all_clients():
    result = cur.execute(
        f"SELECT user_id FROM users WHERE confirmed=1").fetchall()
    return len(result)


def get_all_users():
    result = cur.execute(
        f"SELECT user_id FROM users WHERE confirmed=0").fetchall()
    return len(result)


if __name__ == '__main__':
    create_table_user()
