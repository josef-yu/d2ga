import {
	TableHead as MuiTableHead,
	TableRow,
	TableCell,
	TableSortLabel,
	Box,
} from '@mui/material';
import { visuallyHidden } from '@mui/utils';

export function TableHead({
	columns,
	collapsible,
	sortedColumn,
	order,
	handleSortColumn,
	hasActions,
}) {
	const direction = order == '-' ? 'desc' : 'asc';
	const createSortHandler = (property) => (event) => {
		handleSortColumn(event, property);
	};

	return (
		<MuiTableHead>
			<TableRow>
				{collapsible ? <TableCell /> : <></>}
				{columns.map((column) => (
					<TableCell
						key={`tableheader-${column.id}`}
						align={column.numeric ? 'right' : 'left'}
						padding={column.disablePadding ? 'none' : 'normal'}
						sortDirection={sortedColumn === column.id ? direction : false}
					>
						<TableSortLabel
							active={sortedColumn === column.id}
							direction={sortedColumn === column.id ? direction : 'asc'}
							onClick={createSortHandler(column.id)}
						>
							{column.label}
							{sortedColumn === column.id ? (
								<Box component='span' sx={visuallyHidden}>
									{direction === 'desc'
										? 'sorted descending'
										: 'sorted ascending'}
								</Box>
							) : null}
						</TableSortLabel>
					</TableCell>
				))}
				{hasActions ? <TableCell>Actions</TableCell> : <></>}
			</TableRow>
		</MuiTableHead>
	);
}
