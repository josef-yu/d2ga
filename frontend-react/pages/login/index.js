import Head from 'next/head';
import { LoginForm } from 'components/forms/LoginForm';
import { Footer } from 'components/footer/Footer';
import { useFormik } from 'formik';
import { Container } from '@mui/material';
import { styled } from '@mui/material/styles';
import { login } from 'api/auth';
import { useRouter } from 'next/router';
import { useEffect } from 'react';
import { LoginSchema } from 'utilities/validationSchema';

const StyledMain = styled('main')(theme => ({
	minHeight: '100vh',
	padding: '4rem 0',
	flex: 1,
	display: 'flex',
	flexDirection: 'column',
	justifyContent: 'center',
	alignItems: 'center',
}))

export default function Login() {
	const router = useRouter();

	const loginFormikProps = useFormik({
		initialValues: {
			username: '',
			password: '',
		},
		onSubmit: async (values, actions) => {
			actions.setSubmitting(true);
			try {
				const response = await login(values);

				if (!response) throw 'API/Network Failure';

				localStorage.setItem('token', response.data.auth_token);

				const returnUrl = router.query.returnUrl || '/';
				router.push(returnUrl);
			} catch (error) {
				console.error(error);
			}
			actions.setSubmitting(false);
		},
		validationSchema: LoginSchema,
	});

	useEffect(() => {
		const token = localStorage.getItem('token');
		if (token) router.push('/');
	}, []);

	return (
		<Container>
			<Head>
				<title>DoTA Matchmaking Algorithm</title>
				<meta name='description' content='DoTA Matchmaking Algorithm' />
				<link rel='icon' href='/favicon.ico' />
			</Head>

			<StyledMain>
				<LoginForm {...loginFormikProps} />
			</StyledMain>

			<Footer />
		</Container>
	);
}

Login.getLayout = function getLayout(page) {
	return (
		<>{page}</>
	)
}
