import useAxios from 'utilities/useAxios';

export async function login(data) {
    return await useAxios
        .post('auth/token/login', data)
        .catch(err => console.error(err))
}