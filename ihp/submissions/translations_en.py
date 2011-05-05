#-*- coding: utf-8 -*-
from models import Rating
from django.template import Context, Template

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
    "2DPa" : u"In %(cur_year)s %(one_minus_cur_val).0f%% of health sector aid was reported by the agency on national health sector budgets - %(one_minus_diff_direction)s from %(one_minus_base_val).0f%%. Target = 50%% reduction in aid not on budget (with ≥ 85%% on budget).",
    "2DPb" : Template("In {{ cur_year }} {{ cur_val|floatformat }}% of capacity development was provided by the agency through coordinated programmes {% if diff_direction %}- {{ diff_direction }} from {{ base_val|floatformat }}%.{% endif %} Target = 50%."),
    "2DPc" : "In %(cur_year)s %(cur_val).0f%% of health sector aid was provided by the agency through programme based approaches - %(diff_direction)s from %(base_val).0f%%. Target = 66%%.",
    "3DP" : "In %(cur_year)s %(cur_val).0f%% of health sector aid was provided by the agency through multi-year commitments - %(diff_direction)s from %(base_val).0f%%. Target = 90%%.",
    "4DP" : "In %(cur_year)s %(cur_val).0f%% of health sector aid disbursements provided by the agency were released according to agreed schedules - %(diff_direction)s from %(base_val).0f%% in %(base_year)s. Target = 90%%.",
    "5DPa" : Template("In {{ cur_year }} {{ one_minus_cur_val|floatformat }}% of health sector aid provided by the agency used country procurement systems{% if one_minus_diff_direction %} - {{ one_minus_diff_direction }} from {{ one_minus_base_val|floatformat }}%{% endif %}. Target = 33% reduction in aid not using procurement systems (with ≥ 80% using country systems)."),
    "5DPb" : u"In %(cur_year)s %(one_minus_cur_val).0f%% of health sector aid provided by the agency used national public financial management systems - %(one_minus_diff_direction)s from %(one_minus_base_val).0f%%. Target = 33%% reduction in aid not using PFM systems (with ≥ 80%% using country systems).",
    "5DPc" : "In %(cur_year)s the stock of parallel project implementation units (PIUs) used by the agency in the surveyed countries was %(cur_val)s - %(diff_direction)s from %(base_val)s. Target = 66%% reduction in stock of PIUs.",
    "6DP" : "In %(cur_year)s national performance assessment frameworks were routinely used by the agency to assess progress in %(cur_val).0f%% of IHP+ countries where they exist. Target = 100%%.",
    "7DP" : "In %(cur_year)s the agency participated in health sector mutual assessments of progress in %(cur_val).0f%% of IHP+ countries where they exist. Target = 100%%.",
    "8DP" : "In %(cur_year)s, evidence exists in %(cur_val).0f%% of IHP+ countries that the agency supported civil society engagement in health sector policy processes. Target = 100%%.",
}

direction_decrease = "a decrease" 
direction_increase = "an increase" 
direction_nochange = "no change" 

agency_graphs = {
    "2DPa" : {
        "title" : "2DPa: Change in %% of %(agency_name)s\\'s aid flows to the health sector <br>not reported on goverment\\'s budget",
        "yAxis" : "% change in funds not reported <br>on government\\'s budget",
    },
    "2DPb" : {
        "title" : "2DPb: Change in %% of capacity development provided <br>by the %(agency_name)s through coordinated programmes",
        "yAxis" : "%% of capacity development support <br/>provided through coordinated programmes",
    },
    "2DPc" : {
        "title" : "2DPc: Change in %% of aid provided through programme based approaches",
        "yAxis" : "%% of health sector aid provided <br/>through programme based approaches",
    },
    "3DP" : {
        "title" : "3DP: % of health sector funding provided through multi-year commitments",
        "yAxis" : "%% of health sector funding provided <br>through multi-year commitments",
    },
    "4DP" : {
        "title" : "4DP: Change in %% of %s\\'s health sector aid not disbursed <br>within the year for which it was scheduled",
        "yAxis" : "%% of health sector aid disbursed <br>within the year for which it was scheduled",
    },
    "5DPa" : {
        "title" : "5DPa: % change in health sector aid to the public sector not using <br/>partner countries\\' procurement systems",
        "yAxis" : "%% change in health sector aid to the public sector <br>not using partner countries\\' procurement systems",
    },
    "5DPb" : {
        "title" : "5DPb: Change in %% of %s\\'s health sector aid to the public sector <br/>not using partner countries\\' PFM systems",
        "yAxis" : "%% change in health sector aid to the public sector<br> not using partner countries\\' PFM systems",
    },
    "5DPc" : {
        "title" : "5DPc: Change in number of %s\\'s <br/>parallel project implementation (PIUs) units",
        "yAxis" : "Number parallel <br>project implementation (PIUs) units",
    },
}

