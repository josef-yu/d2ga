import { Table } from 'components/table/Table'
import { MATCH_COLUMNS } from 'constants/tableColumns'

export function PlayerMatches({ id }) {
    return (
        <>
            {id && <Table columns={MATCH_COLUMNS} APIPath={`users/matches/${id}`}/>}
        </>
    )
}