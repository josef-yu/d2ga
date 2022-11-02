import {
	Drawer as MuiDrawer,
	IconButton,
	List,
	ListItem,
	ListItemButton,
	ListItemIcon,
	ListItemText,
	Divider,
	Tooltip,
} from '@mui/material';
import { useTheme } from '@mui/styles';
import { styled } from '@mui/material/styles';
import { PRIVATE_ROUTES } from 'constants/routes';
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';
import { DrawerHeader } from './DrawerHeader';
import Link from 'next/link';

const openedMixin = (theme) => ({
	width: theme.constants.drawerWidth,
	transition: theme.transitions.create('width', {
		easing: theme.transitions.easing.sharp,
		duration: theme.transitions.duration.enteringScreen,
	}),
	overflowX: 'hidden',
});

const closedMixin = (theme) => ({
	transition: theme.transitions.create('width', {
		easing: theme.transitions.easing.sharp,
		duration: theme.transitions.duration.leavingScreen,
	}),
	overflowX: 'hidden',
	width: `calc(${theme.spacing(7)} + 1px)`,
	[theme.breakpoints.up('sm')]: {
		width: `calc(${theme.spacing(8)} + 1px)`,
	},
});

const StyledDrawer = styled(MuiDrawer, {
	shouldForwardProp: (prop) => prop !== 'open',
})(({ theme, open }) => ({
	width: theme.constants.drawerWidth,
	flexShrink: 0,
	whiteSpace: 'nowrap',
	boxSizing: 'border-box',
	...(open && {
		...openedMixin(theme),
		'& .MuiDrawer-paper': openedMixin(theme),
	}),
	...(!open && {
		...closedMixin(theme),
		'& .MuiDrawer-paper': closedMixin(theme),
	}),
}));

export function Drawer({ open, handleDrawerClose }) {
	const theme = useTheme();
	return (
		<StyledDrawer variant='permanent' open={open}>
			<DrawerHeader>
				<IconButton onClick={handleDrawerClose}>
					{theme.direction === 'rtl' ? (
						<ChevronRightIcon />
					) : (
						<ChevronLeftIcon />
					)}
				</IconButton>
			</DrawerHeader>
			<Divider />
			<List>
				{Object.values(PRIVATE_ROUTES).map((obj) => (
					<Tooltip
						title={open ? '' : obj.text}
						placement='right'
						key={`drawer-tooltip-${obj.text}`}
					>
						<ListItem key={obj.text} disablePadding sx={{ display: 'block' }}>
							<Link href={obj.path}>
								<ListItemButton
									sx={{
										minHeight: 48,
										justifyContent: open ? 'initial' : 'center',
										px: 2.5,
									}}
								>
									<ListItemIcon
										sx={{
											minWidth: 0,
											mr: open ? 3 : 'auto',
											justifyContent: 'center',
										}}
									>
										{obj.icon}
									</ListItemIcon>
									<ListItemText
										primary={obj.text}
										sx={{ opacity: open ? 1 : 0 }}
									/>
								</ListItemButton>
							</Link>
						</ListItem>
					</Tooltip>
				))}
			</List>
		</StyledDrawer>
	);
}
