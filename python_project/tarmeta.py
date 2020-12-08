from itertools import zip_longest

import pandas as pd

# TAR TYPES
TAR_FASTQ = 'fastq.tar'
TAR_GZ = 'tar.gz'

# FASTQ TYPES
FASTQ_PLAIN = 'fastq'
FASTQ_GZ = 'fastq.gz'

# RESOLUTION STRATEGIES
STRAT_PE_TAR_FQGZ = 'list of paired fastq.gz files'
STRAT_PE_TARGZ_FQPLAIN = 'paired plain fastq files in tar.gz'
STRAT_SE_TARGZ_FQPLAIN = 'single plain fastq file in tar.gz'


def grouper(n, iterable, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(fillvalue=fillvalue, *args)


def get_meta(meta_file=None, tar_file=None, check_types=True) -> tuple:
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
    sar_id: <sar_id>
    project: <project>
    tar_type: <tar_type>
    fq_type: <fq_type>
    PE: <pe>
    num_fq: <num_fq>
    read_groups:
        <rg1>: 
            rg_meta: 
                <rg_meta_fields>
            fq_list: [fq_list]
        ...
        <rgN>: 
            rg_meta: 
                <rg_meta_fields>
            fq_list: [fq_list]
    """

    if meta_file is None:
        # raise exception
        pass
    if tar_file is None:
        # raise exception
        pass

    df = pd.read_table(meta_file)
    # select records that correspond to the specific tar file
    sel = df['tar_name'] == tar_file
    tdf = df[sel].copy()
    # prepare to build metadata dictionary
    meta = {}
    # save keys consistent in tar file
    for key in ['tar_name', 'sar_id', 'project', 'tar_type', 'num_fq', 'PE', 'fq_type']:
        meta[key] = tdf.iloc[0][key]
        # iterate over read groups in tar file saving rg name and paired files
        rg_name_list = []
        rg_dict_list = []
        for idx, grp in tdf.groupby('read_group_name'):
            rg = {}
            rg['files'] = list(grouper(2, grp['fq_name'].sort_values()))
            rg_name_list.append(idx)
            rg_dict_list.append(rg)
        meta['read_groups'] = dict(zip(rg_name_list, rg_dict_list))
    return meta, tdf['fq_name'].tolist()

    # # gather relevant metadata
    # meta = {}
    # with open(meta_file, 'r') as meta:
    #     keys = meta.readline().strip().split('\t')
    #     rg_files = {}
    #     for line in meta:
    #         linedict = {k:v for k,v in zip(keys, line.strip().split('\t'))}

    #         if check_types:
    #             check_input_types(linedict)

    #         # Build metadata entry
    #         if linedict['tar_name'] == tar_file:
    #             meta['sar_id'] = linedict['sar_id']
    #             meta['project'] = linedict['project']
    #             meta['tar_type'] = linedict['tar_type']
    #             meta['fq_type'] = linedict['fq_type']
    #             meta['PE'] = bool(linedict['PE'])
    #             meta['num_fq'] = int(linedict['num_fq'])

    #             rg = linedict['read_group_name']
    #             if linedict['PE']:
    #                 match = re_pair.search(linedict['fq_name'])
    #                 rg_files
    #             else:
    #                 rg_files = rg_files.get()

    #             rg_files = rg_files.get(linedict['read_group'], []) + [linedict['fq_name']]
    # meta['read_groups'] = rg_files

    # if len(meta) == 0:
    #     # raise exception not found
    #     pass
    # return meta


def check_input_types(linedict):
    """
    Check that input data are in expected range
    """
    if linedict['tar_type'] not in set([TAR_FASTQ, TAR_GZ]):
        # raise exception undefined tar_type
        pass
    if linedict['fq_type'] not in set([FASTQ_PLAIN, FASTQ_GZ]):
        # raise exception undefined fq_type
        pass
    if linedict['num_fq'] not in set(['1', '2', '4', '6']):
        # raise exception unexpected num_fq
        pass
    if linedict['PE'] not in set(['True', 'False']):
        # raise exception unexpected PE
        pass
