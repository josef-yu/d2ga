import Head from 'next/head';
import { MainView } from 'components/main/MainView';
import { Button, Box, Grid, Typography } from '@mui/material';
import { findMatch } from 'api/matchmaking';
import { useState } from 'react';
import { MATCHMAKING_COLUMNS } from 'constants/tableColumns';
import { MatchmakingState } from 'components/matchmaking/MatchmakingState';

export default function MatchmakingPage() {
	const [matchmakingId, setMatchmakingId] = useState();

	async function clickFindMatch() {
		let response = await findMatch();
		setMatchmakingId(await response.data.matchmaking_id);
	}
	return (
		<>
			<Head>
				<title>{`Matchmaking - DoTA Matchmaking Algorithm`}</title>
				<meta name='description' content='DoTA Matchmaking Algorithm' />
				<link rel='icon' href='/favicon.ico' />
			</Head>
			<Box sx={{ marginTop: 1 }}>
				<Grid container direction='row' xs={12} md={6}>
					<Typography variant='h4'>Matchmaking</Typography>
					{!matchmakingId && <Button
						variant='contained'
						onClick={clickFindMatch}
						disabled={Boolean(matchmakingId)}
						sx={{ marginLeft: 2 }}
					>
						Start
					</Button>}

					{matchmakingId && <Button
						variant='contained'
						onClick={() => { setMatchmakingId(null) }}
						sx={{ marginLeft: 2 }}
					>
						Reset
					</Button>}
				</Grid>
				{matchmakingId && <MatchmakingState id={matchmakingId} />}
			</Box>
		</>
	);
}

MatchmakingPage.getLayout = function getLayout(page) {
	return <MainView>{page}</MainView>;
};
