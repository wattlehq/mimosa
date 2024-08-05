export const stateKeys = {
    userDetails: "userDetails",
    selectedProperty: "selectedProperty",
    groupedProperties: "groupedProperties"
  };

/**
 * StateManager object for managing application state in localStorage.
 */
export const StateManager = {
    /**
     * Set a state value in localStorage.
     * @param {string} key - The key to identify the state.
     * @param {*} value - The value to store. Will be JSON stringified.
     */
    setState: (key, value) => {
        localStorage.setItem(key, JSON.stringify(value));
    },

    /**
     * Get a state value from localStorage.
     * @param {string} key - The key to identify the state.
     * @returns {*|null} The parsed value if it exists, null otherwise.
     */
    getState: (key) => {
        const value = localStorage.getItem(key);
        return value ? JSON.parse(value) : null;
    },

    /**
     * Clear a state value from localStorage.
     * @param {string} key - The key to identify the state to clear.
     */
    clearState: (key) => {
        localStorage.removeItem(key);
    }
};