import os

def get_project_root():
    """ Returns the absolute path of the project root directory. """
    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # os.path.dirname multiple times to reach the project root
    project_root = os.path.dirname(os.path.dirname(current_dir))

    return project_root
