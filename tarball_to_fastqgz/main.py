#!/usr/bin/env python
"""
Python Project Template
"""

import argparse
import collections
import datetime
import logging
import os
import sys
from typing import List, Optional

from fileops import find_targets_from_tar
from staging import stage
from tarmeta import get_meta

try:
    from tarball_to_fastqgz import __version__
except Exception:
    __version__ = '0.0.0'

log = logging.getLogger(__name__)


def setup_logger(args):
    """Apply logging config from CLI args."""

    logging.basicConfig(
        level=args.log_level, format=args.log_format,
    )


def setup_parser():
    parser = argparse.ArgumentParser()

    logging_group = parser.add_argument_group("Logging")
    logging_group.add_argument(
        '--log-level',
        choices=[
            logging.INFO,
            logging.DEBUG,
            logging.CRITICAL,
            logging.WARNING,
            logging.ERROR,
        ],
        type=int,
        default=logging.INFO,
    )
    logging_group.add_argument(
        '--log-format',
        type=str,
        metavar='STR',
        default="%(asctime)s %(name)s:%(lineno)s %(levelname)s | %(message)s",
    )

    parser.add_argument('--version', action='version', version=__version__)
    parser.add_argument(
        '--meta',
        '-m',
        dest='meta',
        type=str,
        required=True,
        help='metadata describing tarball contents',
    )
    parser.add_argument(
        '--tarball', '-t', dest='tarfile', type=str, required=True, help='tar file'
    )
    parser.add_argument(
        '--sample',
        dest='sample',
        type=str,
        required=True,
        help='sample identifier (uuid)',
    )

    return parser


def process_args(argv: Optional[List] = None) -> collections.namedtuple:
    """Process args to NamedTuple.
    """

    parser = setup_parser()
    argv = argv or sys.argv

    if argv:
        args, unknown_args = parser.parse_known_args(argv)
    else:
        args, unknown_args = parser.parse_known_args()

    # if args.data_dir:
    #     os.makedirs(args.data_dir)

    args_dict = vars(args)

    # Process extras list
    args_dict['extras'] = unknown_args

    # Recast to immutable namedtuple
    run_args = collections.namedtuple('RunArgs', list(args_dict.keys()))
    return run_args(**args_dict)


def run(run_args) -> int:
    """Method for running script logic."""

    ret_val = 0

    start_time = datetime.datetime.now()

    log.info("Running process...")

    log.info("Got arguments:")
    log.info('meta {}'.format(run_args.meta))
    log.info('tarfile {}'.format(run_args.tarfile))
    log.info('sample {}'.format(run_args.sample))

    # get metadata relevant to tarfile
    log.info('Parsing metadata table.')
    meta, fq_list = get_meta(meta_file=run_args.meta, tar_file=run_args.tarfile)

    # find targets in tar file, save in look-up table
    log.info('Identifying file paths in tarball')
    tar_members = find_targets_from_tar(
        tar_file=run_args.tarfile, target_file_list=fq_list
    )

    # stage fastq and read files
    log.info('Staging data')
    stage(meta, tar_members, run_args.tarfile, run_args.sample)

    # Log runtime info
    end_time = datetime.datetime.now()
    run_time = end_time - start_time
    log.info("Run time: %d seconds", run_time.seconds)
    return ret_val


def main(argv=None) -> int:
    """Main Entrypoint."""
    exit_code = 0

    args = process_args(argv)

    setup_logger(args)

    log.info("Process called with %s", args)

    try:
        exit_code = run(args)
    except Exception as e:
        log.exception(e)
        exit_code = 1
    return exit_code


if __name__ == "__main__":
    """CLI Entrypoint"""

    status_code = 0
    try:
        status_code = main()
    except Exception as e:
        log.exception(e)
        sys.exit(1)
    sys.exit(status_code)


# __END__
