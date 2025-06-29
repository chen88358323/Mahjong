from torrentool.api import Torrent
import zipfile
from pathlib import Path
import os
import shutil
import time
import logging
import traceback

from torrentool.exceptions import BencodeDecodingError
from torrent_download_files_check import DownLoadCheck
import mysqlTemplate as dbtool  # Assuming this is used elsewhere

# Configure logging
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger(__name__)

TORR_ERROR_DIRNAME = 'errorbak'
HALF_NAME_PREFIX = 'HALF-'
LOG_PATH = 'D:\\temp\\0555\\'  # Consider making this configurable

ARRAY_OF_FILES_TO_REMOVE = ['【01axg.xyz】.jpg', '02AXG.XYZ.png', '03axg.XYZ.png', '8axg.xyz.png',
                            'duplicatedirtyData.txt']
XUNLEI_SUFFIX = '.bt.xltd'
FDM_SUFFIX = '.fdmdownload'
BTCOMET_SUFFIX = '.bc!'


def remove_files(filepath: str) -> None:
    """Removes specific files from a directory and its subdirectories."""
    filepath = Path(filepath).resolve()
    for file_path in filepath.rglob("*"):
        if file_path.name in ARRAY_OF_FILES_TO_REMOVE:
            try:
                logger.info(f"Removing file: {file_path}")
                os.remove(file_path)
            except OSError as e:
                logger.error(f"Error removing file: {file_path}, error: {e}")


def find_duplicate_files(filepath: str, duplicate_suffix: str = '(1).jpg') -> None:
    """Logs paths of files with a specific duplicate suffix."""

    filepath = Path(filepath).resolve()
    for file_path in filepath.rglob("*"):
        if str(file_path).endswith(duplicate_suffix):
            logger.info(f"Duplicate file: {file_path}")


def find_torrents_by_string(search_strings: list[str] | None, search_path: str) -> list[str]:
    """Finds torrent files containing any of the given search strings in their file names.

    Args:
        search_strings: A list of strings to search for.
        search_path: The path to search in.

    Returns:
        A list of paths to the matching torrent files.
    """

    found_torrents = []
    if not search_strings:
        return found_torrents

    search_path = Path(search_path).resolve()
    for search_string in search_strings:
        logger.info(f"Starting search for: '{search_string}'")
        for file_path in search_path.rglob("*.torrent"):
            try:
                torrent = load_torrent(str(file_path))
                if torrent:
                    for torrent_file in torrent.files:
                        if torrent_file.name.startswith(search_string):
                            logger.info(f"Found torrent: {file_path}")
                            found_torrents.append(str(file_path))
                            break  # Found a match, no need to check other files in this torrent
            except Exception as e:
                logger.error(f"Error processing torrent file: {file_path}, error: {e}\n{traceback.format_exc()}")
        logger.info(f"Finished search for: '{search_string}'")
    return found_torrents


def load_torrent(torrent_path: str) -> Torrent | None:
    """Loads a torrent file. Handles potential decoding errors.

    Args:
        torrent_path: The path to the torrent file.

    Returns:
        A Torrent object if successful, None otherwise.
    """
    torrent_path = Path(torrent_path).resolve()
    try:
        return Torrent.from_file(str(torrent_path))
    except BencodeDecodingError as e:
        logger.error(f"BencodeDecodingError: {torrent_path}, error: {e}")
        return None
    except IndexError as e:
        logger.error(f"IndexError: {torrent_path}, error: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error loading torrent: {torrent_path}, error: {e}\n{traceback.format_exc()}")
        return None


def load_torrent_and_fix(torrent_path: str, error_count: int) -> Torrent | None:
    """Loads a torrent file, attempting to fix it if necessary.

    Args:
        torrent_path: The path to the torrent file.
        error_count: The number of previous errors encountered.

    Returns:
        A Torrent object if successful, None otherwise.
    """

    torrent_path = Path(torrent_path).resolve()
    try:
        return Torrent.from_file(str(torrent_path))
    except BencodeDecodingError:
        error_count += 1
        logger.info(f"BencodeDecodingError: {torrent_path}")
        if error_count < 2 and os.path.getsize(torrent_path) > 1024:
            return fix_and_load_torrent(torrent_path)
        else:
            return None
    except IndexError:
        logger.info(f"IndexError: {torrent_path}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error loading torrent: {torrent_path}, error: {e}\n{traceback.format_exc()}")
        return None


