import { useRouter } from 'next/router';

export default function Logout() {
	const router = useRouter();
	localStorage.clear();
    router.push('/login')

	return null;
}
