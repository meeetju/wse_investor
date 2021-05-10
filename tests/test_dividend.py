from mock import MagicMock, patch, mock_open
import pytest
import requests

from wse_investor._rank import RankedCompanies
from wse_investor._dividend import Dividend
from wse_investor._limits_reader import LimitsTxtFileReader
from wse_investor._requirement import Requirement
from tests.data_for_tests import ratings_response_text, limits_file_text, dividend_text


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
    def dividend_response(self):
        self.dividend = MagicMock(spec=requests.models.Response)
        self.dividend.text = dividend_text
        yield

    def test_dividends_are_parsed(self, limits_reader, dividend_response, ratings_response):

        with patch('wse_investor._rank.requests.get', return_value=self.ratings):
            companies = RankedCompanies(self.requirement).get_all_companies()

        with patch('wse_investor._dividend.requests.get', return_value=self.dividend):
            dividend = Dividend(companies, self.requirement)
            dividend_companies = dividend.get_best_companies()

        assert len(dividend_companies) == 4

        company = dividend_companies[0]

        assert company.base_link == r'https://strefainwestorow.pl/notowania/gpw/MIRBUD-MRB'
        assert company.last_dividend_year == '2019'
        assert company.last_buy_date == '03.07.2020'
        assert company.dividend_percent == '1.27'
        assert company.payment_date == '13.08.2020'
        assert company.dividend_amount == '0.02'

    def test_companies_with_no_dividend_at_years_are_not_returned(self, limits_reader, dividend_response, ratings_response):

        self.requirement._dividend_years = ['2020']

        with patch('wse_investor._rank.requests.get', return_value=self.ratings):
            companies = RankedCompanies(self.requirement).get_all_companies()

        with patch('wse_investor._dividend.requests.get', return_value=self.dividend):
            dividend = Dividend(companies, self.requirement)
            dividend_companies = dividend.get_best_companies()

        assert len(dividend_companies) == 0
