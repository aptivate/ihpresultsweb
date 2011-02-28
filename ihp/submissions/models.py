from django.db import models
import math
from django.utils.functional import curry
from utils import memoize

class Rating(object):
    QUESTION = "question"
    TICK = "tick"
    ARROW = "arrow"
    CROSS = "cross"
    NONE = "none"

class Language(models.Model):
    language = models.CharField(max_length=30, null=False)

    def __unicode__(self):
        return self.language

class AgencyManager(models.Manager):
    def get_query_set(self):
        return super(AgencyManager, self).get_query_set().filter(type="Agency")

    def get_by_type(self, type):
        return super(AgencyManager, self).get_query_set().filter(type=type)

    def all_types(self):
        return super(AgencyManager, self).get_query_set()

class Agency(models.Model):
    agency = models.CharField(max_length=50, null=False, unique=True)
    type = models.CharField(max_length=15, null=False)
    objects = AgencyManager()

    @property
    @memoize
    def countries(self):
        return Country.objects.filter(agencycountries__agency=self).order_by("country")

    def __unicode__(self):
        return self.agency

    class Meta:
       verbose_name_plural = "Agencies" 

class AgencyProfile(models.Model):
    agency = models.ForeignKey(Agency, null=False)
    language = models.ForeignKey(Language, null=False)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return unicode(self.agency)

    class Meta:
       verbose_name_plural = "Agency Profiles" 
       unique_together = ["agency", "language"]

class AgencyWorkingDraft(models.Model):
    agency = models.OneToOneField(Agency, null=False)
    is_draft = models.BooleanField(null=False, default=True)

    def __unicode__(self):
        return unicode(self.agency)

class Country(models.Model):
    country = models.CharField(max_length=50, null=False, unique=True)
    description = models.TextField()

    @property
    def agencies(self):
        return Agency.objects.filter(agencycountries__country=self).filter(type="Agency").order_by("agency")

    def __unicode__(self):
        return self.country

    class Meta:
       verbose_name_plural = "Countries" 

class CountryWorkingDraft(models.Model):
    country = models.OneToOneField(Country, null=False)
    is_draft = models.BooleanField(null=False, default=True)

    def __unicode__(self):
        return unicode(self.country)


class Submission(models.Model):
    country = models.ForeignKey(Country, null=False)
    agency = models.ForeignKey(Agency, null=True)
    docversion = models.CharField(max_length=10, null=False)
    type = models.CharField(max_length=10, null=False)
    date_submitted = models.DateTimeField(auto_now_add=True)
    completed_by = models.CharField(max_length=50, null=True)
    job_title = models.CharField(max_length=50, null=True)

    def __unicode__(self):
        return "%s %s" % (self.country, self.agency)

class DPQuestionManager(models.Manager):
    pass
    #def get_query_set(self):
    #    return super(DPQuestionManager, self).get_query_set().filter(submission__agency__type="Agency")
    
class DPQuestion(models.Model):
    submission = models.ForeignKey(Submission, null=False)
    question_number = models.CharField(max_length=10, null=False)
    baseline_year = models.CharField(max_length=4, null=False)
    baseline_value = models.CharField(max_length=20, null=False)
    latest_year = models.CharField(max_length=4, null=False)
    latest_value = models.CharField(max_length=20, null=False)
    comments = models.TextField()
    objects = DPQuestionManager()

    def __unicode__(self):
        return "<<DPQuestion Object>>%s %s - Question: %s" % (
            self.submission.country, self.submission.agency, self.question_number
        )

    @property
    def base_val(self):
        if self.question_number == "20":
            try:
                fix = Country8DPFix.objects.get(agency=self.submission.agency, country=self.submission.country)
                return fix.baseline_progress
            except Country8DPFix.DoesNotExist:
                return ""
        return self.baseline_value

    @property
    def cur_val(self):
        if self.question_number == "20":
            try:
                fix = Country8DPFix.objects.get(agency=self.submission.agency, country=self.submission.country)
                return fix.latest_progress
            except Country8DPFix.DoesNotExist:
                return ""
        return self.latest_value

    class Meta:
       verbose_name_plural = "DP Questions" 

class GovQuestion(models.Model):
    submission = models.ForeignKey(Submission, null=False)
    question_number = models.CharField(max_length=10, null=False)
    baseline_year = models.CharField(max_length=4, null=False)
    baseline_value = models.CharField(max_length=20, null=True)
    latest_year = models.CharField(max_length=4, null=False)
    latest_value = models.CharField(max_length=20, null=True)
    comments = models.TextField()

    def __unicode__(self):
        return "<<GovQuestion Object>>%s %s - Question: %s" % (
            self.submission.country, self.submission.agency, self.question_number
        )

    @property
    def base_val(self):
        return self.baseline_value

    @property
    def cur_val(self):
        return self.latest_value

