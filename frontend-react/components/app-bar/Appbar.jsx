import {
	AppBar as MuiAppBar,
	Toolbar,
	IconButton,
	Typography,
	Box,
} from '@mui/material';
import { styled } from '@mui/material/styles';
import MenuIcon from '@mui/icons-material/Menu';
import dynamic from 'next/dynamic';

const NotificationCenter = dynamic(
	() => import('react-notification-center-component'),
	{
		ssr: false,
	}
);

const AppBar = styled(MuiAppBar, {
	shouldForwardProp: (prop) => prop !== 'open',
})(({ theme, open }) => ({
	zIndex: theme.zIndex.drawer + 1,
	backgroundColor: 'gray',
	transition: theme.transitions.create(['width', 'margin'], {
		easing: theme.transitions.easing.sharp,
		duration: theme.transitions.duration.leavingScreen,
	}),
	...(open && {
		marginLeft: theme.constants.drawerWidth,
		width: `calc(100% - ${theme.constants.drawerWidth}px)`,
		transition: theme.transitions.create(['width', 'margin'], {
			easing: theme.transitions.easing.sharp,
			duration: theme.transitions.duration.enteringScreen,
		}),
	}),
}));

const NotifCenter = styled(NotificationCenter)(({ theme }) => ({
	width: '500px',
	height: '50px',
	color: 'black'
}));

export function Appbar({ open, handleDrawerOpen, title }) {
	return (
		<>
			<AppBar position='fixed' open={open}>
				<Toolbar>
					<IconButton
						color='inherit'
						aria-label='open drawer'
						onClick={handleDrawerOpen}
						edge='start'
						sx={{
							marginRight: 5,
							...(open && { display: 'none' }),
						}}
					>
						<MenuIcon />
					</IconButton>
					<Typography variant='h6' noWrap component='div'>
						{title}
					</Typography>
					<Box sx={{ flexGrow: 1 }} />
					<Box>
						<NotifCenter appId='dijF5JL6fH' subscriberId='d2gaapp' />
					</Box>
				</Toolbar>
			</AppBar>
		</>
	);
}
