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
    Returns an string used by Carleton Central to uniquely identify a session.
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
    # Grab the session ID.
    session_id = get_session_id()
    # Generate the term code (this is how Central encodes terms with years)
    term_code = make_term_code(year, term)

    if not (term_code and session_id):
        # Propogate the error
        return None

    # Don't know if this is needed, but make it think we did all the post requests
    requests.post('http://central.carleton.ca/prod/bwysched.p_search_fields',
                  data={'wsea_code': 'EXT', 'term_code': term_code, 'session_id': session_id})

    post_params = {
        'wsea_code': 'EXT',
        'term_code': term_code,
        'session_id': session_id,
        'ws_numb': '',
        'sel_aud': 'dummy',
        'sel_subj': ['dummy', faculty],
        'sel_camp': 'dummy',
        'sel_sess': ['dummy', ''],
        'sel_attr': 'dummy',
        'sel_levl': ['dummy', ''],
        'sel_schd': ['dummy', ''],
        'sel_insm': 'dummy',
        'sel_link': 'dummy',
        'sel_wait': 'dummy',
        'sel_day': ['dummy', 'm', 't', 'w', 'r', 'f', 's', 'u'],
        'sel_begin_hh': ['dummy', '0'],
        'sel_begin_mi': ['dummy', '0'],
        'sel_begin_am_pm': ['dummy', 'a'],
        'sel_end_hh': ['dummy', '0'],
        'sel_end_mi': ['dummy', '0'],
        'sel_end_am_pm': ['dummy', 'a'],
        'sel_instruct': ['dummy', ''],
        'sel_special': ['dummy', 'N'],
        'sel_resd': 'dummy',
        'sel_breadth': 'dummy',
        'sel_number': '',
        'sel_crn': '',
        'block_button': ''
    }

    search_results = requests.post('http://central.carleton.ca/prod/bwysched.p_course_search',
                                    data=post_params)

    if search_results.ok:
        