def fix_and_load_torrent(torrent_file_path: str) -> Torrent | None:
    """Fixes a torrent file and then loads it.

    Args:
        torrent_file_path: The path to the torrent file.

    Returns:
        A Torrent object if successful, None otherwise.
    """
    fix_torrent(torrent_file_path)
    return load_torrent(torrent_file_path)


def get_error_paths(full_path: str) -> tuple[str, Path, Path]:
    """Extracts filename, error backup path, and parent directory from a full file path.

    Args:
        full_path: The full path to the file.

    Returns:
        A tuple containing the filename, the error backup path, and the parent directory path.
    """

    file_path = Path(full_path).resolve()
    file_name = file_path.name
    error_path = file_path.parent / TORR_ERROR_DIRNAME
    return file_name, error_path, file_path.parent


def get_torrent_details(file_path: str, search_string: str) -> list[str]:
    """Finds torrent files in a directory that contain a specific string.

    Args:
        file_path: The path to search in.
        search_string: The string to search for.

    Returns:
        A list of paths to the matching torrent files.
    """

    matching_torrents = []
    file_path = Path(file_path).resolve()

    for sub_path in file_path.rglob("*.torrent"):
        try:
            torrent = load_torrent(str(sub_path))
            if torrent:
                for torrent_file in torrent.files:
                    if torrent_file.name.startswith(search_string):
                        logger.info(f"Found torrent: {sub_path}")
                        matching_torrents.append(str(sub_path))
                        break  # Found a match, move to next torrent
        except Exception as e:
            logger.error(f"Error processing {sub_path}: {e}\n{traceback.format_exc()}")
    return matching_torrents


def edit_xunlei_files(file_path: str, suffix_to_remove: str = XUNLEI_SUFFIX) -> None:
    """Removes a specific suffix from filenames in a directory.

    Args:
        file_path: The path to the directory.
        suffix_to_remove: The suffix to remove from the filenames.
    """

    file_path = Path(file_path).resolve()
    for sub_path in file_path.rglob("*"):
        if sub_path.is_file() and str(sub_path).endswith(suffix_to_remove):
            new_file_path = sub_path.with_name(sub_path.stem)  # Use with_name
            try:
                logger.info(f"Renaming: {sub_path} to {new_file_path}")
                os.rename(sub_path, new_file_path)
            except OSError as e:
                logger.error(f"Error renaming {sub_path}: {e}")


def clear_download_artifacts(file_path: str, suffixes_to_remove: tuple[str, ...] = (
        XUNLEI_SUFFIX, FDM_SUFFIX, BTCOMET_SUFFIX)) -> None:
    """Removes files with specific suffixes from a directory and its subdirectories.

    Args:
        file_path: The path to the directory.
        suffixes_to_remove: A tuple of suffixes to remove.
    """

    file_path = Path(file_path).resolve()
    for sub_path in file_path.rglob("*"):
        if sub_path.is_file() and str(sub_path).endswith(suffixes_to_remove):
            try:
                logger.info(f"Removing file: {sub_path}")
                os.remove(sub_path)
            except OSError as e:
                logger.error(f"Error removing {sub_path}: {e}")
            except UnicodeEncodeError as e:
                logger.error(f"UnicodeEncodeError removing {sub_path}: {e}")


def write_torrent_details_to_files(file_path: str) -> None:
    """Writes details of torrent files in subdirectories to text files.

    Args:
        file_path: The main directory path.
    """

    main_path = Path(file_path).resolve()
    for sub_dir_path in [d for d in main_path.iterdir() if d.is_dir()]:
        logger.info(f"Processing directory: {sub_dir_path}")
        write_torrent_detail(str(sub_dir_path))


def filter_big_torrent_files(torrent_path: str, size_threshold_gb: float) -> list[str]:
    """Filters large torrent files and moves them to a 'big' subdirectory.

    Args:
        torrent_path: The path to the directory containing torrent files.
        size_threshold_gb: The size threshold in gigabytes.

    Returns:
        A list of names of the moved torrents.
    """

    torrent_path = Path(torrent_path).resolve()
    big_torrent_dir = torrent_path / 'big'
    big_torrent_dir.mkdir(parents=True, exist_ok=True)

    size_threshold_bytes = int(size_threshold_gb * 1024 * 1024)
    big_files = []

    for file_path in torrent_path.rglob("*.torrent"):
        try:
            torrent = load_torrent(str(file_path))
            if not torrent:
                continue
            file_size = torrent.total_size
            if file_size > size_threshold_bytes:
                shutil.move(str(file_path), str(big_torrent_dir / file_path.name))
                logger.info(f"Moved large torrent: {file_path.name}")
                big_files.append(torrent.name)
        except Exception as e:
            logger.error(f"Error processing {file_path}: {e}\n{traceback.format_exc()}")

    logger.info(f"Moved {len(big_files)} large torrent files.")
    logger.info(f"Moved torrent names: {big_files}")
    return big_files


