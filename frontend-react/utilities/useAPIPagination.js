import useSWR from 'swr';

export function useAPIPagination(key, swrOptions) {
	var results;

	const { data } = useSWR(key, swrOptions);
	const params = key[1];
	useSWR(
		params && data?.next ? [key[0], { ...params, page: params.page + 1 }] : null,
		swrOptions
	);

	results = data;

	if (key[0].includes('matchmaking') && !key[0].includes('pool')) {
		results = {
			results: data?.optimal ?? [],
			count: data?.optimal?.length ?? 0,
		};

		if (data && data.status == 'Failed') {
			results.results = [];
			results.count = 0;
		}
	}

	return { data: results };
}
