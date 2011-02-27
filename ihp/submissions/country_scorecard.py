from math import fabs
import models
import translations
import target
from indicators import calc_country_indicators
from utils import none_num, fformat_none, fformat_front, fformat_two
from indicators import NA_STR
import traceback

def calc_change(val1, val2):
    try:
        if val1 == None or val2 == None:
            return None, None
        val1 = float(val1)
        val2 = float(val2)
        val = val1 / val2 - 1
        if val < 0:
            dir = "down"
        elif val > 0:
            dir = "up"
        else:
            dir = "no change"
        return fabs(val) * 100, dir
    except ValueError:
        return None, None

def get_country_scorecard_data(country, language):

    submissions = country.submission_set.filter(type="Gov")
    assert submissions.count() == 1

    submission = submissions.all()[0] 

    # Do not process if there are no questions
    if submission.govquestion_set.all().count() == 0: 
        raise Exception("Possible incomplete submission")
    
    country_data = calc_country_ratings(country, language)
    
    for indicator, d in country_data.items():
        old_comments = d["comments"]
        comments = []
        for question_number, country, comment in old_comments:
            comments.append("%s ] %s" % (question_number, comment))
        d["comments"] = "\n".join([comment for comment in comments if comment])
        ##d["key"] = "%s_%s" % (country, indicator)
    ##country_data["np"], country_data["p"] = get_agency_progress(country)
    ##country_data["questions"] = {}

    # Add indicators
    ##indicators = calc_country_indicators(country)
    ##country_data["indicators"] = {}
    ##for indicator in indicators:
    ##    ind = country_data["indicators"][indicator] = {}
    ##    data = indicators[indicator][0]
    ##    ind["baseline_value"] = none_num(data[0])
    ##    ind["baseline_year"] = data[1]
    ##    ind["latest_value"] = none_num(data[2])
    ##    ind["latest_year"] = data[3]

    ###TODO hack
    ##if country_data["indicators"]["3G"]["latest_value"] != NA_STR:
    ##    country_data["indicators"]["3G"]["hs_budget_gap"] = 15 - country_data["indicators"]["3G"]["latest_value"]
    ##else:
    ##    country_data["indicators"]["3G"]["hs_budget_gap"] = None
    ##country_data["indicators"]["other"] = {}

    ### Add agency submissions
    ##agencies = AgencyCountries.objects.get_country_agencies(country)
    ##aval = country_data["agencies"] = {}
    ##for agency in agencies:
    ##    aval[agency.agency] = {}
    ##    for question in DPQuestion.objects.filter(submission__agency=agency, submission__country=country):
    ##        qvals = aval[agency.agency][question.question_number] = {}
    ##        qvals["baseline_year"] = question.baseline_year
    ##        qvals["baseline_value"] = question.base_val
    ##        qvals["latest_year"] = question.latest_year
    ##        qvals["latest_value"] = question.cur_val
    ##        qvals["comments"] = question.comments

    ##for question in GovQuestion.objects.filter(submission__country=country):
    ##    qvals = country_data["questions"][question.question_number] = {}
    ##    qvals["baseline_year"] = question.baseline_year
    ##    qvals["latest_year"] = question.latest_year
    ##    qvals["comments"] = question.comments

    ##    qvals["baseline_value"] = none_num(question.base_val)
    ##    qvals["latest_value"] = none_num(question.cur_val)

    ##questions = country_data["questions"]

    ##other_indicators = country_data["indicators"]["other"]
    ##baseline_denom = questions["18"]["baseline_value"] / 10000.0
    ##latest_denom = questions["18"]["latest_value"] / 10000.0

    ### Outpatient Visits
    ##other_indicators["outpatient_visits_baseline"] = questions["19"]["baseline_value"] / baseline_denom
    ##other_indicators["outpatient_visits_latest"] = questions["19"]["latest_value"] / latest_denom
    ##other_indicators["outpatient_visits_change"], other_indicators["outpatient_visits_change_dir"] = calc_change(other_indicators["outpatient_visits_latest"], other_indicators["outpatient_visits_baseline"])

    ### Skilled Personnel
    ##other_indicators["skilled_personnel_baseline"] = questions["17"]["baseline_value"] / baseline_denom
    ##other_indicators["skilled_personnel_latest"] = questions["17"]["latest_value"] / latest_denom
    ##other_indicators["skilled_personnel_change"], other_indicators["skilled_personnel_change_dir"] = calc_change(other_indicators["skilled_personnel_latest"], other_indicators["skilled_personnel_baseline"])

    ### Health Workforce
    ##other_indicators["health_workforce_perc_of_budget_baseline"] = questions["20"]["baseline_value"] / questions["7"]["baseline_value"]
    ##other_indicators["health_workforce_perc_of_budget_latest"] = questions["20"]["latest_value"] / questions["7"]["latest_value"]
    ##other_indicators["health_workforce_spent_change"], other_indicators["health_workforce_spent_change_dir"] = calc_change(questions["20"]["latest_value"], questions["20"]["baseline_value"])

    ##other_indicators["pfm_diff"] = questions["9"]["latest_value"] - questions["9"]["baseline_value"]
    
    ##def sum_agency_values(question_number, field):
    ##    sum = 0
    ##    for agency in aval:
    ##        if question_number in aval[agency]:
    ##            try:
    ##                sum += float(aval[agency][question_number][field])
    ##            except ValueError:
    ##                pass
    ##    return sum

    ##coordinated_programmes = sum_agency_values("5", "latest_value") - sum_agency_values("4", "latest_value")
    ##if coordinated_programmes > 0.51:
    ##    other_indicators["coordinated_programmes"] = Rating.TICK
    ##elif coordinated_programmes >= 0.11:
    ##    other_indicators["coordinated_programmes"] = Rating.ARROW
    ##else:
    ##    other_indicators["coordinated_programmes"] = Rating.CROSS

    return country_data

