import axios from 'axios';

axios.defaults.baseURL = process.env.NEXT_PUBLIC_API_HOST;

const useAxios = axios.create();

useAxios.interceptors.request.use(
	(config) => {
		const token = localStorage.getItem('token');

		if (token) {
			config.headers.Authorization = `Token ${token}`;
		}
		return config;
	},
	(error) => {
		return Promise.reject(error);
	}
);

export default useAxios;
