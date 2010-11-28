from django.db import models

class Agency(models.Model):
    agency = models.CharField(max_length=50, null=False)
    description = models.TextField()
    type = models.CharField(max_length=15, null=False)

    def __unicode__(self):
        return self.agency

    class Meta:
       verbose_name_plural = "Agencies" 

class Country(models.Model):
    country = models.CharField(max_length=50, null=False)
    description = models.TextField()

    def __unicode__(self):
        return self.country

    class Meta:
       verbose_name_plural = "Countries" 

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
    agency = models.ForeignKey(Agency, null=True)
    tick_criterion_type = models.CharField(max_length=50, null=False)
    tick_criterion_value = models.FloatField(null=True)
    arrow_criterion_type = models.CharField(max_length=50, null=False)
    arrow_criterion_value = models.FloatField(null=True)

    def __unicode__(self):
        return "<<AgencyTargets Object>>%s %s" % (self.agency, self.indicator)

    class Meta:
       verbose_name_plural = "Agency Targets" 

class CountryTargets(models.Model):
    indicator = models.CharField(max_length=10, null=False)
    country = models.ForeignKey(Country, null=True)
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
            return self.latest_value - self.baseline_value

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
