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
