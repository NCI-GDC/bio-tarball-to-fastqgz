from unittest import TestCase

from pkg_resources import resource_filename

from tarball_to_fastqgz.tarmeta import get_meta, grouper


class TestTarMeta(TestCase):
    def test_grouper_even(self):
        source = ['a', 'b', 'c', 'd']
        res = list(grouper(2, source, fillvalue=None))

        expected = [('a', 'b'), ('c', 'd')]

        assert res == expected

    def test_grouper_odd(self):
        source = ['a', 'b', 'c']
        res = list(grouper(2, source, fillvalue=None))

        expected = [('a', 'b'), ('c', None)]

        assert res == expected

    def test_get_meta_pe(self):
        meta_file = resource_filename(
            "tarball_to_fastqgz", "metadata/tcga.rna.11128.tarball.meta.tsv"
        )
        tarball = 'UNCID_2199907.0f61b005-3643-4a6b-a075-bffb7320a2f3.111206_UNC15-SN850_0154_BD080PACXX_8_ATCACG.tar.gz'
        rgmeta, files = get_meta(meta_file, tarball)

        expected = {
            "tar_name": "UNCID_2199907.0f61b005-3643-4a6b-a075-bffb7320a2f3.111206_UNC15-SN850_0154_BD080PACXX_8_ATCACG.tar.gz",
            "sar_id": "a16faa7d-fa0b-42ea-a764-08894950453c",
            "project": "TCGA-LUAD",
            "tar_type": "tar.gz",
            "num_fq": 2,
            "PE": True,
            "fq_type": "fastq",
            "read_groups": {
                "111206_UNC15-SN850_0154_BD080PACXX_ATCACG_L008": {
                    "files": [
                        (
                            "111206_UNC15-SN850_0154_BD080PACXX_ATCACG_L008_1.fastq",
                            "111206_UNC15-SN850_0154_BD080PACXX_ATCACG_L008_2.fastq",
                        )
                    ]
                }
            },
        }

        assert rgmeta == expected

    def test_get_meta_se(self):
        meta_file = resource_filename(
            "tarball_to_fastqgz", "metadata/tcga.rna.11128.tarball.meta.tsv"
        )
        tarball = "UNCID_2210473.00186124-cecf-4580-9dca-cef7c09f741c.110406_UNC1-RDR301647_00058_FC_70EYTAAXX_2.tar.gz"
        rgmeta, files = get_meta(meta_file, tarball)

        expected = {
            "tar_name": "UNCID_2210473.00186124-cecf-4580-9dca-cef7c09f741c.110406_UNC1-RDR301647_00058_FC_70EYTAAXX_2.tar.gz",
            "sar_id": "375efe57-47ba-4adb-ab51-d72830572c9e",
            "project": "TCGA-UCEC",
            "tar_type": "tar.gz",
            "num_fq": 1,
            "PE": False,
            "fq_type": "fastq",
            "read_groups": {
                "110406_UNC1-RDR301647_00058_FC_70EYTAAXX.2": {
                    "files": [
                        ("110406_UNC1-RDR301647_00058_FC_70EYTAAXX.2.fastq", None)
                    ]
                }
            },
        }

        assert rgmeta == expected
