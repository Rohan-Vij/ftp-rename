"""FTP processing utilities."""
import os


def search_names(item_id, file_names):
    """
    Search for a file with the given item id type.

    :param item_id: the item id
    :param file_names: a list of file names

    :returns: the matching file names if found, None otherwise
    """

    return [name for name in file_names if name.startswith(item_id)]


def delete_files(ftp, dir_path):
    """
    Delete all files in the current directory.
    Used for testing purposes.

    :param sftp: the sftp connection
    :param dir_path: the directory path
    """

    remote_path = "/" + dir_path + "/" if dir_path else ""
    files_in_remote_artifacts = os.listdir(remote_path)
    for file in files_in_remote_artifacts:
        ftp.remove(os.path.join(remote_path, file))

    return "OK"


def get_files(ftp, dir_path):
    """
    Get all files in the given directory.

    :param sftp: the sftp connection
    :param dir_path: the directory path

    :returns: a list of file names
    """

    return [file for file in ftp.listdir(dir_path)
            if ftp.path.isfile(ftp.path.join(dir_path, file))]
