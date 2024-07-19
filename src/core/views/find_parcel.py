"""Views for handling property searches and certificate orders."""

from django.shortcuts import render
from django.views import View
from django.db.models import Q

from core.models import Property
from ..forms.find_parcel import FindParcelForm


class FindParcel(View):
    """View for handling property searches and displaying results."""

    template_name = 'pages/certificate_order.html'

    def get(self, request):
        """Handle GET requests by rendering the search form."""
        form = FindParcelForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """
        Handle POST requests by either processing a search or an assessment selection.

        Returns:
            HttpResponse: Rendered template with search results or selected properties.
        """
        if 'selected_assessment' in request.POST:
            return self.handle_assessment_selection(request)
        return self.handle_search(request)

    def handle_search(self, request):
        """
        Process the search form and return results.

        Args:
            request (HttpRequest): The request object.

        Returns:
            HttpResponse: Rendered template with search results.
        """
        form = FindParcelForm(request.POST)
        if form.is_valid():
            properties = self.search_properties(form.cleaned_data)
            grouped_properties = self.group_properties_by_assessment(properties)

            serializable_grouped_properties = {
                assessment: [prop.id for prop in props]
                for assessment, props in grouped_properties.items()
            }

            request.session['grouped_properties'] = serializable_grouped_properties

            return render(request, self.template_name, {
                'form': form,
                'grouped_properties': grouped_properties
            })

        return render(request, self.template_name, {'form': form})

    def handle_assessment_selection(self, request):
        """
        Process the selection of an assessment and return relevant properties.

        Args:
            request (HttpRequest): The request object.

        Returns:
            HttpResponse: Rendered template with selected properties.
        """
        selected_assessment = request.POST.get('selected_assessment')
        serializable_grouped_properties = request.session.get('grouped_properties', {})

        grouped_properties = {
            assessment: list(Property.objects.filter(id__in=prop_ids))
            for assessment, prop_ids in serializable_grouped_properties.items()
        }

        selected_properties = grouped_properties.get(selected_assessment, [])

        return render(request, self.template_name, {
            'form': FindParcelForm(),
            'grouped_properties': grouped_properties,
            'selected_properties': selected_properties,
            'selected_assessment': selected_assessment
        })

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

        lot = cleaned_data.get('lot')
        section = cleaned_data.get('section')
        deposited_plan = cleaned_data.get('deposited_plan')
        street_address = cleaned_data.get('street_address')

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
                    Q(address_street__icontains=part) |
                    Q(address_suburb__icontains=part) |
                    Q(address_state__icontains=part) |
                    Q(address_post_code__icontains=part)
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