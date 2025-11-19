from itertools import zip_longest
from os import PathLike
from typing import Any, Dict, Iterable, List, Optional, Tuple

import pandas as pd

# from tarball_to_fastqgz.error import UndefinedTarType, UndefinedFastqType, FqNumberOutOfBounds, UnexpectedPEType

# TAR TYPES
TAR_FASTQ = "fastq.tar"
TAR_GZ = "tar.gz"

# FASTQ TYPES
FASTQ_PLAIN = "fastq"
FASTQ_GZ = "fastq.gz"

# RESOLUTION STRATEGIES
STRAT_PE_TAR_FQGZ = "list of paired fastq.gz files"
STRAT_PE_TARGZ_FQPLAIN = "paired plain fastq files in tar.gz"
STRAT_SE_TARGZ_FQPLAIN = "single plain fastq file in tar.gz"


def grouper(n: int, iterable: Iterable, fillvalue: Any = None) -> Iterable:
    "Collect data into fixed-length chunks or blocks"
    # grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(fillvalue=fillvalue, *args)


def get_meta(
    meta_file: PathLike[str], tar_file: Optional[str] = None
) -> Tuple[Dict[str, Any], List[Any]]:
    """
    lookup tar_file in meta_file and decide how to handle the data
    metadata is expected to have these columns:
    sar_id
    project
    tar_name
    tar_type
    num_fq
    fq_size
    fq_name
    fq_type
    read_group_name
    PE

    returns dict with following structure
    tar_name: <tar_name>
    sar_id: <sar_id>
    project: <project>
    tar_type: <tar_type>
    num_fq: <num_fq>
    PE: <pe>
    fq_type: <fq_type>
    read_groups:
        <rg1>:
            files: [fq_list]
        ...
        <rgN>:
            files: [fq_list]
    """

    if meta_file is None:
        # raise exception
        pass
    if tar_file is None:
        # raise exception
        pass

    df = pd.read_table(meta_file)
    # select records that correspond to the specific tar file
    sel = df["tar_name"] == tar_file
    tdf = df[sel].copy()
    # prepare to build metadata dictionary
    meta = {}
    # save keys consistent in tar file
    for key in ["tar_name", "sar_id", "project", "tar_type", "num_fq", "PE", "fq_type"]:
        meta[key] = tdf.iloc[0][key]
        if key == "PE":
            meta[key] = bool(meta[key])
        # iterate over read groups in tar file saving rg name and paired files
        rg_name_list = []
        rg_dict_list = []
        for idx, grp in tdf.groupby("read_group_name"):
            rg = {}
            rg["files"] = list(grouper(2, grp["fq_name"].sort_values()))
            rg_name_list.append(idx)
            rg_dict_list.append(rg)
        meta["read_groups"] = dict(zip(rg_name_list, rg_dict_list))
    return meta, tdf["fq_name"].tolist()


# def check_input_types(linedict):
#     """
#     Check that input data are in expected range
#     """
#     if linedict['tar_type'] not in set([TAR_FASTQ, TAR_GZ]):
#         raise UndefinedTarType(linedict['tar_type'])
#     if linedict['fq_type'] not in set([FASTQ_PLAIN, FASTQ_GZ]):
#         # raise exception undefined fq_type
#         raise UndefinedFastqType(linedict['fq_type'])
#     if linedict['num_fq'] not in set(['1', '2', '4', '6']):
#         # raise exception unexpected num_fq
#         raise FqNumberOutOfBounds(linedict['num_fq'])
#     if linedict['PE'] not in set(['True', 'False']):
#         # raise exception unexpected PE
#         raise UnexpectedPEType(linedict['PE'])
