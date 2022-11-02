import Head from 'next/head';
import { useRouter } from 'next/router';
import { MainView } from 'components/main/MainView';
import { PlayerInfo } from 'components/player/PlayerInfo';
import { PlayerMatches } from 'components/player/PlayerMatches';
import { Box, Grid, Typography, IconButton, Tooltip } from '@mui/material';
import CloudSyncIcon from '@mui/icons-material/CloudSync';
import { fetchPlayerMatches } from 'api/players';

export default function PlayerInfoPage() {
	const router = useRouter();
	const id = router.query.playerId;

	function handleSyncMatches() {
		if (id) fetchPlayerMatches(id);
	}

	return (
		<>
			<Head>
				<title>{`Player ${id} - DoTA Matchmaking Algorithm`}</title>
				<meta name='description' content='DoTA Matchmaking Algorithm' />
				<link rel='icon' href='/favicon.ico' />
			</Head>
			<Box sx={{ marginTop: 1 }}>
				<Grid container direction='row' xs={12} md={6}>
					<Typography variant='h4'>{`Player ${id}`}</Typography>
					<Tooltip title='Fetch player matches' placement='right'>
						<IconButton
							color='primary'
							aria-label='Fetch player matches'
							component='label'
							onClick={handleSyncMatches}
						>
							<CloudSyncIcon />
						</IconButton>
					</Tooltip>
				</Grid>
				<Grid container direction='column' xs={12} md={9}>
					<PlayerInfo id={id} />
				</Grid>
				<PlayerMatches id={id} />
			</Box>
		</>
	);
}

PlayerInfoPage.getLayout = function getLayout(page) {
	return <MainView>{page}</MainView>;
};
