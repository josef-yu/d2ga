import { fetcher } from 'api/generic'
import { SEVERITY, VARIANT } from 'components/notification/Snackbar'
import { getHook } from 'react-hooks-outside'

export const SWRConfig = {
    refreshInterval: 3000,
    onError: (error, key) => {
        const { createAlert } = getHook('notification')

        if(key.match(/users\/players\/(.*)\//)) {
            createAlert({
                severity: SEVERITY.ERROR,
                variant: VARIANT.FILLED,
                alertMessage: `Network Failure: Failed to fetch data.`,
            });
        }
    },
    fetcher
}