country_graphs = {
    "2DPa" : {
        "title" : "2DPa: Change in aid flows to the %(country_name)s health sector <br/>not reported on government\\'s budget",
        "yAxis" : "%% change in aid flows not reported <br/>on government\\'s budget",
    },
    "2DPb" : {
        "title" : "2DPb: Change in %% of capacity development support provided to %(country_name)s <br/>health sector through coordinated programmes",
        "yAxis" : "%% of capacity development support <br/>provided through coordinated programmes",
    },
    "2DPc" : {
        "title" : "2DPc: Change in %% of health sector aid provided to %(country_name)s <br/>through programme based approaches",
        "yAxis" : "%% of health sector aid provided <br/>through programme based approaches",
    },
    "3DP" : {
        "title" : "3DP: Change in %% of health sector aid provided to %(country_name)s<br/> through multi-year commitments",
        "yAxis" : "%% of health sector funding provided <br>through multi-year commitments",
    },
    "4DP" : {
        "title" : "4DP: Change in %% of health sector aid to %(country_name)s <br/>disbursed within the year for which it was scheduled",
        "yAxis" : "%% of health sector aid disbursed <br>within the year for which it was scheduled",
    },
    "5DPa" : {
        "title" : "5DPa: %% change in health sector aid to %(country_name)s public sector <br/>not using country procurement systems.",
        "yAxis" : "%% change in health sector aid to the public sector <br>not using partner countries\\' procurement systems",
    },
    "5DPb" : {
        "title" : "5DPb: %% change in health sector aid to %(country_name)s public sector<br/> not using country PFM systems.",
        "yAxis" : "%% change in health sector aid to the public sector<br> not using partner countries\\' PFM systems",
    },
    "5DPc" : {
        "title" : "5DPc: Number of agency PIUs in place in %(country_name)s",
        "yAxis" : "Number parallel <br>project implementation (PIUs) units",
    },
}

highlevel_graphs = {
    "2DPa" : {
        "title" : "2DPa: Aggregate proportion of partner support reported on national budgets",
        "yAxis" : "%",
        "subtitle" : "* Data with baseline values from 2008 are not included",
    },
    "2DPb" : {
        "title" : "2DPb: Aggregate proportion of partner support for capacity-development <br/>provided through coordinated programmes in line with national strategies",
        "yAxis" : "%",
        "subtitle" : "* Data with baseline values from 2008 are not included",
    },
    "2DPc" : {
        "title" : "2DPc: Aggregate proportion of partner support <br/>provided as programme based approaches",
        "yAxis" : "%",
        "subtitle" : "* Data with baseline values from 2008 are not included",
    },
    "3DP"  : {
        "title" : "3DP: Aggregate proportion partner support <br/>provided through multi-year commitments",
        "yAxis" : "%",
        "subtitle" : "* Data with baseline values from 2008 are not included",
    },
    "4DP"  : {
        "title" : "4DP: % of actual health spending planned for that year",
        "yAxis" : "%",
        "subtitle" : "* Data with baseline values from 2008 are not included",
    },
    "5DPa" : {
        "title" : "5DPa: Aggregate partner use of country procurement systems", 
        "yAxis" : "%",
        "subtitle" : "* Data with baseline values from 2008 are not included",
    },
    "5DPb" : {
        "title" : "5DPb: Aggregate partner use of country public financial management systems", 
        "yAxis" : "%",
        "subtitle" : "* Data with baseline values from 2008 are not included",
    },
    "5DPc" : {
        "title" : "5DPc: Aggregate number of parallel Project Implementation Units (PIUs)", 
        "yAxis" : "Total number of PIUs",
        "subtitle" : "* Data with baseline values from 2008 are not included",
    }
}

