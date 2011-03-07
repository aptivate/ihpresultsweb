# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Agency'
        db.create_table('submissions_agency', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('agency', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=15)),
        ))
        db.send_create_signal('submissions', ['Agency'])

        # Adding model 'AgencyWorkingDraft'
        db.create_table('submissions_agencyworkingdraft', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('agency', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['submissions.Agency'], unique=True)),
            ('is_draft', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('submissions', ['AgencyWorkingDraft'])

        # Adding model 'Country'
        db.create_table('submissions_country', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('country', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('submissions', ['Country'])

        # Adding model 'CountryWorkingDraft'
        db.create_table('submissions_countryworkingdraft', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('country', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['submissions.Country'], unique=True)),
            ('is_draft', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('submissions', ['CountryWorkingDraft'])

        # Adding model 'Submission'
        db.create_table('submissions_submission', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['submissions.Country'])),
            ('agency', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['submissions.Agency'], null=True)),
            ('docversion', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('date_submitted', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('completed_by', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('job_title', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
        ))
        db.send_create_signal('submissions', ['Submission'])

        # Adding model 'DPQuestion'
        db.create_table('submissions_dpquestion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('submission', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['submissions.Submission'])),
            ('question_number', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('baseline_year', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('baseline_value', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('latest_year', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('latest_value', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('comments', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('submissions', ['DPQuestion'])

        # Adding model 'GovQuestion'
        db.create_table('submissions_govquestion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('submission', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['submissions.Submission'])),
            ('question_number', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('baseline_year', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('baseline_value', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('latest_year', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('latest_value', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('comments', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('submissions', ['GovQuestion'])

        # Adding model 'AgencyCountries'
        db.create_table('submissions_agencycountries', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('agency', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['submissions.Agency'])),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['submissions.Country'])),
        ))
        db.send_create_signal('submissions', ['AgencyCountries'])

        # Adding model 'AgencyTargets'
        db.create_table('submissions_agencytargets', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('indicator', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('agency', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['submissions.Agency'], null=True, blank=True)),
            ('tick_criterion_type', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('tick_criterion_value', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('arrow_criterion_type', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('arrow_criterion_value', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
        ))
        db.send_create_signal('submissions', ['AgencyTargets'])

        # Adding model 'CountryTargets'
        db.create_table('submissions_countrytargets', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('indicator', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['submissions.Country'], null=True, blank=True)),
            ('tick_criterion_type', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('tick_criterion_value', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('arrow_criterion_type', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('arrow_criterion_value', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
        ))
        db.send_create_signal('submissions', ['CountryTargets'])

        # Adding model 'MDGData'
        db.create_table('submissions_mdgdata', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['submissions.Country'])),
            ('mdg_target', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('baseline_year', self.gf('django.db.models.fields.CharField')(max_length=4, null=True)),
            ('baseline_value', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('latest_year', self.gf('django.db.models.fields.CharField')(max_length=4, null=True)),
            ('latest_value', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('arrow', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
        ))
        db.send_create_signal('submissions', ['MDGData'])

        # Adding model 'DPScorecardSummary'
        db.create_table('submissions_dpscorecardsummary', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('agency', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['submissions.Agency'], unique=True)),
            ('erb1', self.gf('django.db.models.fields.TextField')()),
            ('erb2', self.gf('django.db.models.fields.TextField')()),
            ('erb3', self.gf('django.db.models.fields.TextField')()),
            ('erb4', self.gf('django.db.models.fields.TextField')()),
            ('erb5', self.gf('django.db.models.fields.TextField')()),
            ('erb6', self.gf('django.db.models.fields.TextField')()),
            ('erb7', self.gf('django.db.models.fields.TextField')()),
            ('erb8', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('submissions', ['DPScorecardSummary'])

        # Adding model 'DPScorecardRatings'
        db.create_table('submissions_dpscorecardratings', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('agency', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['submissions.Agency'], unique=True)),
            ('r1', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('er1', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('r2a', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('er2a', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('r2b', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('er2b', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('r2c', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('er2c', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('r3', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('er3', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('r4', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('er4', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('r5a', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('er5a', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('r5b', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('er5b', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('r5c', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('er5c', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('r6', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('er6', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('r7', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('er7', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('r8', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('er8', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('submissions', ['DPScorecardRatings'])

        # Adding model 'GovScorecardRatings'
        db.create_table('submissions_govscorecardratings', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('country', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['submissions.Country'], unique=True)),
            ('r1', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('er1', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('r2a', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('er2a', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('r2b', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('er2b', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('r3', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('er3', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('r4', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('er4', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('r5a', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('er5a', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('r5b', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('er5b', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('r6', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('er6', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('r7', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('er7', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('r8', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('er8', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('submissions', ['GovScorecardRatings'])

        # Adding model 'CountryScorecardOverride'
        db.create_table('submissions_countryscorecardoverride', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('country', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['submissions.Country'], unique=True)),
            ('rf1', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('rf2', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('rf3', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('dbr1', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('dbr2', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('hmis1', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('hmis2', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('jar1', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('jar4', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('hsp1', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('hsp2', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('hsm1', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('hsm4', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('pfm2', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('pr2', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('ta2', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('pf2', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('cd2', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('submissions', ['CountryScorecardOverride'])

        # Adding model 'Country8DPFix'
        db.create_table('submissions_country8dpfix', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('agency', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['submissions.Agency'])),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['submissions.Country'])),
            ('baseline_progress', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('latest_progress', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
        ))
        db.send_create_signal('submissions', ['Country8DPFix'])

        # Adding unique constraint on 'Country8DPFix', fields ['agency', 'country']
        db.create_unique('submissions_country8dpfix', ['agency_id', 'country_id'])

        # Adding model 'NotApplicable'
        db.create_table('submissions_notapplicable', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('variation', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('submissions', ['NotApplicable'])

        # Adding model 'CountryExclusion'
        db.create_table('submissions_countryexclusion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['submissions.Country'])),
            ('question_number', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('baseline_applicable', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('latest_applicable', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('submissions', ['CountryExclusion'])

        # Adding unique constraint on 'CountryExclusion', fields ['country', 'question_number']
        db.create_unique('submissions_countryexclusion', ['country_id', 'question_number'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'CountryExclusion', fields ['country', 'question_number']
        db.delete_unique('submissions_countryexclusion', ['country_id', 'question_number'])

        # Removing unique constraint on 'Country8DPFix', fields ['agency', 'country']
        db.delete_unique('submissions_country8dpfix', ['agency_id', 'country_id'])

        # Deleting model 'Agency'
        db.delete_table('submissions_agency')

        # Deleting model 'AgencyWorkingDraft'
        db.delete_table('submissions_agencyworkingdraft')

        # Deleting model 'Country'
        db.delete_table('submissions_country')

        # Deleting model 'CountryWorkingDraft'
        db.delete_table('submissions_countryworkingdraft')

        # Deleting model 'Submission'
        db.delete_table('submissions_submission')

        # Deleting model 'DPQuestion'
        db.delete_table('submissions_dpquestion')

        # Deleting model 'GovQuestion'
        db.delete_table('submissions_govquestion')

        # Deleting model 'AgencyCountries'
        db.delete_table('submissions_agencycountries')

        # Deleting model 'AgencyTargets'
        db.delete_table('submissions_agencytargets')

        # Deleting model 'CountryTargets'
        db.delete_table('submissions_countrytargets')

        # Deleting model 'MDGData'
        db.delete_table('submissions_mdgdata')

        # Deleting model 'DPScorecardSummary'
        db.delete_table('submissions_dpscorecardsummary')

        # Deleting model 'DPScorecardRatings'
        db.delete_table('submissions_dpscorecardratings')

        # Deleting model 'GovScorecardRatings'
        db.delete_table('submissions_govscorecardratings')

        # Deleting model 'CountryScorecardOverride'
        db.delete_table('submissions_countryscorecardoverride')

        # Deleting model 'Country8DPFix'
        db.delete_table('submissions_country8dpfix')

        # Deleting model 'NotApplicable'
        db.delete_table('submissions_notapplicable')

        # Deleting model 'CountryExclusion'
        db.delete_table('submissions_countryexclusion')


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
            'cd2': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['submissions.Country']", 'unique': 'True'}),
            'dbr1': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'dbr2': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'hmis1': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'hmis2': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'hsm1': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'hsm4': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'hsp1': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'hsp2': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jar1': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'jar4': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'pf2': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'pfm2': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'pr2': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'rf1': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
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
        'submissions.govscorecardratings': {
            'Meta': {'object_name': 'GovScorecardRatings'},
            'country': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['submissions.Country']", 'unique': 'True'}),
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
