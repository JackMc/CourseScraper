from carleton.course import Course

import requests
from bs4 import BeautifulSoup

import datetime
import csv

FALL = 0
WINTER = 1
SUMMER = 2

# Maps term codes to semesters
# Experimentally determined from playing with Carleton Central.
_TERM_MAP = {WINTER: '10', SUMMER: '20', FALL: '30'}

def _make_term_code(year, term):
    # Term is invalid.
    if term not in _TERM_MAP:
        return None

    return str(year) + _TERM_MAP[term]

def _get_session_id():
    """
    Returns a string used by Carleton Central to uniquely identify a session.
    """
    get_session_id = requests.get('http://central.carleton.ca/prod/bwysched.p_select_term',
                                  params={'wsea_code': 'EXT'})

    if not get_session_id.ok:
        # It didn't return a good response code.
        return None

    # Parse out the session ID.
    session_soup = BeautifulSoup(get_session_id.text)
    inputs = session_soup.find('input', attrs={'name': 'session_id'})
    return inputs['value']

def _parse_row(row):
    """
    Returns a two-tuple containing the parsed version of a given row.
    The first tuple will contain all 
    """
    if not row:
        return (None, None)
    elif 'DNI' in row:
        return (None, None)

    return ([eval(x) for x in row if x.startswith('[')], [x[1:] for x in row if x.startswith('\'')])

def get_courses(faculty, year=2014, term=FALL):
    """
    Returns a list of Course objects for a given faculty code (i.e. COMP).
    """
    # We grab the faculty courses page and soup it. This is a listing of courses.
    faculty_courses = requests.get('http://calendar.carleton.ca/undergrad/courses/' + faculty)
    soup = BeautifulSoup(faculty_courses.text)
    # This variable contains a list of the divs that contain the course info.
    course_divs = soup.find_all('div', attrs={'class': 'courseblock'})

    courses = {}

    # Open up the courses/prereqs file
    reader = csv.reader(open(faculty + '_prereqs.csv', 'r+'))

    for div, row in zip(course_divs, reader):
        strong_block = div.find('strong')
        text = strong_block.text
        top, title = text.split('\n')
        # The first half of this would be the faculty code, which we already have.
        # Also for some reason it likes it when I split on \xa0 instead of space,
        # though it's visaully a space. Probably a weird unicode thing.
        _, course_no = top.split('[')[0].strip().split('\xa0')

        # Another magic number... 3 is the length of both 1.0, 0.5, and 0.0
        credits = float(top.split('[')[1][:3])

        description = str(div.string)

        prereqs, text_prereqs = _parse_row(row)

        if prereqs is None or text_prereqs is None:
            continue

        additional = div.find('coursedescadditional')

        courses[faculty + course_no] = Course(credits, faculty, course_no, title, description, prereqs, text_prereqs,
                                              None, additional.get_text() if additional else None)
    return courses