additional_graphs = {
    "2DPa" : {
        "series1" : "Health aid reported on budget",
        "series2" : "Health aid not on budget",
        "title" : "2DPa: Proportion of partner health aid on country budget",
    },
    "2DPb" : {
        "series1" : "Support coordinated and in line",
        "series2" : "Support not coordinated and in line",
        "title" : "2DPb: Support for capacity development that is coordinated <br/>and in line with national strategies",
    },
    "2DPc" : {
        "series1" : "% of health aid as Programme Based Approach",
        "series2" : "% of health aid not as Programme Based Approach",
        "title" : "2DPc: Support provided as Programme Based Approach",
    },
    "3DP" : {
        "series1" : "% of multi-year commitments",
        "series2" : "% not provided through multi-year commitments",
        "title" : "3DP: % of aid provided through multi-year commitments",
    },
    "4DP" : {
        "series1" : "% of aid disbursed within the year for which it was scheduled",
        "series2" : "% of aid not disbursed within the year for which it was scheduled",
        "title" : "4DP: % of health sector aid disbursed within the year for which it was scheduled",
    },
    "5DPa" : {
        "series1" : "Health aid using procurement systems",
        "series2" : "Health aid not using procurement systems",
        "title" : "5DPa: Partner use of country procurement systems",
    },
    "5DPb" : {
        "series1" : "Health aid using PFM systems",
        "series2" : "Health aid not using PFM systems",
        "title" : "5DPb: Partner use of country public financial management systems",
    },
    "5DPc" : {
        "yAxis" : "Total number of PIUs",
        "title" : "5DPc: Aggregate number of parallel Project Implementation Units (PIU)s<br/> by development partner",
    }
}

projection_graphs = {
    "2DPa" : {
        "title" : "Projected time required to meet On Budget target <br>(based on current levels of performance):2007 Baseline",
    },
    "5DPb" : {
        "title" : "Projected time required to meet PFM target <br>(based on current levels of performance):2007 Baseline",
    }
}

government_graphs = {
    "3G" : {
        "title" : "3G: Proportion of national budget allocated to health",
        "subtitle" : "* Target for Nepal is 10%",
    },
    "4G" : {
        "title" : "4G: Actual disbursement of government health budgets",
    },
    "health_workforce" : {
        "title" : "Proportion of health sector budget spent on Human Resources for Health (HRH)",
    },
    "outpatient_visits" : {
        "title" : "Number of Outpatient Department Visits per 10,000 population",
    },
    "skilled_medical" : {
        "title" : "Number of skilled medical personnel per 10,000 population",
    },
    "health_budget" : {
        "title" : "% of national budget is allocated to health (IHP+ Results data)",
    }
}

target_language = {
    "target" : "target",
    "who" : "WHO Recommended"
}

rating = "Rating"
country_data = "Country Data"
agency = "Agency"
by_agency_title = "%s Data across IHP+ Countries"
by_country_title = "Development Partners in %s"
spm = "SPM"
standard_performance_measure = "Standard Performance Measure"

spm_map = {
    #"1DP" : "Proportion of ihp+ countries in which the partner has signed commitment to (or documented support for) the ihp+ country compact, or equivalent agreement.",
    "1DP" : "Partner has signed commitment to (or documented support for) the IHP+ country compact, or equivalent agreement, where they exist.",
    "2DPa" : "Percent of aid flows to the health sector that is reported on national health sector budgets.",
    "2DPb" : "Percent of current capacity-development support provided through coordinated programmes consistent with national plans/strategies for the health sector.",
    "2DPc" : "Percent of health sector aid provided as programme based approaches.",
    "3DP" : "Percent of health sector aid provided through multi-year commitments.",
    "4DP" : "Percent of health sector aid disbursements released according to agreed schedules in annual or multi-year frameworks.",
    "5DPa" : "Percent of health sector aid that uses country procurement systems.",
    "5DPb" : "Percent of health sector aid that uses public financial management systems.",
    "5DPc" : "Number of parallel project implementation units (pius) per country.",
    #"6DP" : "Proportion of countries in which agreed, transparent and monitorable performance assessment frameworks are being used to assess progress in the health sector.",
    "6DP" : "Partner uses the single national performance assessment framework, where they exist, as the primary basis to assess progress (of support to health sector).",
    #"7DP" : "Proportion of countries where mutual assessments have been made of progress implementing commitments in the health sector, including on aid effectiveness.",
    "7DP" : "Partner has participated in mutual assessment of progress implementing commitments in the health sector, including on aid effectiveness, if a mutual assessment process exists.",
    "8DP" : "Evidence of support for civil society to be actively represented in health sector policy processes - including health sector planning, coordination & review mechanisms.",
}

