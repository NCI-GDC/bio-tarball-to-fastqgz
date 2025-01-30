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
from os import PathLike
from typing import List, NamedTuple, Optional

from pkg_resources import resource_filename

from tarball_to_fastqgz.fileops import find_targets_from_tar
from tarball_to_fastqgz.staging import stage
from tarball_to_fastqgz.tarmeta import get_meta

try:
    from tarball_to_fastqgz import __version__
except Exception:
    __version__ = "0.0.0"

log = logging.getLogger(__name__)


class RunArgs(NamedTuple):
    """Static NamedTuple for command-line arguments."""

    log_level: int
    log_format: str
    meta: PathLike[str]
    tarfile: str
    sample: str
    dryrun: bool
    extras: List[str]


def setup_logger(args: RunArgs) -> None:
    """Apply logging config from CLI args."""
    logging.basicConfig(
        level=args.log_level,
        format=args.log_format,
    )


def setup_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()

    logging_group = parser.add_argument_group("Logging")
    logging_group.add_argument(
        "--log-level",
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
        "--log-format",
        type=str,
        metavar="STR",
        default="%(asctime)s %(name)s:%(lineno)s %(levelname)s | %(message)s",
    )

    parser.add_argument("--version", action="version", version=__version__)
    parser.add_argument(
        "--meta",
        "-m",
        dest="meta",
        type=str,
        required=False,
        help="Metadata describing tarball contents",
        default=resource_filename(
            "tarball_to_fastqgz", "metadata/tcga.rna.11128.tarball.meta.tsv"
        ),
    )
    parser.add_argument(
        "--tarball", "-t", dest="tarfile", type=str, required=True, help="Tar file"
    )
    parser.add_argument(
        "--sample",
        dest="sample",
        type=str,
        required=True,
        help="Sample identifier (UUID)",
    )
    parser.add_argument(
        "--dryrun",
        dest="dryrun",
        required=False,
        default=False,
        action="store_true",
        help="Do not write any files, just print JSON to STDOUT",
    )

    return parser


def process_args(argv: Optional[List[str]] = None) -> RunArgs:
    """Process args into a statically declared RunArgs NamedTuple."""
    parser = setup_parser()
    if argv is None:
        # If no argv is passed, parse from command line
        args, unknown_args = parser.parse_known_args()
    else:
        args, unknown_args = parser.parse_known_args(argv)

    # Convert argparse namespace to a dict
    args_dict = vars(args)
    # Add any extra unknown arguments
    extras_list = unknown_args

    return RunArgs(
        log_level=args_dict["log_level"],
        log_format=args_dict["log_format"],
        meta=args_dict["meta"],
        tarfile=args_dict["tarfile"],
        sample=args_dict["sample"],
        dryrun=args_dict["dryrun"],
        extras=extras_list,
    )


def run(run_args: RunArgs) -> int:
    """Main script logic."""
    ret_val = 0
    start_time = datetime.datetime.now()

    log.info("Running process...")

    log.info("Got arguments:")
    log.info("meta: %s", run_args.meta)
    log.info("tarfile: %s", run_args.tarfile)
    log.info("sample: %s", run_args.sample)

    # Get metadata relevant to tarfile
    log.info("Parsing metadata table.")
    meta, fq_list = get_meta(
        meta_file=run_args.meta, tar_file=os.path.basename(run_args.tarfile)
    )

    # Find targets in tar file, save in lookup table
    log.info("Identifying file paths in tarball")
    tar_members = find_targets_from_tar(
        tar_file=run_args.tarfile, target_file_list=fq_list
    )

    # Stage fastq and read files
    log.info("Staging data")
    stage(
        meta,
        tar_members,
        run_args.tarfile,
        run_args.sample,
        json_filename="rg_fastq_list.json",
        prefix="./",
        dryrun=run_args.dryrun,
    )

    # Log runtime info
    end_time = datetime.datetime.now()
    run_time = end_time - start_time
    log.info("Run time: %d seconds", run_time.seconds)
    return ret_val


def main(argv: Optional[List[str]] = None) -> int:
    """Main entry point."""
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
