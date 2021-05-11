from abc import ABC, abstractmethod
import logging
import yaml

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class LimitsReader(ABC):

    @abstractmethod
    def get_p_e_max_limit(self):
        """Get P/E max limit."""

    @abstractmethod
    def get_roe_min_limit(self):
        """Get ROE min limit."""

    @abstractmethod
    def get_dividend_years(self):
        """Get dividend years."""

    @abstractmethod
    def get_p_bv_max_limit(self):
        """Get P/BV max limit."""

    @abstractmethod
    def get_p_pv_g_max_limit(self):
        """Get P/BV Graham max limit."""

    @abstractmethod
    def get_allowed_altman_ratings(self):
        """Get allowed altman ratings."""

    @abstractmethod
    def get_f_score_min_limit(self):
        """Get Piotroski F-Score max limit."""


class LimitsYamlReader(LimitsReader):

    def __init__(self, path):
        self._source_path = path
        self._limits = {}
        self._read()

    def _read(self):
        with open(self._source_path) as f:
            parsed_f = yaml.load(f, Loader=yaml.FullLoader)
            self._limits = parsed_f['limits']

    def get_p_e_max_limit(self):
        """Get P/E max limit."""
        p_e_max = float(self._limits['p_e_max_limit'])
        logger.info('Using P/E max limit: %s' % p_e_max)
        return p_e_max

    def get_roe_min_limit(self):
        """Get ROE min limit."""
        roe_min = float(self._limits['roe_min_limit'])
        logger.info('Using ROE min limit: %s' % roe_min)
        return roe_min

    def get_dividend_years(self):
        """Get dividend years."""
        dividend_yrs = self._limits['dividend_years']
        logger.info('Using dividend years: %s' % dividend_yrs)
        return dividend_yrs

    def get_p_bv_max_limit(self):
        """Get P/BV max limit."""
        p_bv_max = float(self._limits['p_bv_max_limit'])
        logger.info('Using P/BV max limit: %s' % p_bv_max)
        return p_bv_max

    def get_p_pv_g_max_limit(self):
        """Get P/BV Graham max limit."""
        p_bv_g_max = float(self._limits['p_bv_g_max_limit'])
        logger.info('Using P/BV Graham max limit: %s' % p_bv_g_max)
        return p_bv_g_max

    def get_allowed_altman_ratings(self):
        """Get allowed altman ratings."""
        altmans = self._limits['ratings']
        logger.info('Using allowed Altman Rating values %s' % altmans)
        return altmans

    def get_f_score_min_limit(self):
        """Get Piotroski F-Score max limit."""
        f_score_min = float(self._limits['f_score'])
        logger.info('Using Piotroski F-Score min limit: %s' % f_score_min)
        return f_score_min
