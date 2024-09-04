from django.test import TestCase

from core.models.property import Property
from core.services.property.group_properties_by_assessment import (
    group_properties_by_assessment,
)


class GroupPropertiesByAssessmentTest(TestCase):

    def test_group_properties_by_assessment(self):
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

        prop2 = Property(
            assessment="10",
            lot="1000",
            section="1000",
            deposited_plan="1337",
            address_street="123",
            address_suburb="Fake St.",
            address_state="Fake Town",
            address_post_code="2000",
        )

        prop.save()
        prop2.save()

        group = group_properties_by_assessment([prop, prop2])
        self.assertEqual(len(group["10"]), 2)
