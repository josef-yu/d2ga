import {
	TextField,
	Paper,
	Button,
	Grid,
	InputAdornment,
	IconButton,
} from '@mui/material';
import VisibilityIcon from '@mui/icons-material/Visibility';
import VisibilityOff from '@mui/icons-material/VisibilityOff';
import LoadingButton from '@mui/lab/LoadingButton';
import { useState } from 'react';

export function LoginForm({ ...formikProps }) {
	const { values, handleSubmit, handleChange, errors, isSubmitting } =
		formikProps;
	const [isShowPass, setIsShowPass] = useState(false);

	const handleClickShowPassword = () => {
		setIsShowPass((curr) => !curr);
	};

	const handleMouseDownPassword = (event) => {
		event.preventDefault();
	};

	return (
		<form onSubmit={handleSubmit}>
			<Paper
				variant='outlined'
				sx={{ width: '20em', paddingY: 2, paddingLeft: 2 }}
			>
				<Grid
					container
					direction='column'
					justifyContent='center'
					alignItems='stretch'
					spacing={3}
					xs={12}
				>
					<Grid item>
						<TextField
							type='text'
							variant='standard'
							name='username'
							label='Username'
							value={values.username}
							helperText={errors.username}
							error={Boolean(errors.username)}
							onChange={handleChange}
							fullWidth
						/>
					</Grid>

					<Grid item>
						<TextField
							type={isShowPass ? 'text' : 'password'}
							variant='standard'
							name='password'
							label='Password'
							value={values.password}
							helperText={errors.password}
							error={Boolean(errors.password)}
							onChange={handleChange}
							InputProps={{
								endAdornment: (
									<InputAdornment position='end'>
										<IconButton
											aria-label='toggle password visibility'
											onClick={handleClickShowPassword}
											onMouseDown={handleMouseDownPassword}
											edge='end'
										>
											{isShowPass ? <VisibilityOff /> : <VisibilityIcon />}
										</IconButton>
									</InputAdornment>
								),
							}}
							fullWidth
						/>
					</Grid>

					<Grid item xs={12}>
						<LoadingButton
							variant='outlined'
							type='submit'
							loading={isSubmitting}
							fullWidth
						>
							Login
						</LoadingButton>
					</Grid>
				</Grid>
			</Paper>
		</form>
	);
}
