import { useNotificationContext } from './NotificationContext';
import { Snackbar as MuiSnackbar, Alert, AlertTitle } from '@mui/material';

export const SEVERITY = {
	ERROR: 'error',
	INFO: 'info',
	WARNING: 'warning',
	SUCCESS: 'success',
};

export const VARIANT = {
	FILLED: 'filled',
	OUTLINED: 'outlined',
};

export function Snackbar({ children }) {
	const {
		alertElementProps,
		snackbarOpen,
		autoHideDuration,
		setSnackbarOpen,
		setAlertElementProps,
	} = useNotificationContext();

	function handleClose(event, reason) {
		if (reason == 'clickaway') return;

		setSnackbarOpen(false);
		setAlertElementProps(null);
	}

	return (
		<>
			<MuiSnackbar
				open={snackbarOpen}
				autoHideDuration={autoHideDuration}
				onClose={handleClose}
				anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
			>
				{alertElementProps && (
					<Alert
						severity={alertElementProps.severity}
						variant={alertElementProps.variant}
						action={alertElementProps.action}
						onClose={handleClose}
					>
						{alertElementProps.alertTitle && (
							<AlertTitle>{alertElementProps.alertTitle}</AlertTitle>
						)}
						{alertElementProps.alertMessage}
					</Alert>
				)}
			</MuiSnackbar>
			{children}
		</>
	);
}
