import useAxios from 'utilities/useAxios';
import { SEVERITY, VARIANT } from 'components/notification/Snackbar'
import { getHook } from 'react-hooks-outside';

export async function findMatch() {
	const { createAlert } = getHook('notification');

    return useAxios
        .post('users/matchmaking')
        .then(res => {
            createAlert({
				severity: SEVERITY.SUCCESS,
				variant: VARIANT.FILLED,
				alertMessage: `Now finding match`,
			});

            return res
        })
        .catch((err) => {
			createAlert({
				severity: SEVERITY.ERROR,
				variant: VARIANT.FILLED,
				alertMessage: `Network Failure: Failed to start matchmaking.`,
			});
			console.error(err);
		});
}