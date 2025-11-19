from importlib.resources import files
from unittest import TestCase

from tarball_to_fastqgz.tarmeta import get_meta, grouper


class TestTarMeta(TestCase):
    def test_grouper_even(self):
        source = ["a", "b", "c", "d"]
        res = list(grouper(2, source, fillvalue=None))
        expected = [("a", "b"), ("c", "d")]
        assert res == expected

    def test_grouper_odd(self):
        source = ["a", "b", "c"]
        res = list(grouper(2, source, fillvalue=None))
        expected = [("a", "b"), ("c", None)]
        assert res == expected

    def test_get_meta_pe(self):
        meta_file = files("tarball_to_fastqgz").joinpath(
            "metadata/tcga.rna.11128.tarball.meta.tsv"
        )
        tarball = (
            "UNCID_2199907.0f61b005-3643-4a6b-a075-bffb7320a2f3."
            "111206_UNC15-SN850_0154_BD080PACXX_8_ATCACG.tar.gz"
        )
        rgmeta, files_out = get_meta(meta_file, tarball)
        assert rgmeta["PE"] is True
        assert rgmeta["num_fq"] == 2

    def test_get_meta_se(self):
        meta_file = files("tarball_to_fastqgz").joinpath(
            "metadata/tcga.rna.11128.tarball.meta.tsv"
        )
        tarball = (
            "UNCID_2210473.00186124-cecf-4580-9dca-cef7c09f741c."
            "110406_UNC1-RDR301647_00058_FC_70EYTAAXX_2.tar.gz"
        )
        rgmeta, files_out = get_meta(meta_file, tarball)
        assert rgmeta["PE"] is False
        assert rgmeta["num_fq"] == 1
