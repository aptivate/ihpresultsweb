from django.db import models

class SubmissionManager(models.Manager):
    def get_latest_submission(self, country, agency, type):
        return self.filter(
            country=country,
            agency=agency,
            type=type,
        ).reverse()[0:1] or None

class Submission(models.Model):
    country = models.CharField(max_length=30, null=False)
    agency = models.CharField(max_length=30, null=False)
    docversion = models.CharField(max_length=10, null=False)
    type = models.CharField(max_length=10, null=False)
    date_submitted = models.DateTimeField(auto_now_add=True)

    objects = SubmissionManager()

class DPQuestion(models.Model):
    submission = models.ForeignKey(Submission, null=False)
    question_number = models.CharField(max_length=10, null=False)
    baseline_year = models.CharField(max_length=4, null=False)
    baseline_value = models.CharField(max_length=20, null=False)
    latest_year = models.CharField(max_length=4, null=False)
    latest_value = models.CharField(max_length=20, null=False)
    comments = models.TextField()

class AgencyCountries(models.Model):
    agency = models.CharField(max_length=50, null=False)
    country = models.CharField(max_length=50, null=False)

    def __unicode__(self):
        return "<<AgencyCountry Object>>%s %s" % (self.agency, self.country)

