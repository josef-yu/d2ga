import { createContext, useContext, useState, useEffect } from "react";

const TableContext = createContext();

export function useTableContext() {
    return useContext(TableContext)
}

export function TableContextProvider({ children }) {

    
    return <TableContext.Provider>{children}</TableContext.Provider>
}