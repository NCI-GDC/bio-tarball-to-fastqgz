from unittest import TestCase

from tarball_to_fastqgz.rgmeta import (
    build_cwl_file,
    build_cwl_rgmeta,
    build_rg_fastq_file_record,
)



class TestRgmeta(TestCase):
    def test_build_cwl_file(self):
        filename = "foo.txt"
        res = build_cwl_file(filename)

        expected = {"class": "File", "location": filename}

        assert res == expected

    def test_build_cwl_rgmeta(self):
        sample = "test_sample"
        rgname = "test_RG"
        rec = build_cwl_rgmeta(sample, rgname)

        expected = {
            "PL": "ILLUMINA",
            "PU": rgname,
            "ID": rgname,
            "LB": sample,
            "SM": sample,
        }

        assert rec == expected

    def test_build_rg_fastq_file_record_se(self):
        sample = "test_sample"
        rgname = "test_RG"
        fq1 = "test_R1.fq"

        rec = build_rg_fastq_file_record(sample, rgname, fq1)

        expected = {
            "readgroup_meta": {
                "PL": "ILLUMINA",
                "PU": rgname,
                "ID": rgname,
                "LB": sample,
                "SM": sample,
            },
            "forward_fastq": {"class": "File", "location": fq1},
        }

        assert rec == expected

    def test_build_rg_fastq_file_record_pe(self):
        sample = "test_sample"
        rgname = "test_RG"
        fq1 = "test_R1.fq"
        fq2 = "test_R2.fq"

        rec = build_rg_fastq_file_record(sample, rgname, fq1, fq2)

        expected = {
            "readgroup_meta": {
                "PL": "ILLUMINA",
                "PU": rgname,
                "ID": rgname,
                "LB": sample,
                "SM": sample,
            },
            "forward_fastq": {"class": "File", "location": fq1},
            "reverse_fastq": {"class": "File", "location": fq2},
        }

        assert rec == expected


# __END__
