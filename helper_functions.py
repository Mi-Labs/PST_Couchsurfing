import os


def check_file_exists(file_path):
    """
    Checks if a file exists on that given path
    :param file_path: Path to the file
    :return: True if file exists
    """
    return os.path.isfile(file_path)
