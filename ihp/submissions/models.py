from django.db import models

class Agency(models.Model):
    agency = models.CharField(max_length=50, null=False)
    description = models.TextField()

    def __unicode__(self):
        return self.agency

class Country(models.Model):
    country = models.CharField(max_length=50, null=False)
    description = models.TextField()

    def __unicode__(self):
        return self.country

class Submission(models.Model):
    country = models.ForeignKey(Country, null=False)
    agency = models.ForeignKey(Agency, null=True)
    docversion = models.CharField(max_length=10, null=False)
    type = models.CharField(max_length=10, null=False)
    date_submitted = models.DateTimeField(auto_now_add=True)
    completed_by = models.CharField(max_length=40)
    job_title = models.CharField(max_length=40)

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
        res = self.filter(country=country)
        return [r.agency for r in res]

class AgencyCountries(models.Model):
    agency = models.ForeignKey(Agency, null=False)
    country = models.ForeignKey(Country, null=False)

    objects = AgencyCountriesManager()

    def __unicode__(self):
        return "<<AgencyCountry Object>>%s %s" % (self.agency, self.country)

class AgencyTargets(models.Model):
    indicator = models.CharField(max_length=10, null=False)
    agency = models.ForeignKey(Agency, null=True)
    tick_criterion_type = models.CharField(max_length=50, null=False)
    tick_criterion_value = models.FloatField(null=True)
    arrow_criterion_type = models.CharField(max_length=50, null=False)
    arrow_criterion_value = models.FloatField(null=True)

    def __unicode__(self):
        return "<<AgencyTargets Object>>%s %s" % (self.agency, self.indicator)

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