def get_country_questions(country):
    questions = {}
    for question in models.GovQuestion.objects.filter(submission__country=country):
        qvals = questions[question.question_number] = {}
        qvals["baseline_year"] = question.baseline_year
        qvals["latest_year"] = question.latest_year
        qvals["comments"] = question.comments

        qvals["baseline_value"] = none_num(question.base_val)
        qvals["latest_value"] = none_num(question.cur_val)
    return questions

def get_agency_values(country):
    # Add agency submissions
    aval = {}
    for agency in country.agencies:
        aval[agency.agency] = {}
        for question in models.DPQuestion.objects.filter(submission__agency=agency, submission__country=country):
            qvals = aval[agency.agency][question.question_number] = {}
            qvals["baseline_year"] = question.baseline_year
            qvals["baseline_value"] = question.base_val
            qvals["latest_year"] = question.latest_year
            qvals["latest_value"] = question.cur_val
            qvals["comments"] = question.comments
    return aval

def get_country_indicators(country, questions, agencies_data):
    indicator_data = calc_country_indicators(country)
    indicators = {}
    for indicator in indicator_data:
        ind = indicators[indicator] = {}
        data = indicator_data[indicator][0]
        ind["baseline_value"] = none_num(data[0])
        ind["baseline_year"] = data[1]
        ind["latest_value"] = none_num(data[2])
        ind["latest_year"] = data[3]

    if indicators["3G"]["latest_value"] != NA_STR:
        indicators["3G"]["hs_budget_gap"] = 15 - indicators["3G"]["latest_value"]
    else:
        indicators["3G"]["hs_budget_gap"] = None

    indicators["other"] = {}

    other_indicators = indicators["other"]
    baseline_denom = questions["18"]["baseline_value"] / 10000.0
    latest_denom = questions["18"]["latest_value"] / 10000.0

    # Outpatient Visits
    other_indicators["outpatient_visits_baseline"] = questions["19"]["baseline_value"] / baseline_denom
    other_indicators["outpatient_visits_latest"] = questions["19"]["latest_value"] / latest_denom
    other_indicators["outpatient_visits_change"], other_indicators["outpatient_visits_change_dir"] = calc_change(other_indicators["outpatient_visits_latest"], other_indicators["outpatient_visits_baseline"])

    # Skilled Personnel
    other_indicators["skilled_personnel_baseline"] = questions["17"]["baseline_value"] / baseline_denom
    other_indicators["skilled_personnel_latest"] = questions["17"]["latest_value"] / latest_denom
    other_indicators["skilled_personnel_change"], other_indicators["skilled_personnel_change_dir"] = calc_change(other_indicators["skilled_personnel_latest"], other_indicators["skilled_personnel_baseline"])

    # Health Workforce
    other_indicators["health_workforce_perc_of_budget_baseline"] = questions["20"]["baseline_value"] / questions["7"]["baseline_value"]
    other_indicators["health_workforce_perc_of_budget_latest"] = questions["20"]["latest_value"] / questions["7"]["latest_value"]
    other_indicators["health_workforce_spent_change"], other_indicators["health_workforce_spent_change_dir"] = calc_change(questions["20"]["latest_value"], questions["20"]["baseline_value"])

    other_indicators["pfm_diff"] = questions["9"]["latest_value"] - questions["9"]["baseline_value"]

    def sum_agency_values(question_number, field):
        sum = 0
        for agency in agencies_data:
            if question_number in agencies_data[agency]:
                try:
                    sum += float(agencies_data[agency][question_number][field])
                except ValueError:
                    pass
        return sum

    coordinated_programmes = sum_agency_values("5", "latest_value") - sum_agency_values("4", "latest_value")
    if coordinated_programmes > 0.51:
        other_indicators["coordinated_programmes"] = models.Rating.TICK
    elif coordinated_programmes >= 0.11:
        other_indicators["coordinated_programmes"] = models.Rating.ARROW
    else:
        other_indicators["coordinated_programmes"] = models.Rating.CROSS

    return indicators

