from models import AgencyCountries, Country8DPFix, CountryExclusion

def float_or_zero(val):
    try:
        return float(val)
    except: 
        return 0

def sum_current_values(qs):
    item_getter = lambda x : float_or_zero(x.latest_value)
    return sum([item_getter(el) for el in qs])

def sum_baseline_values(qs):
    item_getter = lambda x : float_or_zero(x.baseline_value)
    return sum([item_getter(el) for el in qs])

def func_8dpfix(qs, agency, q):
    countries = Country8DPFix.objects.filter(agency=agency)
    denom = float(len(countries))
    base_num = len([country for country in countries if country.baseline_progress])
    cur_num = len([country for country in countries if country.latest_progress])

    if denom > 0:
        return base_num / denom * 100, cur_num / denom * 100
    else:
        return None, None


def question_values(qs, agency_or_country, q):
    qs = qs.filter(
        question_number=q, 
    )

    qs = qs.filter(question_number=q)
    assert len(qs) == 1
    
    base_val = qs[0].baseline_value
    cur_val = qs[0].latest_value

    return (base_value, cur_value)

def count_factory(value):
    def count_value(qs, agency_or_country, q):
        qs = qs.filter(
            question_number=q, 
        )

        base_value = qs.filter(
            baseline_value__iexact=value
        ).count()

        cur_value = qs.filter(
            latest_value__iexact=value
        ).count()
        
        return (base_value, cur_value)
    return count_value

def exclude_count_factory(value):
    def count_value(qs, agency_or_country, q):
        qs = qs.filter(
            question_number=q, 
        )

        base_value = qs.exclude(
            baseline_value__iexact=value
        ).count()

        cur_value = qs.exclude(
            latest_value__iexact=value
        ).count()
        
        return (base_value, cur_value)
    return count_value

def country_perc_factory(value):
    def perc_value(qs, agency, q):
        # In some countries certain processes do not exists
        # the watchlist reduces the denominator if the agency
        # is active in such a country for a particular question
        count_value = count_factory(value)
        base_value, _ = count_value(
            qs.exclude(submission__country__country__in=CountryExclusion.objects.baseline_excluded_countries(q)),
            agency, q
        )

        _, cur_value = count_value(
            qs.exclude(submission__country__country__in=CountryExclusion.objects.latest_excluded_countries(q)), 
            agency, q
        )

        def calc_val(watchlist, val):
            count_value = count_factory(value)
            countries = [
                country 
                for country in AgencyCountries.objects.get_agency_countries(agency) 
                if country not in watchlist
            ]
            
            num_countries = float(len(countries))
            return val / num_countries * 100 if num_countries > 0 else 0.0
        base_value = calc_val(CountryExclusion.objects.baseline_excluded_countries(q), base_value)
        cur_value = calc_val(CountryExclusion.objects.latest_excluded_countries(q), cur_value)

        return base_value, cur_value
    return perc_value

def equals_or_zero(val):
    def test(qs, agency_or_country, q):
        value = val.lower()
        
        qs = qs.filter(question_number=q)
        # TODO not sure what to do here
        #if len(qs) != 1:
        #    return 0, 0
        try:
            assert len(qs) == 1
            
            if qs[0].baseline_value == None:
                base_val = 0
            else:
                base_val = 100 if qs[0].baseline_value.lower() == value else 0

            if qs[0].latest_value == None:
                cur_val = 0
            else:
                cur_val = 100 if qs[0].latest_value.lower() == value else 0
            return base_val, cur_val
        except AssertionError:
            return None, None
    return test

def equals_yes_or_no(val):
    def test(qs, agency_or_country, q):
        value = val.lower()
        
        qs = qs.filter(question_number=q)
        # TODO not sure what to do here
        #if len(qs) != 1:
        #    return 0, 0
        assert len(qs) == 1
        
        if qs[0].baseline_value == None:
            base_val = ""
        else:
            base_val = "y" if qs[0].baseline_value.lower() == value else "n"

        if qs[0].latest_value == None:
            cur_val = ""
        else:
            cur_val = "y" if qs[0].latest_value.lower() == value else "n"
        return base_val, cur_val
    return test

def combine_yesnos(qs, agency_or_country, *args):
    values_baseline = []
    values_current = []
    for arg in args:
        qs1 = qs.filter(question_number=arg)
        #if qs1.count() == 0:
        #    values_baseline.append(" ")
        #    values_current.append(" ")
        #    continue
        if qs1[0].baseline_value == None:
            base_val = " "
        else: 
            base_val = "y" if qs1[0].baseline_value.lower() == "yes" else "n"

        if qs1[0].latest_value == None:
            cur_val = " "
        else:
            cur_val = "y" if qs1[0].latest_value.lower() == "yes" else "n"

        values_baseline.append(base_val)
        values_current.append(cur_val)
    return "".join(values_baseline), "".join(values_current)

def calc_numdenom(qs, agency_or_country, numq, denomq):
    cur_den = float(sum_current_values(qs.filter(question_number=denomq)))
    cur_num = float(sum_current_values(qs.filter(question_number=numq)))
    base_den = float(sum_baseline_values(qs.filter(question_number=denomq)))
    base_num = float(sum_baseline_values(qs.filter(question_number=numq)))

    base_ratio = cur_ratio = None
    if base_den > 0: base_ratio = base_num / base_den * 100
    if cur_den > 0: cur_ratio = cur_num / cur_den * 100
    return (base_ratio, cur_ratio)

def calc_one_minus_numdenom(qs, agency_or_country, numq, denomq):
    (base_ratio, cur_ratio) = calc_numdenom(qs, agency_or_country, numq, denomq)
    base_ratio = 100 - base_ratio if base_ratio != None else None
    cur_ratio = 100 - cur_ratio if cur_ratio != None else None
    
    return base_ratio, cur_ratio

def sum_values(qs, agency_or_country, *args):
    qs = qs.filter(question_number__in=args)

    cur_val = float(sum_current_values(qs))
    base_val = float(sum_baseline_values(qs))

    return (base_val, cur_val)
