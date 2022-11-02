import { Appbar } from 'components/app-bar/Appbar';
import { Drawer } from 'components/drawer/Drawer';
import { DrawerHeader } from 'components/drawer/DrawerHeader';
import { Snackbar } from 'components/notification/Snackbar';
import { useState } from 'react';
import { Box } from '@mui/material';
import { styled } from '@mui/material/styles';

export function MainView({ children, ...props }) {
	const [open, setOpen] = useState(false);

	function handleDrawerOpen() {
		setOpen(true);
	}

	function handleDrawerClose() {
		setOpen(false);
	}

	return (
		<Box sx={{ display: 'flex' }}>
			<Appbar
				open={open}
				handleDrawerOpen={handleDrawerOpen}
				title='DoTA 2 Matchmaking Algorithm'
			/>
			<Drawer open={open} handleDrawerClose={handleDrawerClose} />
			<Box
				component='main'
				open={open}
				{...props}
				sx={{ flexGrow: 1, paddingLeft: 3, paddingRight: 3 }}
			>
				<DrawerHeader />
				<Snackbar>{children}</Snackbar>
			</Box>
		</Box>
	);
}
