import { API } from './api.js';

/**
 * FindParcel class for handling property search and selection.
 */
class FindParcel {
  /**
   * Create a FindParcel instance.
   * Initialises DOM elements and sets up event listeners.
   */
  constructor() {
    console.debug('FindParcel constructor called');
    this.searchForm = null;
    this.assessmentSection = null;
    this.assessmentList = null;
    this.assessmentForm = null;
    this.propertySection = null;
    this.propertyTitle = null;
    this.propertyList = null;
    this.error = null;
    this.inputSelectionTarget = null;

    this.initialiseElements();
  }

  /**
   * Initialise DOM elements and set up event listeners.
   */
  initialiseElements() {
    console.debug('Initialising elements');
    this.searchForm = document.querySelector('.find-parcel__search form');
    this.assessmentSection = document.querySelector('.find_parcel__assessment');
    this.assessmentList = document.querySelector('.find_parcel__assessment-list');
    this.assessmentForm = document.querySelector('.find_parcel__assessment form');
    this.propertySection = document.querySelector('.find_parcel__property');
    this.propertyTitle = document.querySelector('.find_parcel__property-title');
    this.propertyList = document.querySelector('.find_parcel__property-list');
    this.inputSelectionTarget = document.querySelector('.order-form input[name="property_id"]');
    this.error = document.querySelector('.find-parcel__search-errors');

    if (this.searchForm) {
      console.debug('Search form found, adding event listener');
      this.searchForm.addEventListener('submit', this.handleSearch.bind(this));
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
   * Handles the search form submission.
   * Validates search parameters, and either performs the search or
   * displays validation errors.
   *
   * @param {Event} event - The form submission event.
   * @returns {Promise<void>}
   */
  async handleSearch(event) {
    console.debug('handleSearch called');
    event.preventDefault();

    const formData = new FormData(this.searchForm);
    const searchParams = Object.fromEntries(formData.entries());
    console.debug('Search params:', searchParams);

    try {
      const result = await API.searchProperties(searchParams);
      if (result && result.isValid) {
        this.error.innerHTML = '';
        this.displaySearchResults(result.results);
      } else {
        this.displayValidationErrors(result.errors);
      }
    } catch (error) {
      console.error('Error during search:', error);
      this.displayError('An error occurred while searching for properties.');
    }
  }

  /**
   * Displays validation errors in the error container.
   *
   * @param {Object} errors - An object containing validation errors.
   */
  displayValidationErrors(errors) {
    const displayedErrors = new Set(); // To track unique error messages
    this.error.innerHTML = '';
    for (const field in errors) {
      const errorMessages = errors[field];
      for (const message of errorMessages) {
        if (!displayedErrors.has(message.message)) {
          const errorElement = document.createElement('p');
          errorElement.textContent = message.message;
          this.error.appendChild(errorElement);
          displayedErrors.add(message.message);
        }
      }
    }
  }

  /**
   * Displays a single error message in the error container.
   *
   * @param {string} message - The error message to display.
   */
  displayError(message) {
    const errorContainer = this.error;
    errorContainer.innerHTML = `<p>${message}</p>`;
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
    console.debug('Displaying search results', groupedProperties);
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

    if (ul.children.length === 0) {
      this.displayError('No properties found matching the search criteria.');
    } else {
      this.assessmentList.appendChild(ul);
      this.assessmentSection.style.display = 'block';
      this.propertySection.style.display = 'none';
    }
  }

  /**
   * Display the selected properties for a chosen assessment.
   * Creates and populates a form with the selected properties.
   * @param {Array} selectedProperties - The properties selected for the assessment.
   * @param {string} selectedAssessment - The selected assessment identifier.
   */
  displaySelectedProperties(selectedProperties, selectedAssessment) {
    console.debug('Displaying selected properties');
    this.propertyTitle.textContent = `Assessment: ${selectedAssessment}`;
    this.propertyList.innerHTML = '';

    const form = document.createElement('form');

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

    this.propertyList.appendChild(form);
    this.propertySection.style.display = 'block';

    form.addEventListener('submit', this.handlePropertySelection.bind(this));
  }

  /**
   * Handle the property selection form submission.
   * @param {Event} event - The submit event.
   */
  handlePropertySelection(event) {
    console.debug('handlePropertySelection called');
    event.preventDefault();
    const selectedPropertyRadio = document.querySelector('input[name="selected_property"]:checked');
    const selection = JSON.parse(selectedPropertyRadio.value);

    if (this.inputSelectionTarget) {
      if (selectedPropertyRadio) {
        this.inputSelectionTarget.value = selection.id;
      } else {
        console.debug('No property selected');
        alert('Please select a property.');
      }
    } else {
      console.debug('No property selection target');
    }
  }
}

console.debug('ParcelFinder class defined');

/**
 * Initialise the ParcelFinder when the DOM is fully loaded.
 */
document.addEventListener('DOMContentLoaded', () => {
  console.debug('DOM content loaded in parcelFinder.js');
  new FindParcel();
});