#TODO Used by publicweb
def get_country_export_data(country, language=None):
    """
    Return all the data that is required for the country scorecard
    """
    language = language or models.Language.objects.get(language="English")
    translation = translations.get_translation(language)

    data = target.calc_country_ratings(country, language)
    data["questions"] = get_country_questions(country)
    data["agencies"] = get_agency_values(country)
    data["indicators"] = get_country_indicators(country, data["questions"], data["agencies"])
    data["np"], data["p"] = target.get_agency_progress(country)
    ratings, _ = models.GovScorecardRatings.objects.get_or_create(country=country)
    comments_override, _ = models.CountryScorecardOverrideComments.objects.get_or_create(
        country=country, language=language
    )

    try:
        data["ER1a"] = data["1G"]["target"]
        data["ER1b"] = data["1G"]["commentary"]
        data["ER2a"] = data["2Ga"]["target"]
        data["ER2b"] = data["2Ga"]["commentary"]
        data["ER3a"] = data["2Gb"]["target"]
        data["ER3b"] = data["2Gb"]["commentary"]
        data["ER4a"] = data["3G"]["target"]
        data["ER4b"] = data["3G"]["commentary"]
        data["ER4c"] = country.country
        data["ER5a"] = data["4G"]["target"]
        data["ER5b"] = data["4G"]["commentary"]
        data["ER6a"] = data["5Ga"]["target"]
        data["ER6b"] = data["5Ga"]["commentary"]
        data["ER7a"] = data["5Gb"]["target"]
        data["ER7b"] = data["5Gb"]["commentary"]
        data["ER8a"] = data["6G"]["target"]
        data["ER8b"] = data["6G"]["commentary"]
        data["ER9a"] = data["7G"]["target"]
        data["ER9b"] = data["7G"]["commentary"]
        data["ER10a"] = data["8G"]["target"]
        data["ER10b"] = data["8G"]["commentary"]

        data["file"] = country.country
        data["TB2"] = translation.gov_tb2 % country.country.upper()

        data["CD1"] = data["ER1a"]
        data["CD2"] = comments_override.cd2 or data["questions"]["1"]["comments"]
        data["HSP1"] = ratings.hsp1 or data["Q2G"]["target"]
        data["HSP2"] = ratings.hsp2 or data["Q3G"]["target"]
        data["HSM1"] = ratings.hsm1 or data["Q12G"]["target"]
        data["HSM2"] = data["questions"]["15"]["latest_value"]
        data["HSM3"] = data["ER10a"]
        data["HSM4"] = ratings.hsm4

        data["BC1"] = data["questions"]["5"]["baseline_year"]
        data["BC2"] = data["questions"]["6"]["baseline_value"]
        data["BC3"] = data["questions"]["5"]["latest_year"]
        data["BC4"] = data["questions"]["6"]["latest_value"]
        data["BC5"] = "?????"
        data["BC6"] = "?????"
        data["BC7"] = "?????"
        data["BC8"] = "?????"
        data["BC9"] = "?????"
        data["BC10"] = "?????"

        data["PC1"] = data["indicators"]["3G"]["latest_value"]
        data["PC2"] = data["indicators"]["3G"]["hs_budget_gap"]
        data["PC3"] = translation.gov_pc3 % data["PC1"]
        data["PC4"] = translation.gov_pc4 % data["PC2"]

        data["PF1"] = data["questions"]["16"]["latest_value"]
        data["PF2"] = comments_override.pf2 or data["questions"]["16"]["comments"]

        data["PFM1"] = data["ER6a"]
        data["PFM2"] = comments_override.pfm2 or data["questions"]["9"]["comments"]

        data["PR1"] = data["ER7a"]
        data["PR2"] = comments_override.pr2 or data["questions"]["10"]["comments"]

        data["TA1"] = data["indicators"]["other"]["coordinated_programmes"]
        data["TA2"] = ""
        for agency in data["agencies"]:
            aqs = data["agencies"][agency]
            if "4" in aqs:
                data["TA2"] += "%s %s" % (agency, aqs["4"]["comments"].replace("%", "%%"))
                data["TA2"] += "\n"
        data["TA2"] = comments_override.ta2 or data["TA2"]

        data["PHC1"] = data["indicators"]["other"]["outpatient_visits_baseline"]
        data["PHC2"] = data["questions"]["19"]["baseline_year"]
        data["PHC3"] = data["indicators"]["other"]["outpatient_visits_latest"]
        data["PHC4"] = data["questions"]["19"]["latest_year"]
        data["PHC5"] = data["indicators"]["other"]["outpatient_visits_change"]
        data["PHC6"] = data["indicators"]["other"]["outpatient_visits_change_dir"]
        data["PHC7"] = ""

        data["HRH1"] = data["indicators"]["other"]["skilled_personnel_baseline"]
        data["HRH2"] = data["questions"]["17"]["baseline_year"]
        data["HRH3"] = data["indicators"]["other"]["skilled_personnel_latest"]
        data["HRH4"] = data["questions"]["17"]["latest_year"]
        data["HRH5"] = data["indicators"]["other"]["skilled_personnel_change"]
        data["HRH6"] = data["indicators"]["other"]["skilled_personnel_change_dir"]
        data["HRH7"] = ""

        data["HS1"] = data["questions"]["20"]["baseline_value"]
        data["HS2"] = data["questions"]["20"]["baseline_year"]
        data["HS3"] = data["questions"]["20"]["latest_value"]
        data["HS4"] = data["questions"]["20"]["latest_year"]
        data["HS5"] = data["indicators"]["other"]["health_workforce_spent_change"]
        data["HS6"] = data["indicators"]["other"]["health_workforce_spent_change_dir"]
        data["HS7"] = ""

        data["RF1"] = data["ER8a"]
        data["RF2"] = comments_override.rf2 or data["questions"]["22"]["latest_value"]
        data["RF3"] = comments_override.rf3 or data["questions"]["23"]["latest_value"]

        data["HMIS1"] = ratings.hmis1 or data["Q21G"]["target"]
        data["HMIS2"] = comments_override.hmis2 or data["questions"]["21"]["comments"]

        data["JAR1"] = ratings.jar1 or data["Q12G"]["target"]
        data["JAR2"] = "Field no longer used"
        data["JAR3"] = "Field no longer used"
        data["JAR4"] = comments_override.jar4 or data["questions"]["24"]["comments"]
        data["JAR5"] = "Field no longer used"

        data["DBR1"] = data["ER8a"]
        data["DBR2"] = comments_override.dbr2 or data["questions"]["11"]["comments"]

        group1 = ["MDG1", "MDG2", "MDG3", "MDG4"]
        group2 = ["MDG5a", "MDG5b", "MDG6a", "MDG6b", "MDG6c", "MDG7a", "MDG7b"]
        group1_index = "abcde"
        group2_index = "12345"
        needs_percent = ["MDG1", "MDG2", "MDG6a", "MDG6b", "MDG7a", "MDG7b"]
        add_perc = lambda ind : "%" if ind in needs_percent else ""
        for mdg in group1 + group2:
            #import pdb; pdb.set_trace()
            index = group1_index if mdg in group1 else group2_index
            mdgdata = models.MDGData.objects.get(mdg_target=mdg, country=country)
            if not mdgdata.latest_value:
                data[mdg + index[0]] = ""
                data[mdg + index[1]] = ""
                data[mdg + index[2]] = "questionmdg"
                data[mdg + index[3]] = ""
                data[mdg + index[4]] = ""
            elif not mdgdata.baseline_value:
                data[mdg + index[0]] = str(fformat_front(mdgdata.latest_value)) + add_perc(mdg)
                data[mdg + index[1]] = mdgdata.latest_year
                data[mdg + index[2]] = "questionmdg"
                data[mdg + index[3]] = ""
                data[mdg + index[4]] = ""
            else:
                fmt = fformat_two if mdg == "MDG3" else fformat_front
        
                data[mdg + index[0]] = str(fmt(mdgdata.latest_value)) + add_perc(mdg)
                data[mdg + index[1]] = mdgdata.latest_year
                data[mdg + index[2]] = mdgdata.arrow
                data[mdg + index[3]] = str(fmt(mdgdata.change)) + add_perc(mdg)
                data[mdg + index[4]] = mdgdata.baseline_year

        data["F1"] = country.country
        data["CN1"] = data["TB2"]
        data["GN1"] = country.country

        data["Header"] = country.country

        for i in range(1, 14):
            data["P%d" % i] = data["p"].get(i - 1, "pwhite")
            data["NP%d" % i] = data["np"].get(i - 1, "npwhite")

        working_draft, _ = models.CountryWorkingDraft.objects.get_or_create(country=country)
        data["workingdraft"] = "workingdraft" if working_draft.is_draft else ""

    except Exception, e:
        traceback.print_exc()
    return data
