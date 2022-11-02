import useAxios from 'utilities/useAxios';
import { SEVERITY, VARIANT } from 'components/notification/Snackbar'
import { getHook } from 'react-hooks-outside';

export async function syncSheetsData() {
	const { createAlert } = getHook('notification');

	return await useAxios
		.post('users/sheets/sync')
		.then((res) => {
			createAlert({
				severity: SEVERITY.SUCCESS,
				variant: VARIANT.FILLED,
				alertTitle: 'Now syncing players from sheets',
				alertMessage: `Please wait for a while. The page will reload.`,
			});

			setTimeout(() => {
				window.location.reload();
			}, 3000);
			return res;
		})
		.catch((err) => {
			createAlert({
				severity: SEVERITY.ERROR,
				variant: VARIANT.FILLED,
				alertMessage: `Network Failure: Failed to sync data.`,
			});
			console.error(err);
		});
}

export async function fetchPlayerMatches(id) {
	const { createAlert } = getHook('notification');

	return await useAxios
		.post(`users/matches/${id}`)
		.then((res) => {
			createAlert({
				severity: SEVERITY.SUCCESS,
				variant: VARIANT.FILLED,
				alertTitle: 'Now fetching matches',
				alertMessage: `Please wait for a while. You will be notified after the process is done.`,
			});
			return res;
		})
		.catch((err) => {
			createAlert({
				severity: SEVERITY.ERROR,
				variant: VARIANT.FILLED,
				alertTitle: 'Failed to fetch data',
				alertMessage: `${err.response.data.detail}`,
			});
			console.error(JSON.stringify(err));
		});
}

export async function getPlayer(id) {
	return await useAxios
		.get(`users/players/${id}/`)
		.catch((err) => console.error(err));
}
