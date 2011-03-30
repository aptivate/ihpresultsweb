import indicators
import target
import models
import traceback

def get_agency_scorecard_data(agency, language=None):
    try:
        language = language or models.Language.objects.get(language="English")
        agency_profile, _ = models.AgencyProfile.objects.get_or_create(agency=agency, language=language)
        data = target.calc_agency_ratings(agency, language)
        data["np"], data["p"] = target.get_country_progress(agency)
        data["file"] = agency.agency
        data["agency"] = agency.agency 
        data["agencytitle"] = agency.display_name 
        data["profile"] = agency_profile.description
        for indicator in indicators.dp_indicators:
            h = indicator.replace("DP", "")
            data["er%s" % h] = data[indicator]["commentary"]
            data["r%s" % h] = data[indicator]["target"]

        for i in range(1, models.Country.objects.count() + 1):
            data["p%d" % i] = data["p"].get(i - 1, "pgreen")
            data["np%d" % i] = data["np"].get(i - 1, "npwhite")

        summary, _ = models.DPScorecardSummary.objects.get_or_create(agency=agency, language=language)
        data["erb1"] = summary.erb1
        data["erb2"] = summary.erb2
        data["erb3"] = summary.erb3
        data["erb4"] = summary.erb4
        data["erb5"] = summary.erb5
        data["erb6"] = summary.erb6
        data["erb7"] = summary.erb7
        data["erb8"] = summary.erb8

        working_draft, _ = models.AgencyWorkingDraft.objects.get_or_create(agency=agency)
        data["workingdraft"] = "workingdraft" if working_draft.is_draft else ""
        return data

    except Exception, e:
        traceback.print_exc()
