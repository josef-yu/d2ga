import Head from 'next/head';
import { MainView } from 'components/main/MainView';
import { Table } from 'components/table/Table';
import { Box, Typography, Grid, IconButton, Tooltip } from '@mui/material';
import CloudSyncIcon from '@mui/icons-material/CloudSync';
import { PLAYER_COLUMNS } from 'constants/tableColumns';
import { syncSheetsData } from 'api/players';

export default function Players() {
	return (
		<>
			<Head>
				<title>Players - DoTA Matchmaking Algorithm</title>
				<meta name='description' content='DoTA Matchmaking Algorithm' />
				<link rel='icon' href='/favicon.ico' />
			</Head>
			<Box sx={{ marginTop: 1 }}>
				<Grid container direction='row' xs={12} md={6}>
					<Typography variant='h4'>Players</Typography>
					<Tooltip title='Sync sheets data' placement='right'>
						<IconButton
							color='primary'
							aria-label='Sync sheets data'
							component='label'
							onClick={syncSheetsData}
						>
							<CloudSyncIcon />
						</IconButton>
					</Tooltip>
				</Grid>
				<Table columns={PLAYER_COLUMNS} APIPath='/users/players/' />
			</Box>
		</>
	);
}

Players.getLayout = function getLayout(page) {
	return <MainView>{page}</MainView>;
};
