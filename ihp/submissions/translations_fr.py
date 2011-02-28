#-*- coding: utf-8 -*-
from models import Rating

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
        "all" : u"En %(cur_year)s, %(country_name)s a obtenu un résultat de %(cur_val) sur l'échelle de performance GFP/EPIN."
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

rating_question_text = "Insufficient data has been provided to enable a rating for this Standard Performance Measure."
rating_none_text = "This Standard Performance Measure was deemed not applicable to %s."

gov_tb2 = "%s COUNTRY SCORECARD"
gov_pc3 = "%0.1f %% allocated to health"
gov_pc4 = "%0.1f %% increase needed to meet the Abuja target (15%%)"

agency_commentary_text = {
    "1DP" : "An IHP+ Country Compact or equivalent has been signed by the agency in %(cur_val).0f%% of IHP+ countries where they exist. Objectif-cible = 100%% ",
    "2DPa" : "In %(cur_year)s %(one_minus_cur_val).0f%% of health sector aid was reported by the agency on national health sector budgets - %(one_minus_diff_direction)s from %(one_minus_base_val).0f%%. Objectif-cible = Réduire l’écart de moitié – Réduire de moitié la part de l’aide dont le versement n’est pas effectué au cours de l’exercice budgétaire pour lequel il est prévu. ",
    "2DPb" :"In %(cur_year)s %(cur_val).0f%% of capacity development was provided by the agency through coordinated programmes - %(diff_direction)s from %(base_val).0f%%. Objectif-cible = 50%%. ",
    "2DPc" : "In %(cur_year)s %(cur_val).0f%% of health sector aid was provided by the agency through programme based approaches - %(diff_direction)s from %(base_val).0f%%. Objectif-cible = 66%%. ",
    "3DP" : "In %(cur_year)s %(cur_val).0f%% of health sector aid was provided by the agency through multi-year commitments - %(diff_direction)s from %(base_val).0f%%. Objectif-cible = 90%%. ",
    "4DP" : "In %(cur_year)s %(cur_val).0f%% of health sector aid disbursements provided by the agency were released according to agreed schedules - %(one_minus_diff_direction)s from %(base_val).0f%% in %(base_year)s. Objectif-cible = 90%%. ",
    "5DPa" : "In %(cur_year)s %(one_minus_cur_val).0f%% of health sector aid provided by the agency used country procurement systems - %(one_minus_diff_direction)s from %(one_minus_base_val).0f%%. Objectif-cible = Réduire d’un tiers la part des apports au secteur public qui ne fait pas appel aux systèmes de passation des marchés des pays partenaires. ",
    "5DPb" : "In %(cur_year)s %(one_minus_cur_val).0f%% of health sector aid provided by the agency used national public financial management systems - %(one_minus_diff_direction)s from %(one_minus_base_val).0f%%. Objectif-cible = Réduire d’un tiers la part des apports au secteur public qui ne fait pas  appel aux systèmes de gestion des finances publiques des pays partenaires. ",
    "5DPc" : "In %(cur_year)s the stock of parallel project implementation units (PIUs) used by the agency in the surveyed countries was %(cur_val)s - %(diff_direction)s from %(base_val)s. Objectif-cible = Réduire des deux tiers le nombre d’unités parallèles de mise en oeuvre des projets.",
    "6DP" : "In %(cur_year)s national performance assessment frameworks were routinely used by the agency to assess progress in %(cur_val).0f%% of IHP+ countries where they exist. Objectif-cible = 100%%.",
    "7DP" : "In %(cur_year)s the agency participated in health sector mutual assessments of progress in %(cur_val).0f%% of IHP+ countries where they exist. Objectif-cible = 100%%.",
    "8DP" : "In %(cur_year)s, evidence exists in %(cur_val).0f%% of IHP+ countries that the agency supported civil society engagement in health sector policy processes. Objectif-cible = 100%%.",
}
