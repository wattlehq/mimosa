/**
 * API object for making requests to the server.
 */
const API = {
    /**
     * Search for properties based on given parameters.
     * @param {Object} searchParams - The search parameters.
     * @returns {Promise<Object>} A promise that resolves to the search results.
     * @throws {Error} If the network response is not ok.
     */
    searchProperties: async (searchParams) => {
        const queryString = new URLSearchParams(searchParams).toString();
        const response = await fetch(`/api/search-properties/?${queryString}`, {
            method: 'GET',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            },
        });
        if (!response.ok) throw new Error('Network response was not ok');
        return response.json();
    },
};

/**
 * Utility function to get CSRF token from cookies.
 * @param {string} name - The name of the cookie to retrieve.
 * @returns {string|null} The value of the cookie if found, null otherwise.
 */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}