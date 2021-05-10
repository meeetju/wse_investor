from mock import MagicMock, patch, mock_open
import pytest
import requests

from wse_investor._rank import RankedCompanies
from wse_investor._financial_indicator import FinancialIndicators
from wse_investor._limits_reader import LimitsTxtFileReader
from wse_investor._requirement import Requirement
from tests.data_for_tests import ratings_response_text, limits_file_text, indicators_text


class TestFinancialIndicator:

    @pytest.fixture
    def limits_reader(self):
        with patch("builtins.open", new_callable=mock_open, read_data=limits_file_text):
            self.requirement = Requirement(LimitsTxtFileReader('dummy path'))
            yield

    @pytest.fixture
    def ratings_response(self):
        self.ratings = MagicMock(spec=requests.models.Response)
        self.ratings.text = ratings_response_text
        yield

    @pytest.fixture
    def indicators_response(self):
        self.indicators = MagicMock(spec=requests.models.Response)
        self.indicators.text = indicators_text
        yield

    def test_financial_indicators_are_parsed(self, indicators_response, ratings_response, limits_reader):

        with patch('wse_investor._rank.requests.get', return_value=self.ratings):
            companies = RankedCompanies(self.requirement).get_all_companies()

        self.requirement._p_e_max_limit = 0.0
        self.requirement._p_bv_max_limit = 0.0
        self.requirement._p_bv_g_max_limit = 0.0
        self.requirement._roe_min_limit = 0.0

        with patch('wse_investor._financial_indicator.requests.get', return_value=self.indicators):
            financial_indicator = FinancialIndicators(companies, self.requirement)
            companies = financial_indicator.get_best_companies()

        company = companies[0]

        assert company.base_link == r'https://strefainwestorow.pl/notowania/gpw/MIRBUD-MRB'
        assert company.p_e == '8.04'
        assert company.p_bv == '1.01'
        assert company.p_bv_g == '-'
        assert company.p_s == '0.38'
        assert company.roe == '12.61'

    def test_p_e_greater_than_requirement_companies_not_returned(self, indicators_response, ratings_response, limits_reader):

        with patch('wse_investor._rank.requests.get', return_value=self.ratings):
            companies = RankedCompanies(self.requirement).get_all_companies()

        self.requirement._p_e_max_limit = 8.039
        self.requirement._p_bv_max_limit = 0.0
        self.requirement._p_bv_g_max_limit = 0.0
        self.requirement._roe_min_limit = 0.0

        with patch('wse_investor._financial_indicator.requests.get', return_value=self.indicators):
            financial_indicator = FinancialIndicators(companies, self.requirement)
            financial_companies = financial_indicator.get_best_companies()

        assert len(financial_companies) == 0

    def test_p_e_equal_to_requirement_companies_returned(self, indicators_response, ratings_response, limits_reader):

        with patch('wse_investor._rank.requests.get', return_value=self.ratings):
            companies = RankedCompanies(self.requirement).get_all_companies()

        self.requirement._p_e_max_limit = 8.04
        self.requirement._p_bv_max_limit = 0.0
        self.requirement._p_bv_g_max_limit = 0.0
        self.requirement._roe_min_limit = 0.0

        with patch('wse_investor._financial_indicator.requests.get', return_value=self.indicators):
            financial_indicator = FinancialIndicators(companies, self.requirement)
            financial_companies = financial_indicator.get_best_companies()

        assert len(financial_companies) == 4

    def test_p_e_less_than_requirement_companies_returned(self, indicators_response, ratings_response, limits_reader):

        with patch('wse_investor._rank.requests.get', return_value=self.ratings):
            companies = RankedCompanies(self.requirement).get_all_companies()

        self.requirement._p_e_max_limit = 8.041
        self.requirement._p_bv_max_limit = 0.0
        self.requirement._p_bv_g_max_limit = 0.0
        self.requirement._roe_min_limit = 0.0

        with patch('wse_investor._financial_indicator.requests.get', return_value=self.indicators):
            financial_indicator = FinancialIndicators(companies, self.requirement)
            financial_companies = financial_indicator.get_best_companies()

        assert len(financial_companies) == 4

    def test_p_bv_greater_than_requirement_companies_not_returned(self, indicators_response, ratings_response, limits_reader):

        with patch('wse_investor._rank.requests.get', return_value=self.ratings):
            companies = RankedCompanies(self.requirement).get_all_companies()

        self.requirement._p_e_max_limit = 0.0
        self.requirement._p_bv_max_limit = 1.009
        self.requirement._p_bv_g_max_limit = 0.0
        self.requirement._roe_min_limit = 0.0

        with patch('wse_investor._financial_indicator.requests.get', return_value=self.indicators):
            financial_indicator = FinancialIndicators(companies, self.requirement)
            financial_companies = financial_indicator.get_best_companies()

        assert len(financial_companies) == 0

    def test_p_bv_equal_to_requirement_companies_returned(self, indicators_response, ratings_response, limits_reader):

        with patch('wse_investor._rank.requests.get', return_value=self.ratings):
            companies = RankedCompanies(self.requirement).get_all_companies()

        self.requirement._p_e_max_limit = 0.0
        self.requirement._p_bv_max_limit = 1.01
        self.requirement._p_bv_g_max_limit = 0.0
        self.requirement._roe_min_limit = 0.0

        with patch('wse_investor._financial_indicator.requests.get', return_value=self.indicators):
            financial_indicator = FinancialIndicators(companies, self.requirement)
            financial_companies = financial_indicator.get_best_companies()

        assert len(financial_companies) == 4

    def test_p_bv_less_than_requirement_companies_returned(self, indicators_response, ratings_response, limits_reader):

        with patch('wse_investor._rank.requests.get', return_value=self.ratings):
            companies = RankedCompanies(self.requirement).get_all_companies()

        self.requirement._p_e_max_limit = 0.0
        self.requirement._p_bv_max_limit = 1.011
        self.requirement._p_bv_g_max_limit = 0.0
        self.requirement._roe_min_limit = 0.0

        with patch('wse_investor._financial_indicator.requests.get', return_value=self.indicators):
            financial_indicator = FinancialIndicators(companies, self.requirement)
            financial_companies = financial_indicator.get_best_companies()

        assert len(financial_companies) == 4

    def test_roe_less_than_requirement_companies_not_returned(self, indicators_response, ratings_response, limits_reader):

        with patch('wse_investor._rank.requests.get', return_value=self.ratings):
            companies = RankedCompanies(self.requirement).get_all_companies()

        self.requirement._p_e_max_limit = 0.0
        self.requirement._p_bv_max_limit = 0.0
        self.requirement._p_bv_g_max_limit = 0.0
        self.requirement._roe_min_limit = 12.62

        with patch('wse_investor._financial_indicator.requests.get', return_value=self.indicators):
            financial_indicator = FinancialIndicators(companies, self.requirement)
            financial_companies = financial_indicator.get_best_companies()

        assert len(financial_companies) == 0

    def test_roe_equal_to_requirement_companies_returned(self, indicators_response, ratings_response, limits_reader):

        with patch('wse_investor._rank.requests.get', return_value=self.ratings):
            companies = RankedCompanies(self.requirement).get_all_companies()

        self.requirement._p_e_max_limit = 0.0
        self.requirement._p_bv_max_limit = 0.0
        self.requirement._p_bv_g_max_limit = 0.0
        self.requirement._roe_min_limit = 12.61

        with patch('wse_investor._financial_indicator.requests.get', return_value=self.indicators):
            financial_indicator = FinancialIndicators(companies, self.requirement)
            financial_companies = financial_indicator.get_best_companies()

        assert len(financial_companies) == 4

    def test_roe_greater_than_requirement_companies_returned(self, indicators_response, ratings_response, limits_reader):

        with patch('wse_investor._rank.requests.get', return_value=self.ratings):
            companies = RankedCompanies(self.requirement).get_all_companies()

        self.requirement._p_e_max_limit = 0.0
        self.requirement._p_bv_max_limit = 0.0
        self.requirement._p_bv_g_max_limit = 0.0
        self.requirement._roe_min_limit = 12.60

        with patch('wse_investor._financial_indicator.requests.get', return_value=self.indicators):
            financial_indicator = FinancialIndicators(companies, self.requirement)
            financial_companies = financial_indicator.get_best_companies()

        assert len(financial_companies) == 4
