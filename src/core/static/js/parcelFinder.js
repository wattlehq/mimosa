/**
 * ParcelFinder class for handling property search and selection.
 */
class ParcelFinder {
    /**
     * Create a ParcelFinder instance.
     * Initialises DOM elements and sets up event listeners.
     */
    constructor() {
        console.debug('ParcelFinder constructor called');
        this.form = null;
        this.resultsSection = null;
        this.assessmentList = null;
        this.assessmentForm = null;
        this.detailsSection = null;
        this.selectedAssessmentTitle = null;
        this.selectedPropertiesList = null;
        this.errorContainer = document.getElementById('search-errors');

        this.initialiseElements();
    }

    /**
     * Initialise DOM elements and set up event listeners.
     */
    initialiseElements() {
        console.debug('Initialising elements');
        this.form = document.querySelector('#parcel-search-form');
        this.resultsSection = document.querySelector('#matching-assessments');
        this.assessmentList = document.querySelector('#assessment-list');
        this.assessmentForm = document.querySelector('#assessment-form');
        this.detailsSection = document.querySelector('#property-details');
        this.selectedAssessmentTitle = document.querySelector('#selected-assessment-title');
        this.selectedPropertiesList = document.querySelector('#selected-properties-list');

        if (this.form) {
            console.debug('Search form found, adding event listener');
            this.form.addEventListener('submit', this.handleSearch.bind(this));
        } else {
            console.error('Search form not found');
        }

        if (this.assessmentForm) {
            console.debug('Assessment form found, adding event listener');
            this.assessmentForm.addEventListener('submit', this.handleAssessmentSelection.bind(this));
        } else {
            console.error('Assessment form not found');
        }
    }

    /**
     * Handle the search form submission.
     * Prevents default form submission, calls the search API, and displays results.
     * @param {Event} event - The submit event.
     */
    async handleSearch(event) {
        console.debug('handleSearch called');
        event.preventDefault();
        
        const formData = new FormData(this.form);
        const searchParams = Object.fromEntries(formData.entries());
        console.debug('Search params:', searchParams);
    
        try {
            const validationResult = await API.validateSearch(searchParams);
            if (validationResult.isValid) {
                this.errorContainer.innerHTML = '';
                await this.performSearch(searchParams);
            } else {
                this.displayValidationErrors(validationResult.errors);
            }
        } catch (error) {
            console.error('Error during search validation:', error);
            this.displayError('An error occurred while validating the search parameters.');
        }
    }

    async performSearch(searchParams) {
        try {
            const groupedProperties = await API.searchProperties(searchParams);
            this.displaySearchResults(groupedProperties);
        } catch (error) {
            console.error('Error searching properties:', error);
        }
    }

    displayValidationErrors(errors) {
        const displayedErrors = new Set(); // To track unique error messages
        this.errorContainer.innerHTML = '';
        for (const field in errors) {
            const errorMessages = errors[field];
            for (const message of errorMessages) {
                if (!displayedErrors.has(message.message)) {
                    const errorElement = document.createElement('p');
                    errorElement.textContent = message.message;
                    errorElement.classList.add('error-message');
                    this.errorContainer.appendChild(errorElement);
                    displayedErrors.add(message.message);
                }
            }
        }
    }

    displayError(message) {
        const errorContainer = document.getElementById('search-errors');
        errorContainer.innerHTML = `<p class="error-message">${message}</p>`;
    }

    /**
     * Handle the assessment selection form submission.
     * filters the selected properties client-side,
     * and displays the selected properties.
     * @param {Event} event - The submit event.
     */
    handleAssessmentSelection(event) {
        console.debug('handleAssessmentSelection called');
        event.preventDefault();
    
        const selectedAssessment = document.querySelector('input[name="selected_assessment"]:checked').value;
        const groupedProperties = JSON.parse(this.assessmentList.dataset.groupedProperties);
    
        console.debug('Selected assessment:', selectedAssessment);
        console.debug('Grouped properties:', groupedProperties);
    
        const selectedProperties = groupedProperties[selectedAssessment] || [];
    
        this.displaySelectedProperties(selectedProperties, selectedAssessment);
    }

