import { createTheme } from '@mui/material/styles';

export const theme = createTheme({
	constants: {
		drawerWidth: 240
	},
	components: {
		MuiCssBaseline: {
			styleOverrides: (themeParam) => `
				html,
				body {
					padding: 0;
					margin: 0;
					font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Oxygen,
					Ubuntu, Cantarell, Fira Sans, Droid Sans, Helvetica Neue, sans-serif;
				}
				
				a {
					color: inherit;
					text-decoration: none;
				}
				
				* {
					box-sizing: border-box;
				}
			`,
		},
	},
});
