import tarfile
from itertools import chain, filterfalse, repeat

import mgzip


def find_targets_from_tar(tar_file=None, target_file_list=[]) -> dict:
    """
    Given a list of file names of interest, search the contents of the tar file
    to get the corresponding tar record names.

    Target files not found in the tar_file will have a value of 'None' in the
    returned dictionary.
    """
    # initialize targets dict with None values for tar paths
    targets = dict(zip(target_file_list, repeat(None, len(target_file_list))))
    with tarfile.open(tar_file, "r") as tar:
        for tarinfo in tar:
            # save tar path for desired files
            basename = tarinfo.name.split('/')[-1]
            if basename in targets.keys():
                targets[basename] = tarinfo.name
    return targets


def from_tar_to_dest(
    tar_file=None, tar_member=None, destination=None, compress_dest=False
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


def write_to_plain_file(content, destination):
    """
    Write content to plain file
    """
    with open(destination, 'wb') as destfile:
        for blob in content:
            destfile.write(blob)


def write_to_gzip_file(content, destination):
    """
    Write content to gzipped file
    """
    import mgzip

    with mgzip.open(destination, 'wb', thread=12) as destfile:
        for blob in content:
            destfile.write(blob)
