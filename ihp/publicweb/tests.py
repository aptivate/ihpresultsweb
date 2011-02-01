#-*- coding: utf-8 -*-

"""
Tests for the public IHP website Django parts.
"""

from __future__ import absolute_import

from django.test import TestCase
from django.core.urlresolvers import reverse

from submissions.models import Agency, Country, AgencyCountries
import submissions.target
import submissions.consts

import ihp.publicweb.views

class PublicWebsiteTest(TestCase):
    fixtures = ['submission_test_data.json', 'indicator_tests.yaml']
    unicef = Agency.objects.get(agency="UNICEF")
    mozambique = Country.objects.get(country="Mozambique")

    def get(self, view_function, **view_args):
        return self.client.get(reverse(view_function, kwargs=view_args))
    
    def test_getting_agency_countries(self):
        self.assertNotEqual(self.unicef, None)
        self.assertEqual(self.unicef.id, 27)
        
        self.assertNotEqual(self.mozambique, None)
        self.assertEqual(self.mozambique.id, 9)
        
        agency_countries = AgencyCountries.objects.get_agency_countries(self.unicef)
        self.assertTrue(self.mozambique in agency_countries)
        
        self.assertTrue(submissions.target.country_agency_progress(self.mozambique, self.unicef))
        
        ratings = submissions.target.calc_agency_ratings(self.unicef)
        
        rating_1 = ratings['1DP']
        self.assertEqual(rating_1['base_val'], submissions.consts.NA_STR)
        self.assertEqual(rating_1['cur_val'], 100.0)
        self.assertEqual(rating_1['comments'], [(u'1', self.mozambique, u'')])
        # self.assertEqual(rating_1['comments'][0][0], '1')
        # self.assertEqual(rating_1['comments'][0][1], mozambique)
        # self.assertEqual(rating_1['comments'][0][2], '')
        self.assertEqual(rating_1['commentary'],
            (submissions.target.na_text % self.unicef.agency) + u"∆")
        self.assertEqual(rating_1['target'], submissions.target.Rating.TICK)
        self.assertEqual(rating_1['target_val'], 100.0)
        
    def test_agency_scorecard_view(self):
        response = self.get(ihp.publicweb.views.agency_scorecard_page,
            agency_name=self.unicef.agency)
        self.assertEqual(response.context['agency'], self.unicef)
        
        ratings = submissions.target.calc_agency_ratings(self.unicef)
        indicators = response.context['indicators']
        
        for indicator_code, rating in ratings.iteritems():
            i = indicators.pop(0)
            
            if indicator_code == "1DP":
                self.assertEqual(i.expected_result,
                    "Commitments are documented and mutually agreed")
            else:
                self.assertEqual(i.expected_result, indicator_code)
            
            self.assertEqual(i.rating, rating['target'])
            self.assertEqual(i.overall_progress, rating['commentary'])
        
        (progress, no_progress) = submissions.target.get_country_progress(self.unicef)
        self.assertEqual(progress.values(),
            response.context['progress_countries'])
        self.assertEqual(no_progress.values(),
            response.context['no_progress_countries'])

    def test_country_scorecard_view(self):
        response = self.get(ihp.publicweb.views.country_scorecard_page,
            country_name=self.mozambique.country)
        self.assertEqual(response.context['country'], self.mozambique)
        
        ratings = submissions.target.calc_country_ratings(self.mozambique)
        indicators = response.context['indicators']
        
        for indicator_code, rating in ratings.iteritems():
            i = indicators.pop(0)
            
            # if indicator_code == "1DP":
            #     self.assertEqual(i.expected_result,
            #         "Commitments are documented and mutually agreed")
            # else:
            self.assertEqual(i.expected_result, indicator_code)
            
            self.assertEqual(i.rating, rating['target'])
            self.assertEqual(i.overall_progress, rating['commentary'])
        
        (progress, no_progress) = submissions.target.get_agency_progress(self.mozambique)
        self.assertTrue(len(progress.values()) > 0)
        self.assertTrue(len(no_progress.values()) > 0)
        
        self.assertEqual(progress.values(),
            response.context['progress_agencies'])
        self.assertEqual(no_progress.values(),
            response.context['no_progress_agencies'])
