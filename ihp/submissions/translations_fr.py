#-*- coding: utf-8 -*-
from models import Rating
from django.template import Context, Template

gov_commentary_text = {
    "1G": {
        Rating.TICK : u"Un [space] a été signé en [space] qui se nomme [space].",
        Rating.ARROW : u"Certaines données indiquent qu’un accord ou une entente équivalente est en cours d’élaboration. L’objectif poursuivi est la mise en place de cet accord ou de cette entente avant le [space].",
        Rating.CROSS : u"Il n’y a actuellement aucun plan visant à élaborer un accord ou une entente équivalente.",
    },
    "2Ga" : {
        Rating.TICK : u"Un plan et une stratégie nationaux sectoriels de santé ont été mis en place à l’aide des objectifs et des budgets actuels qui ont été évalués conjointement.",
        Rating.ARROW : u"Mise en place de plans et d'une stratégie nationaux sectoriels de santé à l’aide des objectifs et des budgets actuels qui ont été évalués conjointement.",
        Rating.CROSS : u"Mise en place de plans et d’une stratégie nationaux sectoriels de santé sans plan d’évaluation conjointe.",

    },
    "2Gb" : {
        Rating.TICK : u"Un plan relatif aux HRH chiffré et fondé sur des preuves qui est intégré au plan de santé national a été mis en place.",
        Rating.ARROW : u"""
À la fin de %(cur_year)s, un plan relatif aux HRH chiffré et fondé sur des preuves était en cours d’élaboration. 

À la fin de %(cur_year)s, un plan relatif aux HRH chiffré et fondé sur des preuves avait été mis en place, mais n’était pas encore intégré au plan de santé national. 
""",
        Rating.CROSS : u"À la fin de %(cur_year)s, aucun plan chiffré et fondé sur des preuves relatif aux HRH n’avait été mis en place ni aucun plan visant à en élaborer un.",
    },
    "3G" : {
        "all" : u"En %(cur_year)s, %(country_name)s a alloué %(cur_val).1f%% de son budget annuel ayant été approuvé pour le secteur de la santé.",
    },
    "4G" : {
        "all" : u"En %(cur_year)s, %(one_minus_cur_val).0f%% du financement alloué au secteur de la santé a été décaissé en fonction du budget annuel ayant été autorisé.",
    },
    "5Ga" : {
        "all" : u"En %(cur_year)s, %(country_name)s a obtenu un résultat de %(cur_val).1f sur l'échelle de performance GFP/EPIN."
    },
    "5Gb" : {
        "all" : u"En %(cur_year)s, %(country_name)s a obtenu un résultat de %(cur_val).0f sur l’échelle d’évaluation à quatre points utilisée pour évaluer la performance du secteur de l’approvisionnement. "
    },
    "6G" : {
        Rating.TICK : u"En %(cur_year)s, un cadre d’évaluation de la performance transparent et contrôlable a été mis en place pour évaluer les progrès accomplis par rapport aux a) stratégies de développement national relatives à la santé et aux b) programmes sectoriels de santé.",
        Rating.ARROW : u"À la fin de %(cur_year)s, certaines données indiquaient qu’un cadre d’évaluation de la performance transparent et contrôlable était en cours d’élaboration pour évaluer les progrès accomplis par rapport aux a) stratégies de développement national relatives à la santé et aux b) programmes sectoriels de santé.",
        Rating.CROSS : u"À la fin de %(cur_year)s, aucun cadre d'évaluation de la performance transparent et contrôlable n’avait été mis en place et aucun plan visant à en développer un n’était clair ou sur le point d’être mis en œuvre.",
    },
    "7G" : {
        Rating.TICK : u"Des évaluations conjointes sont faites des progrès accomplis en ce qui concerne la mise en œuvre d’engagements dans le secteur de la santé, notamment en matière d’efficacité de l’aide.",
        Rating.ARROW : u"Des évaluations conjointes sont faites des progrès accomplis en ce qui concerne la mise en œuvre d’engagements dans le secteur de la santé, mais pas en matière d’efficacité de l’aide.",
        Rating.CROSS : u"Des évaluations conjointes sont faites des progrès accomplis en ce qui concerne la mise en œuvre d’engagements dans le secteur de la santé.",
    },
    "8G" : {
        "all" : u"En %(cur_year)s, %(cur_val).0f%% des voix dans les mécanismes nationaux de coordination du secteur de la santé (ou un organe équivalent) ont été allouées aux représentants de la société civile."
    },
}

rating_question_text = u"Une quantité insuffisante de données a été fournie pour permettre d’évaluer cette mesure de la performance standard."
rating_none_text = u"Cette mesure de la performance standard a été jugée non applicable au %s"

gov_tb2 = "%s COUNTRY SCORECARD"
gov_pc3 = "%0.1f %% allocated to health"
gov_pc4 = "%0.1f %% increase needed to meet the Abuja target (15%%)"

