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

rating_question_text = u"Une quantité insuffisante de données a été fournie pour permettre d’évaluer cette mesure de la performance standard."
rating_none_text = u"Cette mesure de la performance standard a été jugée non applicable au %s"

gov_tb2 = "%s COUNTRY SCORECARD"
gov_pc3 = "%0.1f %% allocated to health"
gov_pc4 = "%0.1f %% increase needed to meet the Abuja target (15%%)"

agency_commentary_text = {
    "1DP" : u"Un accord national IHP+ ou une entente équivalente a été signé par l’agence dans %(cur_val).0f%% des pays IHP+ dans lesquels ils sont présents. Objectif-cible = 100%%.",
    "2DPa" : u"En %(cur_year)s, %(one_minus_cur_val).0f%% de l’aide offerte dans le secteur de la santé a été rapporté par l’agence dans les budgets nationaux sectoriels de santé, %(one_minus_diff_direction)s par rapport à %(one_minus_base_val).0f%%. Objectif-cible = réduction de 50%% de l’aide n’apparaissant pas dans le budget (dont > 85%% dans le budget).",
    "2DPb" : Template("En {{ cur_year }}, {{ cur_val|floatformat }}% du développement des capacités a été offert par l’agence par l’intermédiaire de programmes coordonnés{% if diff_direction %}, {{ diff_direction }} par rapport à {{ base_val|floatformat }}%{% endif %}. Objectif-cible = 50%%."),
    "2DPc" : u"En %(cur_year)s, %(cur_val).0f%% de l’aide offerte dans le secteur de la santé a été fourni par l’agence par l’intermédiaire d’approches axées sur les programmes, %(diff_direction)s par rapport à %(base_val).0f%%. Objectif-cible = 66%%.",
    "3DP" : u"En %(cur_year)s, %(cur_val).0f%% de l’aide offerte dans le secteur de la santé a été fourni par l’agence par l’intermédiaire d’engagements pluriannuels, %(diff_direction)s par rapport à %(base_val).0f%%. Objectif-cible = 90%%.",
    "4DP" : u"En %(cur_year)s, %(cur_val).0f%% des décaissements de fonds alloués dans le secteur de la santé fournis par l’agence ont été faits conformément aux échéanciers convenus, %(diff_direction)s par rapport à %(base_val).0f%%. Objectif-cible = 90%%.",
    "5DPa" : u"En %(cur_year)s, %(one_minus_cur_val).0f%% de l’aide offerte dans le secteur de la santé a été fourni par l’agence par l’intermédiaire des systèmes d’approvisionnement nationaux, %(one_minus_diff_direction)s par rapport à %(one_minus_base_val).0f%%. Objectif-cible = diminution de 33%% de l’aide offerte sans utiliser les systèmes d’approvisionnement nationaux (dont ≥ 80%% utilisent les systèmes nationaux).",
    "5DPb" : u"En %(cur_year)s, %(one_minus_cur_val).0f%% de l’aide offerte dans le secteur de la santé a été fourni par l’agence par l’intermédiaire des systèmes de gestion des finances publiques, %(one_minus_diff_direction)s par rapport à %(one_minus_base_val).0f%%. Objectif-cible = diminution de 33%% de l’aide offerte sans utiliser les systèmes de gestion des finances publiques (dont ≥ 80 %% utilisent les systèmes nationaux).",
    "5DPc" : u"En %(cur_year)s, le nombre d’unités de mise en œuvre de projets parallèles utilisés par l’agence dans les pays étudiés était de %(cur_val)s, %(diff_direction)s par rapport à %(base_val)s. Object-cible = réduction de 66%% du nombre d’unités de mise en œuvre de projets parallèles.",
    "6DP" : u"En %(cur_year)s, des cadres nationaux d’évaluation de la performance ont été utilisés de façon systématique par l’agence pour évaluer les progrès accomplis %(cur_val).0f%% dans les pays IHP+ où ils sont présents. Objectif-cible = 100%%.",
    "7DP" : u"En %(cur_year)s, l’agence a participé aux évaluations mutuelles des progrès accomplis dans le secteur de la santé en %(cur_val).0f%% des pays IHP+ dans lesquels ils sont présents. Objectif-cible = 100%%.",
    "8DP" : u"En %(cur_year)s, des données dans %(cur_val).0f%% des pays IHP+ indiquent que l’agence a soutenu l’engagement de la société civile envers les processus relatifs aux politiques dans le secteur de la santé. Objectif-cible = 100%%.",
}

direction_decrease = "une diminution" 
direction_increase = "soit une augmentation" 
direction_nochange = "aucun changement" 
