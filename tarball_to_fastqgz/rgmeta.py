import os


def build_cwl_rgmeta(sample, rgname):
    """
    Uses sample names and rg_name from metadata to create rg_meta information for aligner

    PL : Platform
    PU : Platform-unit ideally flowcell barcode + lane; should be universally unique
    ID : read group identifier
    LB : unique identifier for sequencing library
    SM : unique identifier for sample
    CN : sequencing center
    DS : description
    DT : date sequenced
    FO : flow order
    KS : array of nucleotide bases corresponding to key sequence of each read
    PI : predicted median insert size
    PM : platform model; additional free-text details of sequencing platform
    """

    return dict(
        PL="ILLUMINA",
        PU=rgname,
        ID=rgname,
        LB=sample,
        SM=sample,
        CN='',
        DS='',
        DT='',
        FO='',
        KS='',
        PI='',
        PM='',
    )


def getmount(path):
    path = os.path.realpath(os.path.abspath(path))
    while path != os.path.sep:
        if os.path.ismount(path):
            return path
        path = os.path.abspath(os.path.join(path, os.pardir))
    return path


def build_cwl_file(file):
    """
    build dictionary representing cwl File object
    """

    return {
        'class': 'File',
        'location': os.path.basename(file),
    }


def build_rg_fastq_file_record(sample, rgname, fq1, fq2=None):
    """
    build dictionary representing readgroup_fastq_file object
    """

    return dict(
        forward_fastq=build_cwl_file(fq1),
        reverse_fastq=build_cwl_file(fq2),
        readgroup_meta=build_cwl_rgmeta(sample, rgname),
    )