gov_spm_map = {
    "1G" : "IHP+ Compact or equivalent mutual agreement in place.",
    "2Ga1" : "National Health Sector Plans/Strategy in place with current targets & budgets.",
    "2Ga2" : "National Health Sector Plans/Strategy in place with current targets & budgets that have been jointly assessed.",
    "2Gb" : "Costed and evidence-based HRH plan in place that is integrated with the national health plan.",
    "3G" : "Proportion of public funding allocated to health.",
    "4G" : "Proportion of health sector funding disbursed against the approved annual budget.",
    "5Ga" : "Public Financial Management systems for the health sector either (a) adhere to broadly accepted good practices or (b) have a reform programme in place to achieve these.",
    "5Gb" : "Country Procurement systems for the health sector either (a) adhere to broadly accepted good practices or (b) have a reform programme in place to achieve these.",
    "6G" : "An agreed transparent and monitorable performance assessment framework is being used to assess progress in the health sector.",
    "7G" : "Mutual Assessments, such as Joint Annual Health Sector Reviews, have been made of progress implementing commitments in the health sector, including on aid effectiveness.",
    "8G" : "Evidence that Civil Society is actively represented in health sector policy processes - including Health Sector planning, coordination & review mechanisms.",
}
        
indicator = "Indicator"
base_val = "base val"
cur_val = "cur val"
perc_change = "% change"

dp_table_footnote = """
<b>Important information about these ratings:</b><br/>
<em>Notes on methods:</em>
<ul>
    <li>The methodology used to undertake this exercise is available at – <a href="http://www.ihpresults.com/how/methodology/">www.ihpresults.com/how/methodology</a></li>
    <li>Standard Performance Measures (SPMs) for Country Governments and Development Partners, along with their associated targets, are available at – <a href="http://www.ihpresults.com/how/methodology/spms">www.ihpresults.com/how/methodology/spms</a></li>
    <li>The Criteria used to reach the above ratings are available at – <a href="http://www.ihpresults.net/how/methodology/rating/">www.ihpresults.net/how/methodology/rating/</a></li>
    <li>Detailed guidance on key terms and definitions is available at – <a href="http://www.ihpresults/how/data_collection">www.ihpresults/how/data_collection</a></li>
    <li>The latest available data for this exercise was from 2009. Progress may have been made in 2010 that is not reported here.</li>
    <li>Development Partner data has been aggregated to produce ratings for individual Development Partner scorecards. For more a more detailed explanation on this see – <a href="http://www.ihpresults.net/how/limitations/">www.ihpresults.net/how/limitations</a></li>
<li>SPM 5DPb: 5 countries’ data is not counted for this SPM. For more a more detailed explanation on this see – <a href="http://www.ihpresults.net/how/limitations/">www.ihpresults.net/how/limitations/</a></li>
</ul>
<br/>
<em>Notes on interpretation:</em><br/>
The exercise has been largely self-reported, and it has been difficult to find opportunities to triangulate data without imposing significant transaction costs. 
<ul>
    <li>The consistency of interpretation for key terms and definitions between participating agencies may vary within this country. This could affect the comparability of results.</li>
    <li>For Development Partner SPM ratings it is important to note that the country context has a significant impact on the extent to which progress can be made by Development Partners for each of the Standard Performance Measures. Comparisons of performance across the country offices of a single agency should be made with this in mind.
    </li>
</ul>
"""

country_table_footnote = """
<b>Important information about these ratings:</b><br/>
<em>Notes on methods:</em>
<ul>
    <li>The methodology used to undertake this exercise is available at – <a href="http://www.ihpresults.com/how/methodology/">www.ihpresults.com/how/methodology</a></li>
    <li>Standard Performance Measures (SPMs) for Country Governments and Development Partners, along with their associated targets, are available at – <a href="http://www.ihpresults.com/how/methodology/spms">www.ihpresults.com/how/methodology/spms</a></li>
    <li>The Criteria used to reach the above ratings are available at – <a href="http://www.ihpresults.net/how/methodology/rating/">www.ihpresults.net/how/methodology/rating/</a></li>
    <li>Detailed guidance on key terms and definitions is available at – <a href="http://www.ihpresults/how/data_collection">www.ihpresults/how/data_collection</a></li>
    <li>The latest available data for this exercise was from 2009. Progress may have been made in 2010 that is not reported here.</li>
    <li>Development Partner data has been aggregated to produce ratings for individual Development Partner scorecards. For more a more detailed explanation on this see – <a href="http://www.ihpresults.net/how/limitations/">www.ihpresults.net/how/limitations</a></li>
<li>SPM 5DPb: 5 countries’ data is not counted for this SPM. For more a more detailed explanation on this see – <a href="http://www.ihpresults.net/how/limitations/">www.ihpresults.net/how/limitations/</a></li>
</ul>
<br/>
<em>Notes on interpretation:</em><br/>
The exercise has been largely self-reported, and it has been difficult to find opportunities to triangulate data without imposing significant transaction costs. 
<ul>
    <li>The consistency of interpretation for key terms and definitions between participating agencies may vary within this country. This could affect the comparability of results.</li>
    </li>
</ul>
"""
