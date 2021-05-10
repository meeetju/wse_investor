from bs4 import BeautifulSoup
import datetime
import logging
import re
import requests

from wse_investor._company import Company
from wse_investor._requirement import Requirement

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class RankedCompanies:

    RATINGS_URL = r'https://www.biznesradar.pl/spolki-rating/akcje_gpw'

    def __init__(self, requirement: Requirement):
        self._current_year = datetime.datetime.now().year
        self._companies = []
        self._requirement = requirement

    def get_best_companies(self):
        self._companies = []
        rating_tables = self._parse_companies_html_rows()
        for rating_table in rating_tables:
            company = self._create_company(rating_table)
            if all([self._requirement.is_altman_rating_good(company.rating),
                    self._requirement.is_f_score_greater_equal_to_limit(company.piotroski_f_score)]):
                self._companies.append(company)
        logger.info('Identified %s companies with good ratings' % str(len(self._companies)))
        return self._companies

    def get_all_companies(self):
        self._companies = []
        rating_tables = self._parse_companies_html_rows()
        for rating_table in rating_tables:
            self._companies.append(self._create_company(rating_table))
        return self._companies

    def _parse_companies_html_rows(self):
        ratings_www = requests.get(self.RATINGS_URL)
        ratings_content = BeautifulSoup(ratings_www.text, "html.parser")
        rows = ratings_content.findAll('tr')
        return self._remove_headers_sections(rows)

    @staticmethod
    def _remove_headers_sections(rows):
        output_rows = []
        for row in rows:
            str_row = str(row)
            if '<th>' not in str_row:
                output_rows.append(str_row)
        return output_rows

    def _create_company(self, rating_table):
        company = Company()
        company.name = self._get_name(rating_table)
        company.ticker = self._get_ticker(rating_table)
        company.rating_date = self._get_altman_rating_date(rating_table)
        company.rating = self._get_altman_rating(rating_table)
        company.piotroski_f_score = self._get_f_score(rating_table)
        self._set_base_link(company)
        return company

    def _get_ticker(self, rating_table):
        return self._get_value(re.findall('\">([A-Z0-9]+)[ (A-Z0-9.\-)]*</a', rating_table))

    def _get_name(self, rating_table):
        value = self._get_value(re.findall('\">[A-Z0-9]+ ([(A-Z0-9.\-)]+)</a', rating_table))
        if value:
            return value.replace('(', '').replace(')', '').replace('.', '')
        return self._get_ticker(rating_table)

    def _get_altman_rating(self, rating_table):
        return self._get_value(re.findall('\"color:#[A-F0-9]+\">([A-D]+[+-]?)</span', rating_table))

    def _get_altman_rating_date(self, rating_table):
        return self._get_value(re.findall('[0-9]{4}/Q[1-4]', rating_table))

    def _get_f_score(self, rating_table):
        return self._get_value(re.findall('\"color:#[A-F0-9]+\">([0-9])</span', rating_table))

    def _get_value(self, regex):
        value = regex
        if value:
            return value[0]
        return None

    def _set_base_link(self, company):
        company.base_link = r'https://strefainwestorow.pl/notowania/gpw/%s-%s' % (company.name, company.ticker)
