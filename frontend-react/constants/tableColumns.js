export const PLAYER_COLUMNS = [
    { id: 'dotaID', numeric: false, disablePadding: false, isDate: false, link: '', linkId: 'id', label: 'ID' },
    { id: 'created', numeric: false, disablePadding: false, isDate: true, label: 'Date Surveyed' },
    { id: 'mmr', numeric: false, disablePadding: false, isDate: false, label: 'MMR' },
    { id: 'medal', numeric: false, disablePadding: false, isDate: false, label: 'Medal' },
    { id: 'behavior_score', numeric: false, disablePadding: false, isDate: false, label: 'Behavior Score' },
    { id: 'role', numeric: false, disablePadding: false, isDate: false, label: 'Role' },
    { id: 'num_matches', numeric: false, disablePadding: false, isDate: false, label: 'Valid Matches' }
]

export const MATCH_COLUMNS = [
    { id: 'identifier', numeric: false, disablePadding: false, isDate: false, link:'/match', linkId: 'id', label: 'Match ID' },
    { id: 'date_fetched', numeric: false, disablePadding: false, isDate: true, label: 'Date Fetched' },
    { id: 'lobby_type', numeric: false, disablePadding: false, isDate: false, label: 'Lobby Type' },
    { id: 'fetch_status', numeric: false, disablePadding: false, isDate: false, label: 'Fetch Status' },
    { id: 'remarks', numeric: false, disablePadding: false, isDate: false, label: 'Remarks' },
]

export const MATCHMAKING_COLUMNS = [
    { id: 'dotaID', numeric: false, disablePadding: false, isDate: false, link: null, linkId: null, label: 'DoTA Account ID' },
    { id: 'role', numeric: false, disablePadding: false, isDate: false, link: null, linkId: null, label: 'Role' },
    { id: 'medal', numeric: false, disablePadding: false, isDate: false, link: null, linkId: null, label: 'Medal' },
    { id: 'mmr', numeric: false, disablePadding: false, isDate: false, link: null, linkId: null, label: 'MMR' },
    { id: 'behavior_score', numeric: false, disablePadding: false, isDate: false, link: null, linkId: null, label: 'Behavior Score' },
    { id: 'individual_fantasy', numeric: false, disablePadding: false, isDate: false, link: null, linkId: null, toFixed: 2, label: 'Fantasy' },
    { id: 'side', numeric: false, disablePadding: false, isDate: false, link: null, linkId: null, label: 'Side' },   
]

export const PLAYER_POOL_COLUMNS = [
    { id: 'dotaID', numeric: false, disablePadding: false, isDate: false, label: 'ID' },
    { id: 'mmr', numeric: false, disablePadding: false, isDate: false, label: 'MMR' },
    { id: 'medal', numeric: false, disablePadding: false, isDate: false, label: 'Medal' },
    { id: 'behavior_score', numeric: false, disablePadding: false, isDate: false, label: 'Behavior Score' },
    { id: 'role', numeric: false, disablePadding: false, isDate: false, label: 'Role' },
    { id: 'fantasy', numeric: false, disablePadding: false, isDate: false,toFixed: 2,label: 'Fantasy' }
]