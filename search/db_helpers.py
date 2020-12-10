import sqlite3

def get_prof(prof_identifier):
    """
    Returns all professors that match the identifier entered in the query
    """
    #Fetching professor from DB acc to query
    conn = sqlite3.connect('./db.sqlite3')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM professor WHERE name LIKE ?;", (f'%{prof_identifier}%',))
    return cursor.fetchall()

def get_course(course_identifier):
    """
    Returns all courses that match the identifier entered in the query
    """
    #Fetching professor from course acc to query - checks for substring
    conn = sqlite3.connect('./db.sqlite3')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM course WHERE course_name LIKE ?", (f'%{course_identifier}%',))
    return cursor.fetchall()

def get_prof_course_comb(identifier):
    """
    Returns all instructor and/or courses matching a certain query - made for the combo page
    """
    #Query DB according to the comb_query
    conn = sqlite3.connect('./db.sqlite3')
    cursor = conn.cursor()
    #Getting all the instructor + course pairs matching the query
    cursor.execute("""SELECT professor.prof_id, professor.name, prof_sec.course_name, course.level
                        FROM prof_sec 
                        INNER JOIN professor ON prof_sec.prof_id=professor.prof_id 
                        LEFT JOIN course ON course.course_name = prof_sec.course_name
                        WHERE professor.name LIKE ? OR prof_sec.course_name LIKE ?;"""
                    , (f'%{identifier}%', f'%{identifier}%',))
    return cursor.fetchall()

def get_ratings(prof_id, course_name):
    """
    Returns rating of a particular course+instructor tuple
    """
    conn = sqlite3.connect('./db.sqlite3')
    cursor = conn.cursor()
    cursor.execute("""SELECT rating.workload, rating.learning, rating.grading
                            FROM review
                            INNER JOIN rating ON review.review_id = rating.review_id
                            WHERE review.prof_id = ? AND course_name = ?""", (prof_id, course_name))
    return cursor.fetchall()