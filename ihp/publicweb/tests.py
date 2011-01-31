"""
Tests for the public IHP website Django parts.
"""

from django.test import TestCase
from submissions.models import Agency, Country, AgencyCountries
from submissions.target import *

class PublicWebsiteTest(TestCase):
    fixtures = ['indicator_tests']
    
    def test_getting_agency_countries(self):
        unicef = Agency.objects.get(agency="UNICEF")
        self.assertNotEqual(unicef, None)
        self.assertEqual(unicef.id, 27)
        
        mozambique = Country.objects.get(country="Mozambique")
        self.assertNotEqual(mozambique, None)
        self.assertEqual(mozambique.id, 9)
        
        agency_countries = AgencyCountries.objects.get_agency_countries(unicef)
        self.assertTrue(mozambique in agency_countries)
        
        self.assertTrue(country_agency_progress(mozambique, unicef))
        
        


