import { Grid, Typography, FormGroup } from '@mui/material';
import useSWR from 'swr'

export function PlayerInfo({ id }) {
    const { data: player } = useSWR(id ? [`users/players/${id}/`, null] : null)

	return (
		<Grid container direction='row' justifyContent='space-between'>
			<Grid item direction='column'>
				<FormGroup>
					<Typography variant='h6'>
						Account ID: <strong>{player?.dotaID}</strong>
					</Typography>

					<Typography variant='h6'>
						MMR: <strong>{player?.mmr}</strong>
					</Typography>

					<Typography variant='h6'>
						Role: <strong>{player?.role}</strong>
					</Typography>
				</FormGroup>
			</Grid>

			<Grid item direction='column'>
				<FormGroup>
					<Typography variant='h6'>
						Date Surveyed:{' '}
						<strong>
							{player &&
								new Date(player?.created).toLocaleString(
									{},
									{ dateStyle: 'long', timeStyle: 'short' }
								)}
						</strong>
					</Typography>

					<Typography variant='h6'>
						Medal: <strong>{player?.medal}</strong>
					</Typography>

					<Typography variant='h6'>
						Behavior Score: <strong>{player?.behavior_score}</strong>
					</Typography>
				</FormGroup>
			</Grid>

			<Grid item direction='column'>
				<Typography variant='h6'>
					Valid Matches: <strong>{player?.num_matches}</strong>
				</Typography>
			</Grid>
		</Grid>
	);
}