agency_commentary_text = {
    "1DP" : u"Un accord national IHP+ ou une entente équivalente a été signé par l’agence dans %(cur_val).0f%% des pays IHP+ dans lesquels ils sont présents. Objectif-cible = 100%%.",
    "2DPa" : u"En %(cur_year)s, %(one_minus_cur_val).0f%% de l’aide offerte dans le secteur de la santé a été rapporté par l’agence dans les budgets nationaux sectoriels de santé, %(one_minus_diff_direction)s par rapport à %(one_minus_base_val).0f%%. Objectif-cible = réduction de 50%% de l’aide n’apparaissant pas dans le budget (dont ≥ 85%% dans le budget).",
    "2DPb" : Template(u"En {{ cur_year }}, {{ cur_val|floatformat }}% du développement des capacités a été offert par l’agence par l’intermédiaire de programmes coordonnés{% if diff_direction %}, {{ diff_direction }} par rapport à {{ base_val|floatformat }}%{% endif %}. Objectif-cible = 50%."),
    "2DPc" : u"En %(cur_year)s, %(cur_val).0f%% de l’aide offerte dans le secteur de la santé a été fourni par l’agence par l’intermédiaire d’approches axées sur les programmes, %(diff_direction)s par rapport à %(base_val).0f%%. Objectif-cible = 66%%.",
    "3DP" : u"En %(cur_year)s, %(cur_val).0f%% de l’aide offerte dans le secteur de la santé a été fourni par l’agence par l’intermédiaire d’engagements pluriannuels, %(diff_direction)s par rapport à %(base_val).0f%%. Objectif-cible = 90%%.",
    "4DP" : u"En %(cur_year)s, %(cur_val).0f%% des décaissements de fonds alloués dans le secteur de la santé fournis par l’agence ont été faits conformément aux échéanciers convenus, %(diff_direction)s par rapport à %(base_val).0f%%. Objectif-cible = 90%%.",
    "5DPa" : Template(u"En {{ cur_year }}, {{ one_minus_cur_val|floatformat }}% de l’aide offerte dans le secteur de la santé a été fourni par l’agence par l’intermédiaire des systèmes d’approvisionnement nationaux{% if one_minus_diff_direction %}, {{ one_minus_diff_direction }} par rapport à {{ one_minus_base_val|floatformat }}%{% endif %}. Objectif-cible = diminution de 33% de l’aide offerte sans utiliser les systèmes d’approvisionnement nationaux (dont ≥ 80% utilisent les systèmes nationaux)."),
    "5DPb" : u"En %(cur_year)s, %(one_minus_cur_val).0f%% de l’aide offerte dans le secteur de la santé a été fourni par l’agence par l’intermédiaire des systèmes de gestion des finances publiques, %(one_minus_diff_direction)s par rapport à %(one_minus_base_val).0f%%. Objectif-cible = diminution de 33%% de l’aide offerte sans utiliser les systèmes de gestion des finances publiques (dont ≥ 80 %% utilisent les systèmes nationaux).",
    "5DPc" : u"En %(cur_year)s, le nombre d’unités de mise en œuvre de projets parallèles utilisés par l’agence dans les pays étudiés était de %(cur_val)s, %(diff_direction)s par rapport à %(base_val)s. Object-cible = réduction de 66%% du nombre d’unités de mise en œuvre de projets parallèles.",
    "6DP" : u"En %(cur_year)s, des cadres nationaux d’évaluation de la performance ont été utilisés de façon systématique par l’agence pour évaluer les progrès accomplis dans %(cur_val).0f%% les pays IHP+ où ils sont présents. Objectif-cible = 100%%.",
    "7DP" : u"En %(cur_year)s, l’agence a participé aux évaluations mutuelles des progrès accomplis dans le secteur de la santé en dans %(cur_val).0f%% des pays IHP+ lesquels ils sont présents. Objectif-cible = 100%%.",
    "8DP" : u"En %(cur_year)s, des données dans %(cur_val).0f%% des pays IHP+ indiquent que l’agence a soutenu l’engagement de la société civile envers les processus relatifs aux politiques dans le secteur de la santé. Objectif-cible = 100%%.",
}

direction_decrease = "une diminution" 
direction_increase = "soit une augmentation" 
direction_nochange = "aucun changement" 

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
    },
    "2DPb" : {
        "title" : "2DPb: Aggregate proportion of partner support for capacity-development <br/>provided through coordinated programmes in line with national strategies",
        "yAxis" : "%",
    },
    "2DPc" : {
        "title" : "2DPc: Aggregate proportion of partner support <br/>provided as programme based approaches",
        "yAxis" : "%",
    },
    "3DP"  : {
        "title" : "3DP: Aggregate proportion partner support <br/>provided through multi-year commitments",
        "yAxis" : "%",
    },
    "4DP"  : {
        "title" : "% of actual health spending planned for that year (4DP) ",
        "yAxis" : "%",
    },
    "5DPa" : {
        "title" : "5DPa: Aggregate partner use of country procurement systems", 
        "yAxis" : "%",
    },
    "5DPb" : {
        "title" : "5DPb: Aggregate partner use of country public financial management systems", 
        "yAxis" : "%",
    },
    "5DPc" : {
        "title" : "5DPc: Aggregate number of parallel Project Implementation Units (PIUs)", 
        "yAxis" : "Total number of PIUs",
    }
}

additional_graphs = {
    "2DPa" : {
        "series1" : "Health aid not on budget",
        "series2" : "Health aid reported on budget",
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
        "title" : "2DPC: Support provided as Programme Based Approach",
    },
    "3DP" : {
        "series1" : "% of multi-year commitments",
        "series2" : "% not provided through multi-year commitments",
        "title" : "% of aid provided through multi-year commitments",
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
        "title" : "5DPc: Aggregate number of parallel Project Implementation Units (PIU)s by development partner",
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
    "target" : "objectif",
    "who" : "WHO Recommended"
}

rating = "Rating2"
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
