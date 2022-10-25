from views.menu import Menu
 
if __name__ == '__main__':
    import sys
    import os
    PROJECT_CWD = f"{os.sep}".join(os.getcwd().split(os.sep))
    sys.path.append(os.path.join(PROJECT_CWD,"views"))