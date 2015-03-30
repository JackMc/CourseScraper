from carleton.course import Course

import requests
from bs4 import BeautifulSoup

import datetime

FALL = 0
WINTER = 1
SUMMER = 2

# Maps term codes to semesters
# Experimentally determined from playing with Carleton Central.
_TERM_MAP = {WINTER: '10', SUMMER: '20', FALL: '30'}

def make_term_code(year, term):
    # Term is invalid.
    if term not in _TERM_MAP:
        return None

    return str(year) + _TERM_MAP[term]

def get_session_id():
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

def get_courses(faculty, year=2014, term=FALL):
    """
    Returns a list of Course objects for a given faculty code (i.e. COMP).
    """
    # We grab the faculty courses page and soup it. This is a listing of courses.
    faculty_courses = requests.get('http://calendar.carleton.ca/undergrad/courses/' + faculty)
    soup = BeautifulSoup(faculty_courses.text)
    # This variable contains a list of the divs that contain the course info.
    course_divs = soup.find_all('div', attrs={'class': 'courseblock'})

    courses = []

    for div in course_divs:
        strong_block = div.find('strong')
        text = strong_block.text
        top, title = text.split('\n')
        # The first half of this would be the faculty code, which we already have.
        # Also for some reason it likes it when I split on \xa0 instead of space,
        # though it's visaully a space. Probably a weird unicode thing.
        _, course_no = top.split('[')[0].strip().split('\xa0')

        # Another magic number... 3 is the length of both 1.0, 0.5, and 0.0
        credits = float(top.split('[')[1][:3])

        course_additional = div.find('div', attrs={'class': 'coursedescadditional'})
        # Some courses don't have a course additional section (i.e. co-op/COMP3999)
        if course_additional:
