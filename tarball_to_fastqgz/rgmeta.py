import os


def build_cwl_rgmeta(sample: str, rgname: str) -> dict:
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
        # CN='null',
        # DS='null',
        # DT='null',
        # FO='null',
        # KS='null',
        # PI='null',
        # PM='null',
    )


def build_cwl_file(file: str) -> dict:
    """
    build dictionary representing cwl File object
    """

    return {"class": "File", "location": os.path.basename(file)}


def build_rg_fastq_file_record(
    sample: str, rgname: str, fq1: str, fq2: str = None
) -> dict:
    """
    build dictionary representing readgroup_fastq_file object
    """
    rec = dict(
        forward_fastq=build_cwl_file(fq1),
        readgroup_meta=build_cwl_rgmeta(sample, rgname),
    )
    if fq2 is not None:
        rec["reverse_fastq"] = build_cwl_file(fq2)
    return rec
