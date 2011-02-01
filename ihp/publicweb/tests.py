"""
Tests for the public IHP website Django parts.
"""

from django.test import TestCase
from django.core.urlresolvers import reverse
from submissions.models import Agency, Country, AgencyCountries
from submissions.target import *
from ihp.publicweb.views import agency_scorecard_page

class PublicWebsiteTest(TestCase):
    fixtures = ['indicator_tests']
    unicef = Agency.objects.get(agency="UNICEF")
    
    def test_getting_agency_countries(self):
        self.assertNotEqual(self.unicef, None)
        self.assertEqual(self.unicef.id, 27)
        
        mozambique = Country.objects.get(country="Mozambique")
        self.assertNotEqual(mozambique, None)
        self.assertEqual(mozambique.id, 9)
        
        agency_countries = AgencyCountries.objects.get_agency_countries(self.unicef)
        self.assertTrue(mozambique in agency_countries)
        
        self.assertTrue(country_agency_progress(mozambique, self.unicef))
        
    def test_country_scorecard_view(self):
        response = self.client.get(reverse(agency_scorecard_page,
            kwargs={'agency_name': self.unicef.agency}))
        self.assertEqual(response.context['agency_name'], self.unicef.agency)
        