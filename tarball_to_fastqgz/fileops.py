import tarfile
from itertools import repeat
from typing import Any, Dict, Union

import mgzip
from numpy import iterable


def find_targets_from_tar(tar_file: str, target_file_list: list = []) -> dict:
    """
    Given a list of file names of interest, search the contents of the tar file
    to get the corresponding tar record names.

    Target files not found in the tar_file will have a value of 'None' in the
    returned dictionary.
    """
    # initialize targets dict with None values for tar paths
    targets: Dict[str, Union[None, str]] = dict(
        zip(target_file_list, repeat(None, len(target_file_list)))
    )
    with tarfile.open(tar_file, "r") as tar:
        for tarinfo in tar:
            # save tar path for desired files
            basename = tarinfo.name.split('/')[-1]
            if basename in targets.keys():
                targets[basename] = tarinfo.name
    return targets


def from_tar_to_dest(
    tar_file: str, tar_member: str, destination: str, compress_dest: bool = False
) -> None:
    """
    Extract tar_member from tar_file and write the contents to destination.
    """

    with tarfile.open(tar_file, "r") as tar:
        content = tar.extractfile(tar_member)
        if compress_dest:
            write_to_gzip_file(content, destination)
        else:
            write_to_plain_file(content, destination)


def write_to_plain_file(content: iterable, destination: str) -> None:
    """
    Write content to plain file
    """
    with open(destination, 'wb') as destfile:
        for blob in content:
            destfile.write(blob)


def write_to_gzip_file(content: iterable, destination: str) -> None:
    """
    Write content to gzipped file
    """

    with mgzip.open(destination, 'wb', thread=12) as destfile:
        for blob in content:
            destfile.write(blob)
