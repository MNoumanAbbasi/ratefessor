import sqlite3


def get_prof_details(prof_id):
    """
    Returns the details of the professor in same order as DB.
    """
    cursor = sqlite3.connect('./db.sqlite3').cursor()
    cursor.execute("SELECT * FROM professor WHERE prof_id = ?;", (prof_id))
    return cursor.fetchone()

def get_course_info(course_name):
    """
    Returns the course details using course_name
    """
    cursor = sqlite3.connect('./db.sqlite3').cursor()
    cursor.execute("SELECT * FROM course WHERE course_name = ?;", (course_name,))
    return cursor.fetchone()

def get_profs_of_course(course_name):
    """
    Returns all the professors that offered that course
    """
    cursor = sqlite3.connect('./db.sqlite3').cursor()
    cursor.execute("SELECT * FROM prof_sec WHERE course_name = ?;", (course_name,))
    professors = []
    for row in cursor.fetchall():
        prof_id = row[0]
        cursor.execute("SELECT * FROM professor WHERE prof_id = ?;", (prof_id,))
        r = cursor.fetchone()
        if r:
            professors.append({'id': r[0], 'name': r[1], 'position': r[2], 'dept_name': r[3]})
    return professors

def get_courses_of_prof(prof_id):
    """
    Returns all the courses offered by professor.
    """
    cursor = sqlite3.connect('./db.sqlite3').cursor()
    cursor.execute("SELECT * FROM prof_sec WHERE prof_id = ?;", (prof_id,))
    courses = [{'name': r[1], 'semester': r[2], 'year': r[3]}
               for r in cursor.fetchall()]
    return courses

def get_reviews_ratings(prof_id=None, course_name=None):
    """
    Fetches the reviews and ratings with given constraint prof_id and course_name.
    A missing constraint is not added to the query.
    For example, for review of a course just supply course_name.
    For a course offer, supply both prof_id and course_name.
    Also returns average stats for ratings.
    """
    # Fetching course from DB
    conn = sqlite3.connect('./db.sqlite3')
    cursor = conn.cursor()
    if prof_id and course_name:
        cursor.execute("SELECT * FROM review NATURAL JOIN rating WHERE prof_id = ? AND course_name = ? ORDER BY date DESC;",
                       (prof_id, course_name,))
    elif prof_id:
        cursor.execute("SELECT * FROM review NATURAL JOIN rating WHERE prof_id = ? ORDER BY date DESC;", (prof_id,))
    else:
        cursor.execute("SELECT * FROM review NATURAL JOIN rating WHERE course_name = ? ORDER BY date DESC;", (course_name,))
    rows = cursor.fetchall()

    reviews = [{'review_id': r[0], 'user_id':r[1], 'text':r[2], 'date':r[3], 'semester':r[6], 'year':r[7],
                'workload':r[8], 'learning':r[9], 'grading':r[10]} for r in rows]

    avgs = {}
    if reviews:
        avgs = {
            'workload': round(sum(r['workload'] for r in reviews) / len(reviews), 1),
            'learning': round(sum(r['learning'] for r in reviews) / len(reviews), 1),
            'grading': round(sum(r['grading'] for r in reviews) / len(reviews), 1)
        }
        avgs['overall'] = round(sum(avg for avg in avgs.values()) / len(avgs), 1)

    return reviews, avgs
