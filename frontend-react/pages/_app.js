import { StyledEngineProvider, ThemeProvider } from '@mui/material/styles';
import CssBaseLine from '@mui/material/CssBaseline';
import { theme } from 'styles/theme';
import { RouteGuard } from 'components/private-route/RouteGuard';
import { NotificationContextProvider } from 'components/notification/NotificationContext';
import { SWRConfig as SWRConfigComponent } from 'swr';
import { SWRConfig } from 'utilities/swrConfig'
import { ReactHooksWrapper } from 'react-hooks-outside'

function MyApp({ Component, pageProps }) {
	const getLayout = Component.getLayout || ((page) => page);
	return (
		<StyledEngineProvider injectFirst>
			<ThemeProvider theme={theme}>
				<NotificationContextProvider>
					<SWRConfigComponent value={SWRConfig}>
						<ReactHooksWrapper />
						<CssBaseLine />
						<RouteGuard>{getLayout(<Component {...pageProps} />)}</RouteGuard>
					</SWRConfigComponent>
				</NotificationContextProvider>
			</ThemeProvider>
		</StyledEngineProvider>
	);
}

export default MyApp;
