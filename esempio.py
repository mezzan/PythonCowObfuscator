import sys, getopt
import os
import re

""" commento su una linea """
def getStudentID(fileName):
    print("=============")
    print(fileName)
    student=re.match('VR[0-9][0-9][0-9][0-9][0-9][0-9]',fileName)
    print(student.group(0))
    print("=============")


def parseFolder(dir):
    """ commento
        su
        piu
        linee
    """
    for top, dirs, files in os.walk(dir):
        for nm in files:
            with open(os.path.join(top, nm)) as fileOpened:
                getStudentID(nm)




def main(argv):
    if len(argv) == 0:
        print("Error: invalid use.")
        print("studentsList.py -d <inputdir>")
        sys.exit(2)

    try:
        opt, arg = getopt.getopt(argv, "d", ["idir="])
    except getopt.GetoptError:
        print("Error: invalid use.")
        print("studentsList.py -d <inputdir>")
        sys.exit(2)

    parseFolder(str(arg[0]))

if __name__ == "__main__":
    main(sys.argv[1:])
