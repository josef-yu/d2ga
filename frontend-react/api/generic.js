import useAxios from 'utilities/useAxios';

export async function fetcher(url, params) {
    return useAxios.get(url, { params })
        .then(res => res.data)
}