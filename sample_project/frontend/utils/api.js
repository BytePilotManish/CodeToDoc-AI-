export const apiRequest = async (endpoint) => {
    return fetch(`/api/${endpoint}`);
};
