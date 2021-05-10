from mock import patch, mock_open
import pytest

from wse_investor._limits_reader import LimitsTxtFileReader
from wse_investor._requirement import Requirement
from tests.data_for_tests import limits_file_text


class TestRequirements:

    @pytest.fixture
    def limits_reader(self):
        with patch("builtins.open", new_callable=mock_open, read_data=limits_file_text):
            self.requirement = Requirement(LimitsTxtFileReader('dummy path'))
            yield

    def test_p_e_requirement(self, limits_reader):

        self.requirement._p_e_max_limit = 10.0

        assert not self.requirement.is_p_e_less_equal_to_limit('11')
        assert self.requirement.is_p_e_less_equal_to_limit('10')
        assert self.requirement.is_p_e_less_equal_to_limit('9')
        assert not self.requirement.is_p_e_less_equal_to_limit('-')

    def test_altman_rating_requirement(self, limits_reader):

        assert not self.requirement.is_altman_rating_good('CCC')
        assert self.requirement.is_altman_rating_good('AAA')
        assert self.requirement.is_altman_rating_good('A-')
        assert self.requirement.is_altman_rating_good('BB+')

    def test_f_score_requirement(self, limits_reader):

        self.requirement._f_score_min_limit = 5.0

        assert not self.requirement.is_f_score_greater_equal_to_limit('4')
        assert self.requirement.is_f_score_greater_equal_to_limit('5')
        assert self.requirement.is_f_score_greater_equal_to_limit('6')
        assert not self.requirement.is_f_score_greater_equal_to_limit(None)

    def test_p_bv_requirement(self, limits_reader):

        self.requirement._p_bv_max_limit = 5.0

        assert not self.requirement.is_p_bv_less_equal_to_limit('6')
        assert self.requirement.is_p_bv_less_equal_to_limit('5')
        assert self.requirement.is_p_bv_less_equal_to_limit('4')
        assert not self.requirement.is_p_bv_less_equal_to_limit('-')

    def test_p_bv_g_requirement(self, limits_reader):

        self.requirement._p_bv_g_max_limit = 10.0

        assert not self.requirement.is_p_bv_g_less_equal_to_limit('11')
        assert self.requirement.is_p_bv_g_less_equal_to_limit('10')
        assert self.requirement.is_p_bv_g_less_equal_to_limit('9')
        assert not self.requirement.is_p_bv_g_less_equal_to_limit('-')

    def test_dividend_paid__requirement(self, limits_reader):

        assert not self.requirement.is_dividend_paid('2018')
        assert self.requirement.is_dividend_paid('2019')
        assert self.requirement.is_dividend_paid('2020')
        assert self.requirement.is_dividend_paid('2021')
        assert not self.requirement.is_dividend_paid(None)

    def test_roe_requirement(self, limits_reader):

        self.requirement._roe_min_limit = 5.0

        assert not self.requirement.is_roe_greater_equal_to_limit('4')
        assert self.requirement.is_roe_greater_equal_to_limit('5')
        assert self.requirement.is_roe_greater_equal_to_limit('6')
        assert not self.requirement.is_roe_greater_equal_to_limit('-')

    def test_disabled_requirements(self, limits_reader):

        self.requirement._p_e_max_limit = 0.0
        assert self.requirement.is_p_e_less_equal_to_limit('100')

        self.requirement._roe_min_limit = 0.0
        assert self.requirement.is_roe_greater_equal_to_limit('1')

        self.requirement._p_bv_max_limit = 0.0
        assert self.requirement.is_p_bv_less_equal_to_limit('100')

        self.requirement._p_bv_g_max_limit = 0.0
        assert self.requirement.is_p_bv_g_less_equal_to_limit('100')

        self.requirement._f_score_min_limit = 0.0
        assert self.requirement.is_f_score_greater_equal_to_limit('100')

