from django.db import models
import math
from django.utils.functional import curry

class Rating(object):
    QUESTION = "question"
    TICK = "tick"
    ARROW = "arrow"
    CROSS = "cross"
    NONE = "none"

class Agency(models.Model):
    agency = models.CharField(max_length=50, null=False, unique=True)
    description = models.TextField()
    type = models.CharField(max_length=15, null=False)

    @property
    def countries(self):
        return Country.objects.filter(agencycountries__agency=self).order_by("country")

    def __unicode__(self):
        return self.agency

    class Meta:
       verbose_name_plural = "Agencies" 

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


class UpdateAgency(models.Model):
    agency = models.OneToOneField(Agency, null=False)
    update = models.BooleanField(null=False)

    def __unicode__(self):
        return unicode(self.agency)

    class Meta:
       verbose_name_plural = "Update Agencies" 


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

class DPQuestion(models.Model):
    submission = models.ForeignKey(Submission, null=False)
    question_number = models.CharField(max_length=10, null=False)
    baseline_year = models.CharField(max_length=4, null=False)
    baseline_value = models.CharField(max_length=20, null=False)
    latest_year = models.CharField(max_length=4, null=False)
    latest_value = models.CharField(max_length=20, null=False)
    comments = models.TextField()

    def __unicode__(self):
        return "<<DPQuestion Object>>%s %s - Question: %s" % (
            self.submission.country, self.submission.agency, self.question_number
        )

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

class AgencyCountriesManager(models.Manager):
    def get_agency_countries(self, agency):
        res = self.filter(agency=agency)
        return [r.country for r in res]

    def get_country_agencies(self, country):
        res = self.filter(country=country, agency__type="Agency")
        return [r.agency for r in res]

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
    tick_criterion_value = models.FloatField(null=True)
    arrow_criterion_type = models.CharField(max_length=50, null=False)
    arrow_criterion_value = models.FloatField(null=True)

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
    agency = models.OneToOneField(Agency, null=False)
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

ratings_choices = [(x, x) for x in [Rating.TICK, Rating.ARROW, Rating.CROSS, Rating.QUESTION, Rating.NONE]]
RatingsField = curry(models.CharField, max_length=20, null=True, blank=True, choices=ratings_choices)
CommentsField = curry(models.TextField, null=True, blank=True)

class DPScorecardRatings(models.Model):
    agency = models.OneToOneField(Agency, null=False)
    r1 = RatingsField()
    er1 = CommentsField()

    r2a = RatingsField()
    er2a = CommentsField()
    r2b = RatingsField()
    er2b = CommentsField()
    r2c = RatingsField()
    er2c = CommentsField()

    r3 = RatingsField()
    er3 = CommentsField()

    r4 = RatingsField()
    er4 = CommentsField()

    r5a = RatingsField()
    er5a = CommentsField()
    r5b = RatingsField()
    er5b = CommentsField()
    r5c = RatingsField()
    er5c = CommentsField()

    r6 = RatingsField()
    er6 = CommentsField()

    r7 = RatingsField()
    er7 = CommentsField()

    r8 = RatingsField()
    er8 = CommentsField()


    def __unicode__(self):
        return unicode(self.agency)

    class Meta:
       verbose_name_plural = "DP Scorecard Ratings" 

class GovScorecardRatings(models.Model):
    country = models.OneToOneField(Country, null=False)
    r1 = RatingsField()
    er1 = CommentsField()

    r2a = RatingsField()
    er2a = CommentsField()
    r2b = RatingsField()
    er2b = CommentsField()

    r3 = RatingsField()
    er3 = CommentsField()

    r4 = RatingsField()
    er4 = CommentsField()

    r5a = RatingsField()
    er5a = CommentsField()
    r5b = RatingsField()
    er5b = CommentsField()

    r6 = RatingsField()
    er6 = CommentsField()

    r7 = RatingsField()
    er7 = CommentsField()

    r8 = RatingsField()
    er8 = CommentsField()


    def __unicode__(self):
        return unicode(self.country)

    class Meta:
       verbose_name_plural = "Gov Scorecard Ratings" 

class CountryScorecardOverride(models.Model):
    country = models.OneToOneField(Country, null=False)

    rf1 = RatingsField(verbose_name="RF1")
    rf2 = CommentsField(verbose_name="RF2")
    rf3 = CommentsField(verbose_name="RF3")

    dbr1 = RatingsField(verbose_name="DBR1")
    dbr2 = CommentsField(verbose_name="DBR2")

    hmis1 = RatingsField(verbose_name="HMIS1")
    hmis2 = CommentsField(verbose_name="HMIS2")

    jar1 = RatingsField(verbose_name="JAR1")
    jar4 = CommentsField(verbose_name="JAR4")

    hsp1 = RatingsField(verbose_name="HSP1")

    hsp2 = RatingsField(verbose_name="HSP2")

    hsm1 = RatingsField(verbose_name="HSM1")

    hsm4 = RatingsField(verbose_name="HSM4")

    pfm2 = CommentsField(verbose_name="PFM2")

    pr2 = CommentsField(verbose_name="PR2")

    ta2 = CommentsField(verbose_name="TA2")

    pf2 = CommentsField(verbose_name="PF2")

    def __unicode__(self):
        return unicode(self.country)

    class Meta:
       verbose_name_plural = "Country Scorecard Override" 

class Country8DPFix(models.Model):
    agency = models.ForeignKey(Agency, null=False)
    country = models.ForeignKey(Country, null=False)
    baseline_progress = models.BooleanField(null=False)
    latest_progress = models.BooleanField(null=False)

    def __unicode__(self):
        return "%s - %s" % (self.agency, self.country)

    class Meta:
        verbose_name_plural = "Country 8DP Fixes" 
        unique_together = ["agency", "country"]

class CountryLanguage(models.Model):
    country = models.ForeignKey(Country, null=False)
    language = models.CharField(max_length=20, null=False)

class NotApplicableManager(models.Manager):
    def is_not_applicable(self, val):
        if val == None:
            return False

        val = val.strip().lower()
        variations = [na.variation for na in self.all()]
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

    def is_applicable(self, question, country):
        """
        Checks whether a question is applicable to that particular country
        """
        if type(country) == Country:
            country = country.country

        baseline_applicable = self.filter(question_number=question, country__country=country, baseline_applicable=False).count() == 0
        latest_applicable = self.filter(question_number=question, country__country=country, latest_applicable=False).count() == 0

        return baseline_applicable, latest_applicable

    def baseline_excluded_countries(self, question):
        return [ce.country for ce in self.filter(question_number=question, baseline_applicable=False)]

    def latest_excluded_countries(self, question):
        return [ce.country for ce in self.filter(question_number=question, latest_applicable=False)]

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
