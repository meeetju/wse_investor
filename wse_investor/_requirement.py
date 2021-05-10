from wse_investor._limits_reader import LimitsReader


class Requirement:

    def __init__(self, limits_reader: LimitsReader):
        self._p_e_max_limit = limits_reader.get_p_e_max_limit()
        self._roe_min_limit = limits_reader.get_roe_min_limit()
        self._p_bv_max_limit = limits_reader.get_p_bv_max_limit()
        self._p_bv_g_max_limit = limits_reader.get_p_pv_g_max_limit()
        self._f_score_min_limit = limits_reader.get_f_score_min_limit()
        self._dividend_years = limits_reader.get_dividend_years()
        self._acceptable_ratings = limits_reader.get_allowed_altman_ratings()

    def is_p_e_less_equal_to_limit(self, p_e):
        if self._p_e_max_limit == 0.0:
            return True
        if p_e == '-':
            return False
        return 0.0 < float(p_e) <= self._p_e_max_limit

    def is_roe_greater_equal_to_limit(self, roe):
        if self._roe_min_limit == 0.0:
            return True
        if roe == '-':
            return False
        return float(roe) >= self._roe_min_limit

    def is_dividend_paid(self, last_dividend_year):
        if not last_dividend_year:
            return False
        return last_dividend_year in self._dividend_years

    def is_p_bv_less_equal_to_limit(self, p_bv):
        if self._p_bv_max_limit == 0.0:
            return True
        if p_bv == '-':
            return False
        return 0.0 < float(p_bv) <= self._p_bv_max_limit

    def is_p_bv_g_less_equal_to_limit(self, p_bv_g):
        if self._p_bv_g_max_limit == 0.0:
            return True
        if p_bv_g == '-':
            return False
        return 0.0 < float(p_bv_g) <= self._p_bv_g_max_limit

    def is_altman_rating_good(self, rating):
        return rating in self._acceptable_ratings

    def is_f_score_greater_equal_to_limit(self, f_score):
        if self._f_score_min_limit == 0.0:
            return True
        if f_score is None:
            return False
        return self._f_score_min_limit <= float(f_score)
