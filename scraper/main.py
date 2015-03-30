import carleton

import sys

def main(args):
    # Grab the session ID so we can use it later.
    carleton.get_courses('COMP')



if __name__ == '__main__':
    main(sys.argv)
