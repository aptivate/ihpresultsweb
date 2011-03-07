# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'CountryScorecardOverride.rf3'
        db.delete_column('submissions_countryscorecardoverride', 'rf3')

        # Deleting field 'CountryScorecardOverride.rf2'
        db.delete_column('submissions_countryscorecardoverride', 'rf2')

        # Deleting field 'CountryScorecardOverride.hmis2'
        db.delete_column('submissions_countryscorecardoverride', 'hmis2')

        # Deleting field 'CountryScorecardOverride.pf2'
        db.delete_column('submissions_countryscorecardoverride', 'pf2')

        # Deleting field 'CountryScorecardOverride.ta2'
        db.delete_column('submissions_countryscorecardoverride', 'ta2')

        # Deleting field 'CountryScorecardOverride.cd2'
        db.delete_column('submissions_countryscorecardoverride', 'cd2')

        # Deleting field 'CountryScorecardOverride.pr2'
        db.delete_column('submissions_countryscorecardoverride', 'pr2')

        # Deleting field 'CountryScorecardOverride.pfm2'
        db.delete_column('submissions_countryscorecardoverride', 'pfm2')

        # Deleting field 'CountryScorecardOverride.dbr2'
        db.delete_column('submissions_countryscorecardoverride', 'dbr2')

        # Deleting field 'CountryScorecardOverride.jar4'
        db.delete_column('submissions_countryscorecardoverride', 'jar4')


    def backwards(self, orm):
        
        # Adding field 'CountryScorecardOverride.rf3'
        db.add_column('submissions_countryscorecardoverride', 'rf3', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'CountryScorecardOverride.rf2'
        db.add_column('submissions_countryscorecardoverride', 'rf2', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'CountryScorecardOverride.hmis2'
        db.add_column('submissions_countryscorecardoverride', 'hmis2', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'CountryScorecardOverride.pf2'
        db.add_column('submissions_countryscorecardoverride', 'pf2', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'CountryScorecardOverride.ta2'
        db.add_column('submissions_countryscorecardoverride', 'ta2', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'CountryScorecardOverride.cd2'
        db.add_column('submissions_countryscorecardoverride', 'cd2', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'CountryScorecardOverride.pr2'
        db.add_column('submissions_countryscorecardoverride', 'pr2', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'CountryScorecardOverride.pfm2'
        db.add_column('submissions_countryscorecardoverride', 'pfm2', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'CountryScorecardOverride.dbr2'
        db.add_column('submissions_countryscorecardoverride', 'dbr2', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'CountryScorecardOverride.jar4'
        db.add_column('submissions_countryscorecardoverride', 'jar4', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)


    models = {
        'submissions.agency': {
            'Meta': {'object_name': 'Agency'},
            'agency': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '15'})
        },
        'submissions.agencycountries': {
            'Meta': {'object_name': 'AgencyCountries'},
            'agency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['submissions.Agency']"}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['submissions.Country']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'submissions.agencytargets': {
            'Meta': {'object_name': 'AgencyTargets'},
            'agency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['submissions.Agency']", 'null': 'True', 'blank': 'True'}),
            'arrow_criterion_type': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'arrow_criterion_value': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indicator': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'tick_criterion_type': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'tick_criterion_value': ('django.db.models.fields.FloatField', [], {'null': 'True'})
        },
        'submissions.agencyworkingdraft': {
            'Meta': {'object_name': 'AgencyWorkingDraft'},
            'agency': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['submissions.Agency']", 'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_draft': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'submissions.country': {
            'Meta': {'object_name': 'Country'},
            'country': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'submissions.country8dpfix': {
            'Meta': {'unique_together': "(['agency', 'country'],)", 'object_name': 'Country8DPFix'},
            'agency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['submissions.Agency']"}),
            'baseline_progress': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['submissions.Country']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latest_progress': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})
        },
        'submissions.countryexclusion': {
            'Meta': {'unique_together': "(['country', 'question_number'],)", 'object_name': 'CountryExclusion'},
            'baseline_applicable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['submissions.Country']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latest_applicable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'question_number': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'submissions.countryscorecardoverride': {
            'Meta': {'object_name': 'CountryScorecardOverride'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['submissions.Country']"}),
            'dbr1': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'hmis1': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'hsm1': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'hsm4': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'hsp1': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'hsp2': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jar1': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'rf1': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})
        },
        'submissions.countryscorecardoverridecomments': {
            'Meta': {'unique_together': "(['country', 'language'],)", 'object_name': 'CountryScorecardOverrideComments'},
            'cd2': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['submissions.Country']"}),
            'dbr2': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'hmis2': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jar4': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['submissions.Language']"}),
            'pf2': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'pfm2': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'pr2': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'rf2': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'rf3': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'ta2': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'submissions.countrytargets': {
            'Meta': {'object_name': 'CountryTargets'},
            'arrow_criterion_type': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'arrow_criterion_value': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['submissions.Country']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indicator': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'tick_criterion_type': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'tick_criterion_value': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        'submissions.countryworkingdraft': {
            'Meta': {'object_name': 'CountryWorkingDraft'},
            'country': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['submissions.Country']", 'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_draft': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'submissions.dpquestion': {
            'Meta': {'object_name': 'DPQuestion'},
            'baseline_value': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'baseline_year': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'comments': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latest_value': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'latest_year': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'question_number': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'submission': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['submissions.Submission']"})
        },
        'submissions.dpscorecardratings': {
            'Meta': {'object_name': 'DPScorecardRatings'},
            'agency': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['submissions.Agency']", 'unique': 'True'}),
            'er1': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'er2a': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'er2b': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'er2c': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'er3': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'er4': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'er5a': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'er5b': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'er5c': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'er6': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'er7': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'er8': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'r1': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'r2a': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'r2b': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'r2c': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'r3': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'r4': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'r5a': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'r5b': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'r5c': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'r6': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'r7': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'r8': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})
        },
        'submissions.dpscorecardsummary': {
            'Meta': {'object_name': 'DPScorecardSummary'},
            'agency': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['submissions.Agency']", 'unique': 'True'}),
            'erb1': ('django.db.models.fields.TextField', [], {}),
            'erb2': ('django.db.models.fields.TextField', [], {}),
            'erb3': ('django.db.models.fields.TextField', [], {}),
            'erb4': ('django.db.models.fields.TextField', [], {}),
            'erb5': ('django.db.models.fields.TextField', [], {}),
            'erb6': ('django.db.models.fields.TextField', [], {}),
            'erb7': ('django.db.models.fields.TextField', [], {}),
            'erb8': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'submissions.govquestion': {
            'Meta': {'object_name': 'GovQuestion'},
            'baseline_value': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'baseline_year': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'comments': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latest_value': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'latest_year': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'question_number': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'submission': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['submissions.Submission']"})
        },
        'submissions.govscorecardcomments': {
            'Meta': {'unique_together': "(['country', 'language'],)", 'object_name': 'GovScorecardComments'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['submissions.Country']"}),
            'er1': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'er2a': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'er2b': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'er3': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'er4': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'er5a': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'er5b': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'er6': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'er7': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'er8': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['submissions.Language']"})
        },
        'submissions.govscorecardratings': {
            'Meta': {'object_name': 'GovScorecardRatings'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['submissions.Country']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'r1': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'r2a': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'r2b': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'r3': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'r4': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'r5a': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'r5b': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'r6': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'r7': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'r8': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})
        },
        'submissions.language': {
            'Meta': {'object_name': 'Language'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'submissions.mdgdata': {
            'Meta': {'object_name': 'MDGData'},
            'arrow': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'baseline_value': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'baseline_year': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['submissions.Country']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latest_value': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'latest_year': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True'}),
            'mdg_target': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'submissions.notapplicable': {
            'Meta': {'object_name': 'NotApplicable'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'variation': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'submissions.submission': {
            'Meta': {'object_name': 'Submission'},
            'agency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['submissions.Agency']", 'null': 'True'}),
            'completed_by': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['submissions.Country']"}),
            'date_submitted': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'docversion': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job_title': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        }
    }

    complete_apps = ['submissions']
