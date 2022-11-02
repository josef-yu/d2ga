import { createContext, useContext, useState, useMemo, useEffect } from 'react';
import { useRouter } from 'next/router';
import { setHook } from 'react-hooks-outside';
import { useSWRConfig } from 'swr';

const NotificationContext = createContext();

export function useNotificationContext() {
	return useContext(NotificationContext);
}

setHook('notification', useNotificationContext);
setHook('swr-config', useSWRConfig);

export function NotificationContextProvider({ children }) {
	const [alertElementProps, setAlertElementProps] = useState(null);
	const [snackbarOpen, setSnackbarOpen] = useState(false);
	const [autoHideDuration, setAutoHideDuration] = useState(6000);
	const router = useRouter();

	function createAlert({
		severity,
		alertTitle,
		variant,
		alertMessage,
		action,
	}) {
		setAlertElementProps({
			severity,
			alertTitle,
			variant,
			alertMessage,
			action,
		});
		setSnackbarOpen(true);
	}

	const value = useMemo(
		() => ({
			alertElementProps,
			setAlertElementProps,
			snackbarOpen,
			setSnackbarOpen,
			autoHideDuration,
			setAutoHideDuration,
			createAlert,
		}),
		[alertElementProps, snackbarOpen, autoHideDuration]
	);

	useEffect(() => {
		router.events.on('routeChangeComplete', () => {
			setAlertElementProps(null);
			setSnackbarOpen(false);
		});

		return () => {
			router.events.off('routeChangeComplete', () => {
				setAlertElementProps(null);
				setSnackbarOpen(false);
			});
		};
	}, [router.events]);

	return (
		<NotificationContext.Provider value={value}>
			{children}
		</NotificationContext.Provider>
	);
}
