### This file is weirdly named to avoid 'class' as a filename

class Class:
    """
    Represents a class at Carleton University.
    """

    def __init__(crn, faculty, course_no, description, prereqs):
        """
        Initializes a Class object.
        Parameters:
        crn: int,
        faculty: str, The associated faculty code, i.e. "COMP"
        """
        self.crn = crn
        self.term = term
        self.faculty = faculty
        self.course_no = course_no
        self.description = description
        self.prereqs = prereqs
