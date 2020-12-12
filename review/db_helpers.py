import sqlite3
from datetime import datetime


def add_review(user_id, course_name, prof_id, review):
    """
    Accepts user_id, course_name, and review object and inserts
    the review into DB.
    Note: If review by user already exists, overwrites the exisitng
    review.

    user_id : user who posted the review  
    course_name : name of course 
    prof_id : id of professor that offered course
    review : dictionary of review data including ratings 
    """
    with sqlite3.connect('./db.sqlite3') as conn:
        cursor = conn.cursor()
        semester = review['semester']
        year = review['year']
        workload = review['workload']
        learning = review['learning']
        grading = review['grading']
        review = review['text']

        date = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')

        # First check if review by this user already exists
        cursor.execute("SELECT review_id FROM review WHERE user_id = ? AND prof_id = ? AND course_name = ?",
                       (user_id, prof_id, course_name))
        r = cursor.fetchone()

        # If yes, update the exisitng review
        # Else insert new review and rating tuples
        if r:
            review_id = r[0]
            cursor.execute("UPDATE review SET text = ?, date = ?, semester = ?, year = ? WHERE review_id = ?",
                           (review, date, semester, year, review_id))
            cursor.execute("UPDATE rating SET workload = ?, learning = ?, grading = ? WHERE review_id = ?",
                           (workload, learning, grading, review_id))
        else:
            cursor.execute("INSERT INTO review (user_id,text,date,prof_id,course_name,semester,year) VALUES (?,?,?,?,?,?,?)",
                           (user_id, review, date, prof_id, course_name, semester, year))
            review_id = cursor.lastrowid
            cursor.execute("INSERT INTO rating VALUES (?,?,?,?)", (review_id, workload, learning, grading))
        conn.commit()
        cursor.close()


def get_user_review(user_id, prof_id, course_name):
    """
    Fetches the user review from DB if exists.
    Otherwise returns None.
    """
    cursor = sqlite3.connect('./db.sqlite3').cursor()
    cursor.execute("SELECT * FROM review NATURAL JOIN rating WHERE user_id = ? AND prof_id = ? AND course_name = ?;",
                   (user_id, prof_id, course_name,))
    r = cursor.fetchone()
    user_review = {}
    if r:
        user_review = {'review_id': r[0], 'user_id': r[1], 'text': r[2], 'date': r[3], 'semester': r[6], 'year': r[7],
                       'workload': r[8], 'learning': r[9], 'grading': r[10]}
    return user_review


def delete_review(review_id, user_id):
    """
    Deletes the review only if user_id also matches.
    """
    with sqlite3.connect('./db.sqlite3') as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")  # turning on delete cascade so rating gets removed too
        cursor.execute("DELETE FROM review WHERE review_id = ? AND user_id = ?;", (review_id, user_id))
        conn.commit()
        cursor.close()