class AgencyCountriesManager(models.Manager):
    
    @memoize
    def _get_agency_countries(self):
        return list(self.all().select_related())

    def get_agency_countries(self, agency):
        return [r.country for r in self._get_agency_countries() if r.agency==agency]

    def get_country_agencies(self, country):
        return [r.agency for r in self._get_agency_countries() if r.country==country and r.agency.type=="Agency"]

class AgencyCountries(models.Model):
    agency = models.ForeignKey(Agency, null=False)
    country = models.ForeignKey(Country, null=False)

    objects = AgencyCountriesManager()

    def __unicode__(self):
        return "<<AgencyCountry Object>>%s %s" % (self.agency, self.country)

    class Meta:
       verbose_name_plural = "Agency Countries" 

class AgencyTargets(models.Model):
    indicator = models.CharField(max_length=10, null=False)
    agency = models.ForeignKey(Agency, null=True, blank=True)
    tick_criterion_type = models.CharField(max_length=50, null=False)
    tick_criterion_value = models.FloatField(null=True)
    arrow_criterion_type = models.CharField(max_length=50, null=False)
    arrow_criterion_value = models.FloatField(null=True, blank=True)

    def __unicode__(self):
        return "<<AgencyTargets Object>>%s %s" % (self.agency, self.indicator)

    class Meta:
       verbose_name_plural = "Agency Targets" 

class CountryTargets(models.Model):
    indicator = models.CharField(max_length=10, null=False)
    country = models.ForeignKey(Country, null=True, blank=True)
    tick_criterion_type = models.CharField(max_length=50, null=False)
    tick_criterion_value = models.FloatField(null=True, blank=True)
    arrow_criterion_type = models.CharField(max_length=50, null=False)
    arrow_criterion_value = models.FloatField(null=True, blank=True)

    def __unicode__(self):
        return """<<CountryTargets Object>>
Country:%s 
Indicator:%s
Tick Criterion:%s (%s)
Arrow Criterion:%s (%s)
""" % (self.country, self.indicator, self.tick_criterion_type, self.tick_criterion_value, self.arrow_criterion_type, self.arrow_criterion_value)

    class Meta:
       verbose_name_plural = "Country Targets" 

class MDGData(models.Model):
    country = models.ForeignKey(Country, null=False)
    mdg_target = models.CharField(max_length=20, null=False)
    baseline_year = models.CharField(max_length=4, null=True)
    baseline_value = models.FloatField(null=True)
    latest_year = models.CharField(max_length=4, null=True)
    latest_value = models.FloatField(null=True)
    arrow = models.CharField(max_length=20, null=True)

    @property
    def change(self):
        if self.latest_value == None or self.baseline_value == None:
            return None
        else:
            val = math.fabs(self.latest_value - self.baseline_value)
            if round(val, 3) == 0:
                return "same"
            return val

    class Meta:
        verbose_name_plural = "MDG Data" 

class DPScorecardSummary(models.Model):
    agency = models.ForeignKey(Agency, null=False)
    language = models.ForeignKey(Language, null=False)
    erb1 = models.TextField()
    erb2 = models.TextField()
    erb3 = models.TextField()
    erb4 = models.TextField()
    erb5 = models.TextField()
    erb6 = models.TextField()
    erb7 = models.TextField()
    erb8 = models.TextField()

    def __unicode__(self):
        return unicode(self.agency)

    class Meta:
       verbose_name_plural = "DP Scorecard Summaries" 
       unique_together = ["agency", "language"]

ratings_choices = [(x, x) for x in [Rating.TICK, Rating.ARROW, Rating.CROSS, Rating.QUESTION, Rating.NONE]]
RatingsField = curry(models.CharField, max_length=20, null=True, blank=True, choices=ratings_choices)
CommentsField = curry(models.TextField, null=True, blank=True)

class DPScorecardRatings(models.Model):
    agency = models.OneToOneField(Agency, null=False)
    r1 = RatingsField()
    r2a = RatingsField()
    r2b = RatingsField()
    r2c = RatingsField()
    r3 = RatingsField()
    r4 = RatingsField()
    r5a = RatingsField()
    r5b = RatingsField()
    r5c = RatingsField()
    r6 = RatingsField()
    r7 = RatingsField()
    r8 = RatingsField()


    def __unicode__(self):
        return unicode(self.agency)

    class Meta:
       verbose_name_plural = "DP Scorecard Ratings" 

class DPScorecardComments(models.Model):
    agency = models.ForeignKey(Agency, null=False)
    language = models.ForeignKey(Language, null=False)

    er1 = CommentsField()
    er2a = CommentsField()
    er2b = CommentsField()
    er2c = CommentsField()
    er3 = CommentsField()
    er4 = CommentsField()
    er5a = CommentsField()
    er5b = CommentsField()
    er5c = CommentsField()
    er6 = CommentsField()
    er7 = CommentsField()
    er8 = CommentsField()

    def __unicode__(self):
        return "%s %s" % (self.agency, self.language)

    class Meta:
       verbose_name_plural = "DP Scorecard Comments" 
       unique_together = ["agency", "language"]

