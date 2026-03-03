import { useState } from 'react';

export const useFetch = (url) => {
    const [data, setData] = useState(null);
    return { data };
};
