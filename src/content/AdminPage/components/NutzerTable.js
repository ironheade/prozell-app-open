import {Checkbox, DataTable, Table, TableBody, TableCell, TableHead, TableHeader, TableRow, TableToolbar } from "carbon-components-react";
import { interpolateWarm } from "d3";
import React, {useState} from "react";

export default function NutzerTable(props){
    console.table(props.data)
    const [isChecked, setIsChecked] = useState(false)

    const headers=[
        {
          header: 'Nutzername',
          key: 'Nutzername'
        },
        {
          header: 'Startzeit',
          key: 'Startzeit'
        },
        {
          header: 'Endzeit',
          key: 'Endzeit'
        },
        {
          header: 'Kommentar',
          key: 'Kommentar'
        }, 
        {
          header: 'Startzeit in MS',
          key: 'StartzeitMS'
        },
        {
          header: 'Endzeit in MS',
          key: 'EndzeitMS'
        }

      ]

      const rows = props.data.map(item => ({ ...item, id: item["id"].toString(),
      Startzeit:item.Startzeit.split(",")[0],
      Endzeit:item.Endzeit.split(",")[0] }))
      .filter(isChecked ? item => item.EndzeitMS > Date.now() : item => item)

    return(
        <>

        <h3 >Alle Nutzer</h3>
        <Checkbox id="checkbox" labelText="nur aktive Nutzer" checked={isChecked} onChange={()=>isChecked?setIsChecked(false):setIsChecked(true)} />

        <DataTable rows={rows} headers={headers} isSortable useZebraStyles size="short">
        {({ rows, headers, getTableProps, getHeaderProps, getRowProps }) => (
            
            <Table {...getTableProps()}>
            <TableHead>
                <TableRow>
                {headers.map((header) => (
                    <TableHeader {...getHeaderProps({ header })}>
                    {header.header}
                    </TableHeader>
                ))}
                </TableRow>
            </TableHead>
            <TableBody>
                {rows.map((row) => (
                <TableRow {...getRowProps({ row })}>
                    {row.cells.map((cell) => (
                    <TableCell key={cell.id}>{cell.value}</TableCell>
                    ))}
                </TableRow>
                ))}
            </TableBody>
            </Table>
        )}
        </DataTable>

        </>
    )
}