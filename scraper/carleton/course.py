### This file is weirdly named to avoid 'class' as a filename

class Course:
    """
    Represents a class at Carleton University.
    """

    def __init__(credits, faculty, course_no, title, description, prereqs, preclusions, extra_info):
        """
        Initializes a Class object.
        All self-explanetory, except prereqs. It is a list of strings representing
        the prerequisites to take this course.
        """
        self.credits = credits
        self.term = term
        self.faculty = faculty
        self.course_no = course_no
        self.title = title
        self.description = description
        self.prereqs = prereqs
        self.preclusions = preclusions
        self.extra_info = extra_info
