### This file is weirdly named to avoid 'class' as a filename

class Course:
    """
    Represents a class at Carleton University.
    """

    def __init__(self, credits, faculty, course_no, title, description, course_prereqs, text_prereqs, preclusions, extra_info):
        """
        Initializes a Class object.
        All self-explanetory, except prereqs. It is a list of strings representing
        the prerequisites to take this course.
        """
        self.credits = credits
        self.faculty = faculty
        self.course_no = course_no
        self.title = title
        self.description = description
        self.course_prereqs = course_prereqs
        # Text prereqs are actually on the graph
        self.text_prereqs = text_prereqs
        self.preclusions = preclusions
        self.extra_info = extra_info
    def __str__(self):
        return faculty + " " + course_no