    /**
     * Display the search results.
     * Creates and populates the list of assessments based on the grouped properties.
     * @param {Object} groupedProperties - The properties grouped by assessment.
     */
    displaySearchResults(groupedProperties) {
        console.debug('Displaying search results');
        this.assessmentList.innerHTML = '';
        this.assessmentList.dataset.groupedProperties = JSON.stringify(groupedProperties);
        
        const ul = document.createElement('ul');

        for (const [assessment, properties] of Object.entries(groupedProperties)) {
            const property = properties[0];
            const li = document.createElement('li');

            const input = document.createElement('input');
            input.type = 'radio';
            input.name = 'selected_assessment';
            input.value = assessment;
            input.required = true;
            input.id = `assessment-${assessment}`;

            const label = document.createElement('label');
            label.htmlFor = `assessment-${assessment}`;
            label.textContent = `${assessment} ${property.address_street}, ${property.address_suburb} ${property.address_state} ${property.address_post_code}`;

            li.appendChild(input);
            li.appendChild(label);
            ul.appendChild(li);
        }

        this.assessmentList.appendChild(ul);
        this.resultsSection.style.display = 'block';
        this.detailsSection.style.display = 'none';
    }

    /**
     * Display the selected properties for a chosen assessment.
     * Creates and populates a form with the selected properties.
     * @param {Array} selectedProperties - The properties selected for the assessment.
     * @param {string} selectedAssessment - The selected assessment identifier.
     */
    displaySelectedProperties(selectedProperties, selectedAssessment) {
        console.debug('Displaying selected properties');
        this.selectedAssessmentTitle.textContent = `Assessment: ${selectedAssessment}`;
        this.selectedPropertiesList.innerHTML = '';
        
        const form = document.createElement('form');
        form.id = 'property-selection-form';

        selectedProperties.forEach((property, index) => {
            const li = document.createElement('li');
            
            const input = document.createElement('input');
            input.type = 'radio';
            input.name = 'selected_property';
            input.value = JSON.stringify(property);
            input.id = `property-${index}`;
            input.required = true;

            const label = document.createElement('label');
            label.htmlFor = `property-${index}`;
            label.textContent = `Lot ${property.lot} Section ${property.section} Deposited Plan ${property.deposited_plan} - ${property.address_street}, ${property.address_suburb} ${property.address_state} ${property.address_post_code}`;

            li.appendChild(input);
            li.appendChild(label);
            form.appendChild(li);
        });

        const submitButton = document.createElement('button');
        submitButton.type = 'submit';
        submitButton.textContent = 'Select Property';
        form.appendChild(submitButton);

        this.selectedPropertiesList.appendChild(form);
        this.detailsSection.style.display = 'block';

        form.addEventListener('submit', this.handlePropertySelection.bind(this));
    }
    
    /**
     * Handle the property selection form submission.
     * Saves the selected property to the StateManager and clears unnecessary data.
     * @param {Event} event - The submit event.
     */
    handlePropertySelection(event) {
        console.debug('handlePropertySelection called');
        event.preventDefault();
        const selectedPropertyRadio = document.querySelector('input[name="selected_property"]:checked');
        if (selectedPropertyRadio) {
            const selectedProperty = JSON.parse(selectedPropertyRadio.value);
            StateManager.setState('selectedProperty', selectedProperty);
            StateManager.clearState('groupedProperties');
            console.debug('Property selected and saved locally. Other data cleared.');
            alert('Property selected and saved locally. Other data cleared.');
        } else {
            console.debug('No property selected');
            alert('Please select a property.');
        }
    }
}

console.debug('ParcelFinder class defined');

/**
 * Initialise the ParcelFinder when the DOM is fully loaded.
 */
document.addEventListener('DOMContentLoaded', () => {
    console.debug('DOM content loaded in parcelFinder.js');
    new ParcelFinder();
});