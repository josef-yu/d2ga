import DashboardIcon from '@mui/icons-material/Dashboard';
import LogoutIcon from '@mui/icons-material/Logout';
import PeopleAltIcon from '@mui/icons-material/PeopleAlt';
import SportsEsportsIcon from '@mui/icons-material/SportsEsports';

export const PUBLIC_ROUTES = {
    'LOGIN': '/login'
}

export const PRIVATE_ROUTES = {
    'HOME': {
        path: '/',
        icon: <DashboardIcon />,
        text: 'Home'
    },
    'PLAYERS': {
        path: '/players',
        icon: <PeopleAltIcon />,
        text: 'Players'
    },
    'MATCHMAKING': {
        path: '/matchmaking',
        icon: <SportsEsportsIcon />,
        text: 'Matchmaking'
    },
    'LOGOUT': {
        path: '/logout',
        icon: <LogoutIcon />,
        text: 'Logout'
    }
}