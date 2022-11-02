import useSWR from 'swr';
import {
	MATCHMAKING_COLUMNS,
	PLAYER_POOL_COLUMNS,
} from 'constants/tableColumns';
import { InlineMath } from 'react-katex';
import { Grid, Typography, FormGroup, Box } from '@mui/material';
import { Table } from 'components/table/Table';
import 'katex/dist/katex.min.css';

export function MatchmakingState({ id }) {
	const { data } = useSWR(id ? 'users/matchmaking?id=' + id : null);
	let results = {};

	if (data) results = data.optimal[0];
	return (
		<>
			<Grid container direction='column' xs={12} md={9}>
				<Grid container direction='row' justifyContent='space-between'>
					<Grid item direction='column'>
						<FormGroup>
							<Typography variant='h6'>
								Matchmaking ID: <strong>{id}</strong>
							</Typography>

							<Typography variant='h6'>
								Elapsed Time: <strong>{results?.elapsed_time ?? ''}</strong>
							</Typography>

							<Typography variant='h6'>
								Status: <strong>{data?.status ?? ''}</strong>
							</Typography>

							<Typography variant='h6'>
								Generation: <strong>{results?.generation ?? ''}</strong>
							</Typography>
						</FormGroup>
					</Grid>

					<Grid item direction='column'>
						<FormGroup>
							<Typography variant='h6'>
								Imbalance <InlineMath math='f' />:{' '}
								<strong>{results?.imbalance ?? ''}</strong>
							</Typography>

							<Typography variant='h6'>
								{/* f1: <strong>{results?.f_mmr ?? ''}</strong> */}
								<InlineMath math='f_{1}' />:{' '}
								<strong>{results?.f_mmr ?? ''}</strong>
							</Typography>

							<Typography variant='h6'>
								{/* f2: */}
								<InlineMath math='f_{2}' />:{' '}
								<strong>{results?.f_behavior_score ?? ''}</strong>
							</Typography>

							<Typography variant='h6'>
								{/* f3: */}
								<InlineMath math='f_{3}' />:{' '}
								<strong>{results?.f_fantasy ?? ''}</strong>
							</Typography>
						</FormGroup>
					</Grid>

					<Grid item direction='column'>
						<FormGroup>
							<Typography variant='h6'>
								Remarks:
								<strong>{data?.remarks ?? 'None'}</strong>
							</Typography>

							<Typography variant='h6'>
								Iterations:{' '}
								{results?.generation && (
									<strong>
										{data?.status == 'Found'
											? results?.generation + 25
											: results?.generation}
									</strong>
								)}
							</Typography>
						</FormGroup>
					</Grid>
				</Grid>
			</Grid>
			<Box sx={{ marginTop: 1 }}>
				<Typography variant='h5'>Matched Players</Typography>
				<Table
					columns={MATCHMAKING_COLUMNS}
					APIPath={'/users/matchmaking?id=' + id}
				/>
			</Box>
			<Box sx={{ marginTop: 1 }}>
				<Typography variant='h5'>Player Pool</Typography>
				<Table
					columns={PLAYER_POOL_COLUMNS}
					APIPath={'/users/matchmaking/pool/' + id}
					disableRouter={true}
					swrOptions={{ refreshInterval: 0 }}
				/>
			</Box>
		</>
	);
}