def move_pdf_if_exists(torrent_file_path: str, target_directory: str) -> None:
    """Moves a PDF file associated with a torrent if it exists.

    Args:
        torrent_file_path: The path to the torrent file.
        target_directory: The directory to move the PDF to.
    """

    pdf_path = torrent_name_to_pdf_path(torrent_file_path)
    if pdf_path and Path(pdf_path).is_file():
        try:
            target_path = Path(target_directory)
            target_path.mkdir(parents=True, exist_ok=True)
            shutil.move(pdf_path, str(target_path / Path(pdf_path).name))
            logger.info(f"Moved PDF: {pdf_path} to {target_directory}")
        except OSError as e:
            logger.error(f"Error moving PDF: {pdf_path}, error: {e}")


def torrent_name_to_pdf_path(torrent_file_path: str) -> str | None:
    """Converts a torrent file path to its corresponding PDF path.

    Args:
        torrent_file_path: The path to the torrent file.

    Returns:
        The path to the PDF file, or None if the input is None.
    """

    if not torrent_file_path:
        return None
    return str(Path(torrent_file_path).with_suffix('.pdf'))


def filter_downloaded_files(torrent_dir_path: str, download_dir_path: str, target_sub_dir_name: str) -> None:
    """Filters and moves downloaded files based on torrent files.

    Args:
        torrent_dir_path: Path to the directory containing torrent files.
        download_dir_path: Path to the directory containing downloaded files.
        target_sub_dir_name: Name of the subdirectory to move files to.
    """

    torrent_dir_path = Path(torrent_dir_path).resolve()
    download_dir_path = Path(download_dir_path).resolve()

    downloaded_dirs = {d.name: d for d in download_dir_path.iterdir() if d.is_dir()}
    torrent_dict = generate_torrent_dict(torrent_dir_path)
    matching_dirs = set(downloaded_dirs.keys()) & set(torrent_dict.keys())

    torrent_done_path = torrent_dir_path / target_sub_dir_name
    torrent_done_path.mkdir(parents=True, exist_ok=True)

    finished_file_path = download_dir_path / target_sub_dir_name
    finished_file_path.mkdir(parents=True, exist_ok=True)

    for dir_name in matching_dirs:
        logger.info("Processing matched directory: %s", dir_name)
        new_torrent_file = torrent_done_path / Path(torrent_dict[dir_name]).name
        finished_file = finished_file_path / dir_name

        if new_torrent_file.is_file():
            logger.error("Duplicate download detected for: %s", dir_name)
            logger.error("Torrent file: %s", new_torrent_file)
            logger.error("Downloaded file/dir: %s, Target: %s", downloaded_dirs[dir_name], finished_file)
            try:
                os.remove(torrent_dict[dir_name])
            except OSError as e:
                logger.error(f"Error removing torrent file: {torrent_dict[dir_name]}, error: {e}")
        else:
            try:
                shutil.move(torrent_dict[dir_name], new_torrent_file)
                logger.debug("Moved torrent from %s to %s", torrent_dict[dir_name], new_torrent_file)
            except OSError as e:
                logger.error(f"Error moving torrent file: {torrent_dict[dir_name]}, error: {e}")

        if finished_file.exists():
            finished_file = finished_file.with_name(f"{finished_file.name}_new")  # Avoid overwrite
            finished_file.mkdir(parents=True, exist_ok=True)  # Ensure dir exists if needed

        try:
            shutil.move(str(downloaded_dirs[dir_name]), str(finished_file))
            logger.debug("Moved downloaded from %s to %s", downloaded_dirs[dir_name], finished_file)
        except OSError as e:
            logger.error(f"Error moving downloaded data: {downloaded_dirs[dir_name]}, error: {e}")

        move_pdf_if_exists(torrent_dict[dir_name], str(finished_file))

    logger.info("Moved %d sets of files.", len(matching_dirs))


def count_file_sizes(torrent_dir_path: str, download_dir_path: str) -> None:
    """Counts and logs the sizes of downloaded files compared to torrent information.

    Args:
        torrent_dir_path: Path to the directory containing torrent files.
        download_dir_path: Path to the directory containing downloaded files.
    """

    downloaded_files = {
        filename: calculate_size(Path(os.path.join(download_dir_path, filename)))
        for filename in os.listdir(download_dir_path)
    }
    torrent_dict = generate_torrent_dict(Path(