import { TableCell } from '@mui/material'

export function TableActions({ actions }) {


    return (
        <TableCell>
            {actions.map(item => (item))}
        </TableCell>
    )
}