import sqlite3
import numpy as np

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

def get_cards(prof_course_list):
    """
    Returns the card view given a filtered list of instructor+course tuples
    """
    #for each pair - get the ratings if any 
    if (len(prof_course_list) == 0): return [] 
    else:
        comb_list = []
        for row in prof_course_list:
            #getting the ratings
            rating_tuple = get_ratings(row[0], row[2])
            if len(rating_tuple) != 0:
                ratings = np.array(rating_tuple)
                print(ratings)
                cum_ratings = np.round(np.mean(ratings, axis = 0, dtype = np.float64), 2)
            else:
                cum_ratings = [-1]
            print(cum_ratings)
            comb_list.append({'prof_id': row[0], 'prof_name': row[1], 'course_name': row[2], 'level': row[3], 'ratings': cum_ratings})

        return comb_list

def filter_acc_level(level):
    """
    Returns records filtered according to level ONLY
    """
    conn = sqlite3.connect('./db.sqlite3')
    cursor = conn.cursor()
    cursor.execute("""SELECT professor.prof_id, professor.name, prof_sec.course_name, course.level
                        FROM prof_sec 
                        INNER JOIN professor ON prof_sec.prof_id=professor.prof_id 
                        LEFT JOIN course ON course.course_name = prof_sec.course_name
                        WHERE course.level = ?;""", (level,))
    return cursor.fetchall()

def filter_acc_ratings(rating_list):
    """
    Returns records filtered according to ratings ONLY
    """
    conn = sqlite3.connect('./db.sqlite3')
    cursor = conn.cursor()
    cursor.execute("""SELECT professor.prof_id, professor.name, prof_sec.course_name, course.level
                        FROM prof_sec 
                        INNER JOIN professor ON prof_sec.prof_id=professor.prof_id 
                        LEFT JOIN course ON course.course_name = prof_sec.course_name
                        WHERE (professor.prof_id, prof_sec.course_name) IN (SELECT prof_id, course_name 
                                                                                FROM review 
                                                                                INNER JOIN rating ON review.review_id = rating.review_id
                                                                                GROUP BY prof_id
                                                                                HAVING (AVG(workload) BETWEEN ? AND ?) AND (AVG(learning) BETWEEN ? AND ?) AND (AVG(grading) BETWEEN ? AND ?));"""
                                                                                , (float(rating_list[0]), float(rating_list[1]), float(rating_list[2]), float(rating_list[3]), float(rating_list[4]), float(rating_list[5]),))
    return cursor.fetchall()

def filter_acc_level_ratings(level, rating_list):
    """
    Returns records filtered according to ratings and level ONLY
    """
    conn = sqlite3.connect('./db.sqlite3')
    cursor = conn.cursor()
    cursor.execute("""SELECT professor.prof_id, professor.name, prof_sec.course_name, course.level
                        FROM prof_sec 
                        INNER JOIN professor ON prof_sec.prof_id=professor.prof_id 
                        LEFT JOIN course ON course.course_name = prof_sec.course_name
                        WHERE course.level = ? AND (professor.prof_id, prof_sec.course_name) IN (SELECT prof_id, course_name 
                                                                                FROM review 
                                                                                INNER JOIN rating ON review.review_id = rating.review_id
                                                                                GROUP BY prof_id
                                                                                HAVING (AVG(workload) BETWEEN ? AND ?) AND (AVG(learning) BETWEEN ? AND ?) AND (AVG(grading) BETWEEN ? AND ?));"""
    , (level, float(rating_list[0]), float(rating_list[1]), float(rating_list[2]), float(rating_list[3]), float(rating_list[4]), float(rating_list[5]),))
    return cursor.fetchall()

def filter_acc_prof_course_ratings(identifier, rating_list):
    """
    Returns records filtered according to prof/course and ratings ONLY
    """
    conn = sqlite3.connect('./db.sqlite3')
    cursor = conn.cursor()
    cursor.execute("""SELECT professor.prof_id, professor.name, prof_sec.course_name, course.level
                        FROM prof_sec 
                        INNER JOIN professor ON prof_sec.prof_id=professor.prof_id 
                        LEFT JOIN course ON course.course_name = prof_sec.course_name
                        WHERE (professor.name LIKE ? OR prof_sec.course_name LIKE ?) AND (professor.prof_id, prof_sec.course_name) IN (SELECT prof_id, course_name 
                                                                                FROM review 
                                                                                INNER JOIN rating ON review.review_id = rating.review_id
                                                                                GROUP BY prof_id
                                                                                HAVING (AVG(workload) BETWEEN ? AND ?) AND (AVG(learning) BETWEEN ? AND ?) AND (AVG(grading) BETWEEN ? AND ?));"""
    , (f'%{identifier}%', f'%{identifier}%', float(rating_list[0]), float(rating_list[1]), float(rating_list[2]), float(rating_list[3]), float(rating_list[4]), float(rating_list[5]),))
    return cursor.fetchall()

def filter_acc_prof_course_level(identifier, level):
    """
    Returns records filtered according to prof/course and level ONLY
    """
    conn = sqlite3.connect('./db.sqlite3')
    cursor = conn.cursor()
    cursor.execute("""SELECT professor.prof_id, professor.name, prof_sec.course_name, course.level
                        FROM prof_sec 
                        INNER JOIN professor ON prof_sec.prof_id=professor.prof_id 
                        LEFT JOIN course ON course.course_name = prof_sec.course_name
                        WHERE professor.name LIKE ? OR prof_sec.course_name LIKE ? AND course.level = ?;"""
                    , (f'%{identifier}%', f'%{identifier}%', level))
    return cursor.fetchall()

def filter_acc_all(identifier, level, rating_list):
    """
    Returns records filtered according to prof/course, level and ratings
    """
    conn = sqlite3.connect('./db.sqlite3')
    cursor = conn.cursor()
    cursor.execute("""SELECT professor.prof_id, professor.name, prof_sec.course_name, course.level
                        FROM prof_sec 
                        INNER JOIN professor ON prof_sec.prof_id=professor.prof_id 
                        LEFT JOIN course ON course.course_name = prof_sec.course_name
                        WHERE professor.name LIKE ? OR prof_sec.course_name LIKE ? AND course.level = ? AND (professor.prof_id, prof_sec.course_name) IN (SELECT prof_id, course_name 
                                                                                FROM review 
                                                                                INNER JOIN rating ON review.review_id = rating.review_id
                                                                                GROUP BY prof_id
                                                                                HAVING (AVG(workload) BETWEEN ? AND ?) AND (AVG(learning) BETWEEN ? AND ?) AND (AVG(grading) BETWEEN ? AND ?));"""
                    , (f'%{identifier}%', f'%{identifier}%', level, float(rating_list[0]), float(rating_list[1]), float(rating_list[2]), float(rating_list[3]), float(rating_list[4]), float(rating_list[5]),))
    return cursor.fetchall()