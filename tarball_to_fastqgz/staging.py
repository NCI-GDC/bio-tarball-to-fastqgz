from json import dumps

from tarball_to_fastqgz.fileops import from_tar_to_dest
from tarball_to_fastqgz.rgmeta import build_rg_fastq_file_record
from tarball_to_fastqgz.tarmeta import FASTQ_GZ, FASTQ_PLAIN, TAR_FASTQ, TAR_GZ


def stage(
    meta,
    tar_members,
    tarfile,
    sample_id,
    json_filename='rg_fastq_list.json',
    prefix='./',
    dryrun=False,
):
    """
    Extract data and stage files into directory
    """

    strategy_fn = resolve_strategy(meta)
    rg_fq_record_list = []

    for rg_name, rg_dict in meta['read_groups'].items():
        # log.info("Processing read group {}".format(rg_name))
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


def write_json_file(object, json_filename, dryrun=False):
    """
    Writes readgroup_fastq_file_list json file
    """
    if dryrun:
        print(dumps(object, indent=4, sort_keys=True))
    else:
        with open(json_filename, 'w') as json_out:
            json_out.write(dumps(object))


def resolve_strategy(meta=None):
    """
    Decide which strategy to use for extracting files and placing them where they should be
    """

    if (
        meta['tar_type'] == TAR_FASTQ
        and meta['fq_type'] == FASTQ_GZ
        and meta['PE'] == True
    ):
        return strat_pe_tar_fqgz
    if (
        meta['tar_type'] == TAR_GZ
        and meta['fq_type'] == FASTQ_PLAIN
        and meta['PE'] == True
    ):
        return strat_pe_targz_fqplain
    if (
        meta['tar_type'] == TAR_GZ
        and meta['fq_type'] == FASTQ_PLAIN
        and meta['PE'] == False
    ):
        return strat_se_targz_fqplain

    print("NO STRATEGY FOUND")


def strat_pe_tar_fqgz(
    tar_filename, tar_member, basename, prefix='./', dryrun=False
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
    tar_filename, tar_member, basename, prefix='./', dryrun=False
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
    tar_filename, tar_member, basename, prefix='./', dryrun=False
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