class GovScorecardRatings(models.Model):
    country = models.ForeignKey(Country, null=False)

    r1 = RatingsField()
    r2a = RatingsField()
    r2b = RatingsField()
    r3 = RatingsField()
    r4 = RatingsField()
    r5a = RatingsField()
    r5b = RatingsField()
    r6 = RatingsField()
    r7 = RatingsField()
    r8 = RatingsField()
    hmis1  = RatingsField(verbose_name="HMIS1 (Q21G)")
    jar1 = RatingsField(verbose_name="JAR1 (Q12G)")
    hsp1 = RatingsField(verbose_name="HSP1 (Q2G)")
    hsp2 = RatingsField(verbose_name="HSP2 (Q3G)")
    hsm1 = RatingsField(verbose_name="HSM1 (Q12G)")
    hsm4 = RatingsField(verbose_name="HSM4")

    def __unicode__(self):
        return unicode(self.country)

    class Meta:
        verbose_name_plural = "Gov Scorecard Ratings" 

class GovScorecardComments(models.Model):
    country = models.ForeignKey(Country, null=False)
    language = models.ForeignKey(Language, null=False)

    er1 = CommentsField()
    er2a = CommentsField()
    er2b = CommentsField()
    er3 = CommentsField()
    er4 = CommentsField()
    er5a = CommentsField()
    er5b = CommentsField()
    er6 = CommentsField()
    er7 = CommentsField()
    er8 = CommentsField()

    def __unicode__(self):
        return unicode(self.country)

    class Meta:
        verbose_name_plural = "Gov Scorecard Comments" 
        unique_together = ["country", "language"]

class CountryScorecardOverrideComments(models.Model):
    country = models.ForeignKey(Country, null=False)
    language = models.ForeignKey(Language, null=False)

    rf2 = CommentsField(verbose_name="RF2")
    rf3 = CommentsField(verbose_name="RF3")
    dbr2 = CommentsField(verbose_name="DBR2")
    hmis2 = CommentsField(verbose_name="HMIS2")
    jar4 = CommentsField(verbose_name="JAR4")
    pfm2 = CommentsField(verbose_name="PFM2")
    pr2 = CommentsField(verbose_name="PR2")
    ta2 = CommentsField(verbose_name="TA2")
    pf2 = CommentsField(verbose_name="PF2")
    cd2 = CommentsField(verbose_name="CD2")

    def __unicode__(self):
        return "%s (%s)" % (self.country, self.language)

    class Meta:
        verbose_name_plural = "Country Scorecard Override Comments"
        unique_together = ["country", "language"]

class Country8DPFix(models.Model):
    agency = models.ForeignKey(Agency, null=False)
    country = models.ForeignKey(Country, null=False)
    baseline_progress = RatingsField()
    latest_progress = RatingsField()

    def __unicode__(self):
        return "%s - %s" % (self.agency, self.country)

    class Meta:
        verbose_name_plural = "Country 8DP Fixes" 
        unique_together = ["agency", "country"]

class NotApplicableManager(models.Manager):
    @memoize
    def _get_variations(self):
        return list(self.all())

    def is_not_applicable(self, val):
        if val == None:
            return False

        val = str(val).strip().lower()
        variations = [na.variation for na in self._get_variations()]
        if val in variations:
            return True
        else:
            return False

class NotApplicable(models.Model):
    variation = models.CharField(max_length=30, null=False)
    objects = NotApplicableManager()

    def __unicode__(self):
        return self.variation

    class Meta:
       verbose_name_plural = "Not Applicable Variations" 

class CountryExclusionManager(models.Manager):

    @memoize
    def _get_baseline_applicable(self):
        return list(self.filter(baseline_applicable=False).select_related())

    @memoize
    def _get_latest_applicable(self):
        return list(self.filter(latest_applicable=False).select_related())
        
    @memoize
    def is_applicable(self, question, country):
        """
        Checks whether a question is applicable to that particular country
        """
        if type(country) == Country:
            country = country.country

        bapp = self._get_baseline_applicable()
        lapp = self._get_latest_applicable()

        baseline_applicable = len([
            ba 
            for ba in bapp 
            if ba.question_number==question and ba.country.country==country
        ]) == 0

        latest_applicable = len([
            ba 
            for ba in lapp 
            if ba.question_number==question and ba.country.country==country
        ]) == 0

        return baseline_applicable, latest_applicable

    def baseline_excluded_countries(self, question):
        return [ce.country for ce in self._get_baseline_applicable() if ce.question_number==question]

    def latest_excluded_countries(self, question):
        return [ce.country for ce in self._get_latest_applicable() if ce.question_number==question]

class CountryExclusion(models.Model):
    country = models.ForeignKey(Country, null=False)
    question_number = models.CharField(max_length=10, null=False)
    baseline_applicable = models.BooleanField()
    latest_applicable = models.BooleanField()
    objects = CountryExclusionManager()

    def __unicode__(self):
        return "%s - %s" % (self.question_number, self.country)

    class Meta:
       verbose_name_plural = "Country Exclusions" 
       unique_together = ["country", "question_number"]
