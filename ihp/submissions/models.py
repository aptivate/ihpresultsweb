from django.db import models

class Agency(models.Model):
    agency = models.CharField(max_length=50, null=False)
    description = models.TextField()

    def __unicode__(self):
        return self.agency

class Submission(models.Model):
    country = models.CharField(max_length=30, null=False)
    agency = models.ForeignKey(Agency, null=False)
    docversion = models.CharField(max_length=10, null=False)
    type = models.CharField(max_length=10, null=False)
    date_submitted = models.DateTimeField(auto_now_add=True)

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

class AgencyCountriesManager(models.Manager):
    def get_agency_countries(self, agency):
        res = self.filter(agency=agency)
        return [r.country for r in res]

class AgencyCountries(models.Model):
    agency = models.ForeignKey(Agency, null=False)
    country = models.CharField(max_length=50, null=False)

    objects = AgencyCountriesManager()

    def __unicode__(self):
        return "<<AgencyCountry Object>>%s %s" % (self.agency, self.country)

class Targets(models.Model):
    indicator = models.CharField(max_length=10, null=False)
    agency = models.ForeignKey(Agency, null=True)
    tick_criterion_type = models.CharField(max_length=50, null=False)
    tick_criterion_value = models.IntegerField(null=True)
    arrow_criterion_type = models.CharField(max_length=50, null=False)
    arrow_criterion_value = models.IntegerField(null=True)

    def __unicode__(self):
        return "<<Targets Object>>%s %s" % (self.agency, self.indicator)
