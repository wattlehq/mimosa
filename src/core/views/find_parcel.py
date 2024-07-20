"""Views for handling property searches and certificate orders."""

from django.shortcuts import render
from django.views import View
from django.db.models import Q
import json

from core.models.property import Property
from core.forms.find_parcel import FindParcelForm


class FindParcel(View):
    """View for handling property searches and displaying results."""

    template_name = "pages/certificate_order.html"

    def get(self, request):
        """Handle GET requests by rendering the search form."""
        form = FindParcelForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        """
        Handle POST requests by either processing a search
        or an assessment selection.

        Returns:
            HttpResponse: Rendered template with search results
            or selected properties.
        """
        if "selected_assessment" in request.POST:
            return self.handle_assessment_selection(request)
        return self.handle_search(request)

    def handle_search(self, request):
        """
        Process the search form, find matching properties, and prepare data
        for rendering.

        Args:
            request (HttpRequest): The request object containing the search
            form data.

        Returns:
            HttpResponse: Rendered template with search results and serialized
            data for client-side storage.
        """
        form = FindParcelForm(request.POST)
        if form.is_valid():
            properties = self.search_properties(form.cleaned_data)
            grouped_properties = self.group_properties_by_assessment(
                properties
            )

            serializable_grouped_properties = {
                assessment: [self.serialize_property(prop) for prop in props]
                for assessment, props in grouped_properties.items()
            }

            return render(
                request,
                self.template_name,
                {
                    "form": form,
                    "grouped_properties": grouped_properties,
                    "serializable_grouped_properties": json.dumps(
                        serializable_grouped_properties,
                    ),
                },
            )

        return render(request, self.template_name, {"form": form})

    def handle_assessment_selection(self, request):
        """
        Process the selection of an assessment and prepare the selected
        properties for display.

        Args:
            request (HttpRequest): The request object containing the selected
            assessment and previously serialized property data.

        Returns:
            HttpResponse: Rendered template with selected properties and
            related data. In case of invalid data, returns an error message.
        """
        selected_assessment = request.POST.get("selected_assessment")
        grouped_properties_json = request.POST.get("grouped_properties")

        original_search_data = json.loads(request.POST.get(
            "original_search_data", "{}")
        )
        form = FindParcelForm(original_search_data)

        try:
            grouped_properties = json.loads(grouped_properties_json)
        except json.JSONDecodeError:
            return render(
                request, self.template_name, {
                    "form": form,
                    "error": "Invalid grouped properties data",
                }
            )

        selected_properties = grouped_properties.get(selected_assessment, [])

        return render(
            request,
            self.template_name,
            {
                "form": form,
                "grouped_properties": grouped_properties,
                "selected_properties": selected_properties,
                "selected_assessment": selected_assessment,
                "serializable_grouped_properties": grouped_properties_json,
                "original_search_data": json.dumps(original_search_data),
            },
        )

    @staticmethod
    def search_properties(cleaned_data):
        """
        Search for properties based on the provided criteria.

        Args:
            cleaned_data (dict): Cleaned form data containing search criteria.

        Returns:
            QuerySet: Filtered Property objects.
        """
        q_objects = Q()

        lot = cleaned_data.get("lot")
        section = cleaned_data.get("section")
        deposited_plan = cleaned_data.get("deposited_plan")
        street_address = cleaned_data.get("street_address")

        if lot or section or deposited_plan:
            if lot:
                q_objects &= Q(lot__icontains=lot)
            if section:
                q_objects &= Q(section__icontains=section)
            if deposited_plan:
                q_objects &= Q(deposited_plan__icontains=deposited_plan)
        elif street_address:
            parts = street_address.split()
            for part in parts:
                q_objects |= (
                    Q(address_street__icontains=part)
                    | Q(address_suburb__icontains=part)
                    | Q(address_state__icontains=part)
                    | Q(address_post_code__icontains=part)
                )

        return Property.objects.filter(q_objects)

    @staticmethod
    def group_properties_by_assessment(properties):
        """
        Group properties by their assessment values.

        Args:
            properties (QuerySet): Property objects to be grouped.

        Returns:
            dict: Properties grouped by assessment.
        """
        grouped_properties = {}
        for prop in properties:
            if prop.assessment:
                if prop.assessment not in grouped_properties:
                    grouped_properties[prop.assessment] = []
                grouped_properties[prop.assessment].append(prop)
        return grouped_properties

    @staticmethod
    def serialize_property(prop):
        """
        Serialize a Property object into a dictionary of its attributes.

        Args:
            prop (Property): The Property model instance to be serialized.

        Returns:
            dict: A dictionary containing the essential attributes of
            the Property.
        """
        return {
            "id": prop.id,
            "lot": prop.lot,
            "section": prop.section,
            "deposited_plan": prop.deposited_plan,
            "address_street": prop.address_street,
            "address_suburb": prop.address_suburb,
            "address_state": prop.address_state,
            "address_post_code": prop.address_post_code,
        }
