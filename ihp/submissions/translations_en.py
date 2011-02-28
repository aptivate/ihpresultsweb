from models import Rating

# Country Scorecard
gov_commentary_text = {
    "1G": {
        Rating.TICK : "An [space] was signed in [space] called [space].",
        Rating.ARROW : "There is evidence of a Compact or equivalent agreement under development. The aim is to have this in place by [space].",
        Rating.CROSS : "There are no current plans to develop a Compact or equivalent agreement.",
    },
    "2Ga" : {
        Rating.TICK : "A National Health Sector Plan/Strategy is in place with current targets & budgets that have been jointly assessed.",
        Rating.ARROW : "National Health Sector Plans/Strategy in place with current targets & budgets with evidence of plans for joint assessment.",
        Rating.CROSS : "National Health Sector Plans/Strategy in place with no plans for joint assessment. Target = National Health Sector Plans/Strategy in place with current targets & budgets that have been jointly assessed.",

    },
    "2Gb" : {
        Rating.TICK : "There is currently a costed and evidence based HRH plan in place that is integrated with the national health plan.",
        Rating.ARROW : """At the end of %(cur_year)s a costed and evidence based HRH plan was under development. 

At the end of %(cur_year)s a costed and evidence based HRH plan was in place but not yet integrated with the national health plan. """,
        Rating.CROSS : "At the end of %(cur_year)s there was no costed and evidence based HRH plan in place, or plans to develop one. ",
    },
    "3G" : {
        "all" : "In %(cur_year)s %(country_name)s allocated %(cur_val).1f%% of its approved annual national budget to health.",
    },
    "4G" : {
        "all" : "In %(cur_year)s, %(one_minus_cur_val).0f%% of health sector funding was disbursed against the approved annual budget.",
    },
    "5Ga" : {
        "all" : "In %(cur_year)s, %(country_name)s achieved a score of %(cur_val).1f on the PFM/CPIA scale of performance."
    },
    "5Gb" : {
        "all" : "In %(cur_year)s, %(country_name)s achieved a score of %(cur_val).0f on the four point scale used to assess performance in the the procurement sector."
    },
    "6G" : {
        Rating.TICK : "In %(cur_year)s there was a transparent and monitorable performance assessment framework in place to assess progress against (a) the national development strategies relevant to health and (b) health sector programmes.",
        Rating.ARROW : "At the end of %(cur_year)s there was evidence that a transparent and monitorable performance assessment framework was under development to assess progress against (a) the national development  strategies relevant to health and (b) health sector programmes.",
        Rating.CROSS : "At the end of %(cur_year)s there was no transparent and monitorable performance assessment framework in place and no plans to develop one were clear or being implemented.",
    },
    "7G" : {
        Rating.TICK : "Mutual assessments are being made of progress implementing commitments in the health sector, including on aid effectiveness.",
        Rating.ARROW : "Mutual assessments are being made of progress implementing commitments in the health sector, but not on aid effectiveness.",
        Rating.CROSS : "Mutual assessments are not being made of progress implementing commitments in the health sector.",
    },
    "8G" : {
        "all" : "In %(cur_year)s %(cur_val).0f%% of seats in the Health Sector Coordination Mechanism (or equivalent body) were allocated to Civil Society representatives."
    },
}

rating_question_text = "Insufficient data has been provided to enable a rating for this Standard Performance Measure."
rating_none_text = "This Standard Performance Measure was deemed not applicable to %s."
gov_tb2 = "%s COUNTRY SCORECARD"
gov_pc3 = "%0.1f %% allocated to health"
gov_pc4 = "%0.1f %% increase needed to meet the Abuja target (15%%)"

agency_commentary_text = {
    "1DP" : "An IHP+ Country Compact or equivalent has been signed by the agency in %(cur_val).0f%% of IHP+ countries where they exist. Target = 100%%.",
    "2DPa" : "In %(cur_year)s %(one_minus_cur_val).0f%% of health sector aid was reported by the agency on national health sector budgets - %(one_minus_diff_direction)s from %(one_minus_base_val).0f%%. Target = 50%% reduction in aid not on budget (with > 85%% on budget).",
    "2DPb" :"In %(cur_year)s %(cur_val).0f%% of capacity development was provided by the agency through coordinated programmes - %(diff_direction)s from %(base_val).0f%%. Target = 50%%.",
    "2DPc" : "In %(cur_year)s %(cur_val).0f%% of health sector aid was provided by the agency through programme based approaches - %(diff_direction)s from %(base_val).0f%%. Target = 66%%.",
    "3DP" : "In %(cur_year)s %(cur_val).0f%% of health sector aid was provided by the agency through multi-year commitments - %(diff_direction)s from %(base_val).0f%%. Target = 90%%.",
    "4DP" : "In %(cur_year)s %(cur_val).0f%% of health sector aid disbursements provided by the agency were released according to agreed schedules - %(one_minus_diff_direction)s from %(base_val).0f%% in %(base_year)s. Target = 90%%.",
    "5DPa" : "In %(cur_year)s %(one_minus_cur_val).0f%% of health sector aid provided by the agency used country procurement systems - %(one_minus_diff_direction)s from %(one_minus_base_val).0f%%. Target = 33%% reduction in aid not using procurement systems.",
    "5DPb" : "In %(cur_year)s %(one_minus_cur_val).0f%% of health sector aid provided by the agency used national public financial management systems - %(one_minus_diff_direction)s from %(one_minus_base_val).0f%%. Target = 33%% reduction in aid not using PFM systems.",
    "5DPc" : "In %(cur_year)s the stock of parallel project implementation units (PIUs) used by the agency in the surveyed countries was %(cur_val)s - %(diff_direction)s from %(base_val)s. Target = 66%% reduction in stock of PIUs.",
    "6DP" : "In %(cur_year)s national performance assessment frameworks were routinely used by the agency to assess progress in %(cur_val).0f%% of IHP+ countries where they exist. Target = 100%%.",
    "7DP" : "In %(cur_year)s the agency participated in health sector mutual assessments of progress in %(cur_val).0f%% of IHP+ countries where they exist. Target = 100%%.",
    "8DP" : "In %(cur_year)s, evidence exists in %(cur_val).0f%% of IHP+ countries that the agency supported civil society engagement in health sector policy processes. Target = 100%%.",
}

