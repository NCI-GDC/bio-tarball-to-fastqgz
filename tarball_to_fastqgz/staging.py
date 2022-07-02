from json import dumps

from tarball_to_fastqgz.error import NoStrategyError
from tarball_to_fastqgz.fileops import from_tar_to_dest
from tarball_to_fastqgz.rgmeta import build_rg_fastq_file_record
from tarball_to_fastqgz.tarmeta import FASTQ_GZ, FASTQ_PLAIN, TAR_FASTQ, TAR_GZ


def stage(
    meta: dict,
    tar_members: dict,
    tarfile: str,
    sample_id: str,
    json_filename: str = 'rg_fastq_list.json',
    prefix: str = './',
    dryrun: bool = False,
) -> None:
    """
    Extract data and stage files into directory
    """

    strategy_fn = resolve_strategy(meta)
    rg_fq_record_list = []

    for rg_name, rg_dict in meta['read_groups'].items():
        for fq1, fq2 in rg_dict['files']:
            fq1_loc = strategy_fn(tarfile, tar_members[fq1], fq1, prefix, dryrun)
            fq2_loc = (
                strategy_fn(tarfile, tar_members[fq2], fq2, prefix, dryrun)
                if fq2 is not None
                else None
            )
            rec = build_rg_fastq_file_record(sample_id, rg_name, fq1_loc, fq2_loc)
            rg_fq_record_list += [rec]
    write_json_file(rg_fq_record_list, prefix + json_filename, dryrun)


def write_json_file(object: list, json_filename: str, dryrun: bool = False):
    """
    Writes readgroup_fastq_file_list json file
    """
    if dryrun:
        print(dumps(object, indent=4, sort_keys=True))
    else:
        with open(json_filename, 'w') as json_out:
            json_out.write(dumps(object))


def resolve_strategy(meta: dict) -> callable:
    """
    Decide which strategy to use for extracting files and placing them where they should be
    """

    if (
        meta['tar_type'] == TAR_FASTQ
        and meta['fq_type'] == FASTQ_GZ
        and meta['PE'] is True
    ):
        return strat_pe_tar_fqgz
    if (
        meta['tar_type'] == TAR_GZ
        and meta['fq_type'] == FASTQ_PLAIN
        and meta['PE'] is True
    ):
        return strat_pe_targz_fqplain
    if (
        meta['tar_type'] == TAR_GZ
        and meta['fq_type'] == FASTQ_PLAIN
        and meta['PE'] is False
    ):
        return strat_se_targz_fqplain

    raise NoStrategyError("NO STRATEGY FOUND")


def strat_pe_tar_fqgz(
    tar_filename: str,
    tar_member: str,
    basename: str,
    prefix: str = './',
    dryrun: bool = False,
) -> str:
    """
    tar file containing paired fastq.gz files; between 1 and 3 pairs

    Extract fastq.gz files into output directory
    returns destination
    """

    dest_name = prefix + basename
    # extract tar_member from tar file, save to file at dest_name
    if not dryrun:
        from_tar_to_dest(
            tar_file=tar_filename,
            tar_member=tar_member,
            destination=dest_name,
            compress_dest=False,
        )
    return dest_name


def strat_pe_targz_fqplain(
    tar_filename: str,
    tar_member: str,
    basename: str,
    prefix: str = './',
    dryrun: bool = False,
):
    """
    tar.gz file contiaining plain paired-end fastq files

    Extract fastq files, write compressed file to output directory
    returns destination file
    """
    dest_name = prefix + basename + '.gz'
    # extract tar_member from tar file, gzip and save to file at dest_name
    if not dryrun:
        from_tar_to_dest(
            tar_file=tar_filename,
            tar_member=tar_member,
            destination=dest_name,
            compress_dest=True,
        )
    return dest_name


def strat_se_targz_fqplain(
    tar_filename: str,
    tar_member: str,
    basename: str,
    prefix: str = './',
    dryrun: bool = False,
):
    """
    tar.gz file containing plain single-end fastq file

    Extract fastq file, write compressed file to output directory
    returns destination file
    """

    dest_name = prefix + basename + '.gz'
    # extract tar_member from tar file, gzip and save to file at dest_name
    if not dryrun:
        from_tar_to_dest(
            tar_file=tar_filename,
            tar_member=tar_member,
            destination=dest_name,
            compress_dest=True,
        )
    return dest_name
