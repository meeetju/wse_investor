from bs4 import BeautifulSoup
import logging
import requests

from wse_investor._company import Company
from wse_investor._requirement import Requirement

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class FinancialIndicators:

    def __init__(self, companies: [Company], requirement: Requirement):
        self._in_companies = companies
        self._out_companies = []
        self._requirement = requirement

    def _get_financial_indicator_content(self, company):
        indicators_values = []

        link = company.base_link + r'/wskazniki-finansowe'
        try:
            indicators_www = requests.get(link)
            indicators = BeautifulSoup(indicators_www.text, "html.parser")
            for tr in indicators.findAll('tr'):
                for td in tr.findAll('td'):
                    indicators_values.append(self._get_value(td))

            company.p_e = indicators_values[1]
            company.p_bv = indicators_values[3]
            company.p_bv_g = indicators_values[5]
            company.p_s = indicators_values[9]
            company.roe = indicators_values[21]

            logger.info('Getting data from : %s' % link)
        except:
            logger.warning('Could not reach : %s' % link)

    def _get_value(self, td):
        return td.text.replace('%', '').replace(' ', '')

    def get_best_companies(self):
        for company in self._in_companies:
            self._get_financial_indicator_content(company)
            if all([self._requirement.is_p_e_less_equal_to_limit(company.p_e),
                    self._requirement.is_p_bv_less_equal_to_limit(company.p_bv),
                    self._requirement.is_p_bv_g_less_equal_to_limit(company.p_bv_g),
                    self._requirement.is_roe_greater_equal_to_limit(company.roe)]):
                self._out_companies.append(company)

        logger.info('Identified %s companies with good indicators' % str(len(self._out_companies)))
        return self._out_companies
