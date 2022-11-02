import { styled } from '@mui/material/styles'
import Image from 'next/image';

const StyledSpan = styled('span')(theme => ({
	height: '1em',
	marginLeft: '0.5rem',
}))

const StyledFooter = styled('footer')(theme => ({
	display: 'flex',
	flex: 1,
	padding: '2rem 0',
	borderTop: '1px solid #eaeaea',
	justifyContent: 'center',
	alignItems: 'center',
	'& a': {
		display: 'flex',
		justifyContent: 'center',
		alignItems: 'center',
		flexGrow: 1,
	},
}))

export function Footer() {
	return (
		<StyledFooter>
			<a
				href='https://vercel.com?utm_source=create-next-app&utm_medium=default-template&utm_campaign=create-next-app'
				target='_blank'
				rel='noopener noreferrer'
			>
				Powered by{' '}
				<StyledSpan>
					<Image src='/vercel.svg' alt='Vercel Logo' width={72} height={16} />
				</StyledSpan>
			</a>
		</StyledFooter>
	);
}
