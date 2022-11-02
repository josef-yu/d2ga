import Head from 'next/head';
import { MainView } from 'components/main/MainView';
import { BarGraph } from 'components/charts/BarGraph';
import {
	Box,
	Typography,
	Grid,
	Paper,
	CircularProgress,
	Select,
	MenuItem,
} from '@mui/material';
import { useState } from 'react';
import useSWR from 'swr';
import { CssRounded } from '@mui/icons-material';

export default function Home() {
	const [playerBreakdownCriteria, setPlayerBreakdownCriteria] =
		useState('role');
	const [matchBreakdownCriteria, setMatchBreakdownCriteria] = useState('role');
	const [statsBreakdownCriteria, setStatsBreakdownCriteria] = useState('all');

	const { data: playerCount, error: playerError } = useSWR(
		`/users/count/${playerBreakdownCriteria}`
	);
	const { data: matchCount, error: matchError } = useSWR(
		`/users/match/count/${matchBreakdownCriteria}`
	);
	const { data: statsCount, error: statsError } = useSWR(
		`/users/average/${statsBreakdownCriteria}`
	);
	let kda
	let cs
	let bigStats

	function handlePlayerSelectChange(event) {
		setPlayerBreakdownCriteria(event.target.value);
	}

	function handleMatchSelectChange(event) {
		setMatchBreakdownCriteria(event.target.value);
	}

	function handleStatsSelectChange(event) {
		setStatsBreakdownCriteria(event.target.value);
	}

	if (playerError) {
		playerCount.count = 0;
	}

	if (matchError) {
		matchCount.count = 0;
	}

	if (statsError) {
		statsCount.count = 0
	} else {
		kda = statsCount?.breakdown?.slice(0, 3) ?? []
		cs = statsCount?.breakdown?.slice(3,6) ?? []
		bigStats = statsCount?.breakdown?.slice(6) ?? []
	}

	return (
		<>
			<Head>
				<title>DoTA Matchmaking Algorithm</title>
				<meta name='description' content='DoTA Matchmaking Algorithm' />
				<link rel='icon' href='/favicon.ico' />
			</Head>
			<Box sx={{ marginTop: 1 }}>
				<Typography variant='h4'>Dashboard</Typography>
				<Grid container display='flex' direction='column' spacing={2}>
					<Grid item>
						<Grid container spacing={3}>
							<Grid item xs={12} md={4}>
								<Paper
									sx={{
										height: 130,
										padding: '10px 10px',
										border: '2px solid #1A86D3',
									}}
								>
									<Typography variant='h6'>Total Players</Typography>
									{playerCount?.total >= 0 ? (
										<Typography variant='h3' align='center'>
											{playerCount?.total}
										</Typography>
									) : (
										<Grid
											container
											item
											display='flex'
											justifyContent='center'
											alignItems='center'
										>
											<CircularProgress />
										</Grid>
									)}
								</Paper>
							</Grid>
							<Grid item xs={12} md={4}>
								<Paper
									sx={{
										height: 130,
										padding: '10px 10px',
										border: '2px solid #1A86D3',
									}}
								>
									<Typography variant='h6'>Valid Matches</Typography>
									{matchCount?.total >= 0 ? (
										<Typography variant='h3' align='center'>
											{matchCount?.total}
										</Typography>
									) : (
										<Grid
											container
											item
											display='flex'
											justifyContent='center'
											alignItems='center'
										>
											<CircularProgress />
										</Grid>
									)}
								</Paper>
							</Grid>
						</Grid>
					</Grid>

					<Grid item>
						<Grid container spacing={3}>
							<Grid item xs={12} md={7}>
								<Paper sx={{ minHeight: 260, padding: '20px 20px' }}>
									<Grid
										container
										direction='row'
										justifyContent='space-between'
									>
										<Typography variant='h5'>Player Breakdown</Typography>
										{playerCount?.breakdown && (
											<Select
												value={playerBreakdownCriteria}
												onChange={handlePlayerSelectChange}
											>
												<MenuItem value='role'>by role</MenuItem>
												<MenuItem value='medal'>by medal</MenuItem>
											</Select>
										)}
									</Grid>
									{playerCount?.breakdown ? (
										<BarGraph
											data={playerCount?.breakdown}
											XAxisLabel='name'
											dataKeys={[{ key: 'count', color: '#8884d8' }]}
											margin={{ top: 20, right: 30, left: 0, bottom: 0 }}
											minHeight={260}
											tooltip
										/>
									) : playerCount?.total == 0 ? (
										<Grid
											container
											item
											display='flex'
											justifyContent='center'
											alignItems='center'
											sx={{ height: '180px' }}
										>
											<Typography variant='h4'>No data</Typography>
										</Grid>
									) : (
										<Grid
											container
											item
											display='flex'
											justifyContent='center'
											alignItems='center'
											sx={{ height: '180px' }}
										>
											<CircularProgress />
										</Grid>
									)}
								</Paper>
							</Grid>
						</Grid>
					</Grid>

					<Grid item>
						<Grid container spacing={3}>
							<Grid item xs={12} md={7}>
								<Paper sx={{ minHeight: 260, padding: '20px 20px' }}>
									<Grid
										container
										direction='row'
										justifyContent='space-between'
									>
										<Typography variant='h5'>Match Breakdown</Typography>
										{matchCount?.breakdown && (
											<Select
												value={matchBreakdownCriteria}
												onChange={handleMatchSelectChange}
											>
												<MenuItem value='role'>by role</MenuItem>
												<MenuItem value='medal'>by medal</MenuItem>
											</Select>
										)}
									</Grid>
									{matchCount?.breakdown ? (
										<BarGraph
											data={matchCount?.breakdown}
											XAxisLabel='name'
											dataKeys={[{ key: 'count', color: '#8884d8' }]}
											margin={{ top: 20, right: 30, left: 0, bottom: 0 }}
											minHeight={260}
											tooltip
										/>
									) : matchCount?.total == 0 ? (
										<Grid
											container
											item
											display='flex'
											justifyContent='center'
											alignItems='center'
											sx={{ height: '180px' }}
										>
											<Typography variant='h4'>No data</Typography>
										</Grid>
									) : (
										<Grid
											container
											item
											display='flex'
											justifyContent='center'
											alignItems='center'
											sx={{ height: '180px' }}
										>
											<CircularProgress />
										</Grid>
									)}
								</Paper>
							</Grid>
						</Grid>
					</Grid>

					<Grid item>
						<Grid container spacing={3}>
							<Grid item xs={12} md={7}>
								<Paper sx={{ minHeight: 260, padding: '20px 20px' }}>
									<Grid
										container
										direction='row'
										justifyContent='space-between'
									>
										<Typography variant='h5'>Stats Breakdown</Typography>
										{statsCount?.breakdown && (
											<Select
												value={statsBreakdownCriteria}
												onChange={handleStatsSelectChange}
											>
												<MenuItem value='all'>All</MenuItem>
												<MenuItem value='1'>Safe Lane</MenuItem>
												<MenuItem value='2'>Mid Lane</MenuItem>
												<MenuItem value='3'>Off Lane</MenuItem>
												<MenuItem value='4'>Soft Support</MenuItem>
												<MenuItem value='5'>Hard Support</MenuItem>
											</Select>
										)}
									</Grid>
									{statsCount?.breakdown ? (
										<>
											<BarGraph
												data={kda}
												XAxisLabel='name'
												dataKeys={[{ key: 'count', color: '#8884d8' }]}
												margin={{ top: 20, right: 30, left: 0, bottom: 0 }}
												minHeight={260}
												tooltip
											/>
											<BarGraph
												data={cs}
												XAxisLabel='name'
												dataKeys={[{ key: 'count', color: '#8884d8' }]}
												margin={{ top: 20, right: 30, left: 0, bottom: 0 }}
												minHeight={260}
												tooltip
											/>
											<BarGraph
												data={bigStats}
												XAxisLabel='name'
												dataKeys={[{ key: 'count', color: '#8884d8' }]}
												margin={{ top: 20, right: 30, left: 0, bottom: 0 }}
												minHeight={260}
												tooltip
											/>
										</>
									) : statsCount?.total == 0 ? (
										<Grid
											container
											item
											display='flex'
											justifyContent='center'
											alignItems='center'
											sx={{ height: '180px' }}
										>
											<Typography variant='h4'>No data</Typography>
										</Grid>
									) : (
										<Grid
											container
											item
											display='flex'
											justifyContent='center'
											alignItems='center'
											sx={{ height: '180px' }}
										>
											<CircularProgress />
										</Grid>
									)}
								</Paper>
							</Grid>
						</Grid>
					</Grid>
				</Grid>
			</Box>
		</>
	);
}

Home.getLayout = function getLayout(page) {
	return <MainView>{page}</MainView>;
};
