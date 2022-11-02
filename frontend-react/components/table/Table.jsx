import {
	Paper,
	TableContainer,
	TablePagination,
	TableRow,
	TableCell,
	TableBody,
	Table as MuiTable,
} from '@mui/material';
import { useState, useEffect } from 'react';
import { TableHead } from './TableHead';
import { TableActions } from './TableActions';
import Link from 'next/link';
import MuiLink from '@mui/material/Link';
import { useRouter } from 'next/router';
import { useAPIPagination } from 'utilities/useAPIPagination';

function usePagination(disableRouter = false) {
	const router = useRouter();
	const [page, setPage] = useState(0);
	const [rowsPerPage, setRowsPerPage] = useState(10);

	function handleChangePage(event, newPage) {
		setPage(newPage);

		if (!disableRouter) {
			router.query.page = parseInt(newPage) + 1;
			const url = {
				pathname: router.pathname,
				query: router.query,
			};
			router.replace(url, undefined, { shallow: true });
		}
	}

	function handleChangeRowsPerPage(event) {
		setRowsPerPage(+event.target.value);
		setPage(0);
	}

	useEffect(() => {
		if (!router.isReady) return;

		if (router.query?.page) {
			const startPage = parseInt(router.query?.page) - 1;
			setPage(startPage);
		}
	}, [router.isReady]);

	return {
		page,
		rowsPerPage,
		handleChangePage,
		handleChangeRowsPerPage,
	};
}

function useSort(disableRouter = false) {
	const router = useRouter();
	const [order, setOrder] = useState('');
	const [sortedColumn, setSortedColumn] = useState('id');

	function handleSortColumn(event, property) {
		const isAsc = sortedColumn === property && order === '';
		setOrder(isAsc ? '-' : '');
		setSortedColumn(property);

		if (!disableRouter) {
			router.query.sort = (isAsc ? '-' : '') + property;
			const url = {
				pathname: router.pathname,
				query: router.query,
			};
			router.replace(url, undefined, { shallow: true });
		}
	}

	useEffect(() => {
		if (!router.isReady) return;

		if (router.query?.sort) {
			setSortedColumn(router.query.sort);
		}
	}, [router.isReady]);

	return {
		sortedColumn,
		order,
		handleSortColumn,
	};
}

export function Table({
	APIPath,
	columns,
	collapsible,
	actionProps = null,
	disableRouter = false,
	swrOptions = {}
}) {
	const router = useRouter();
	const { page, rowsPerPage, handleChangePage, handleChangeRowsPerPage } =
		usePagination(disableRouter);

	const { sortedColumn, order, handleSortColumn } = useSort(disableRouter);

	const { data } = useAPIPagination([
		APIPath,
		{
			page: parseInt(page) + 1,
			page_size: rowsPerPage,
			ordering: order + sortedColumn,
		},
	], swrOptions);

	const rows = data?.results ?? [];
	const count = data?.count ?? 0;

	function renderRowCell(row, header) {
		if (header.isDate) {
			return new Date(row[header.id]).toLocaleString(
				{},
				{ dateStyle: 'long', timeStyle: 'short' }
			);
		} else if (header.link != null) {
			const path = router.asPath.split('?')[0];
			const url = `${path}${header.link}/${row[header.linkId]}`;
			return (
				<Link href={url}>
					<MuiLink href={url}>{row[header.id]}</MuiLink>
				</Link>
			);
		} else if (header.toFixed != null) {
			return row[header.id].toFixed(header.toFixed);
		} else {
			return row[header.id];
		}
	}

	if (!router.isReady) return null;

	return (
		<Paper>
			<TableContainer sx={{ width: '100%' }}>
				<MuiTable sx={{ width: '100%' }}>
					<TableHead
						hasActions={Boolean(actionProps)}
						columns={columns}
						collapsbile={collapsible}
						sortedColumn={sortedColumn}
						handleSortColumn={handleSortColumn}
						order={order}
					/>
					<TableBody>
						{rows.map((row, index) => (
							<TableRow key={`tablerow-${index}`}>
								{columns.map((header) => (
									<TableCell key={`tablerow-cell-${header.id}-${index}`}>
										{renderRowCell(row, header)}
									</TableCell>
								))}
								{actionProps && (
									<TableActions actions={actionProps?.elements} />
								)}
							</TableRow>
						))}
					</TableBody>
				</MuiTable>
			</TableContainer>

			<TablePagination
				rowsPerPageOptions={[10, 15, 20]}
				component='div'
				rowsPerPage={rowsPerPage}
				count={count}
				page={page * rowsPerPage > count ? 0 : page}
				onPageChange={handleChangePage}
				onRowsPerPageChange={handleChangeRowsPerPage}
			/>
		</Paper>
	);
}
