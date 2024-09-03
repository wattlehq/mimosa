from django.test import TestCase

from core.models.property import Property
from core.services.property.search_properties import search_properties


class SearchPropertiesTest(TestCase):

    def test_search_properties_by_details(self):
        prop = Property(
            assessment="10",
            lot="100",
            section="1000",
            deposited_plan="1337",
            address_street="123",
            address_suburb="Fake St.",
            address_state="Fake Town",
            address_post_code="2000",
        )

        prop.save()

        search = search_properties(
            lot="10", section="1000", deposited_plan="1337"
        )

        self.assertEqual(search.first().pk, prop.pk)

    def test_search_properties_by_street(self):
        prop = Property(
            assessment="10",
            lot="100",
            section="1000",
            deposited_plan="1337",
            address_street="123",
            address_suburb="Fake St.",
            address_state="Fake Town",
            address_post_code="2000",
        )

        prop.save()

        search = search_properties(street_address="123 Fake St.")

        self.assertEqual(search.first().pk, prop.pk)
