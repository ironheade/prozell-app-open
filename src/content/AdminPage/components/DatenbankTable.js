import { Button, DataTable, Dropdown, NumberInput, Table, TableBody, TableCell, TableContainer, TableHead, TableHeader, TableRow, TextInput } from "carbon-components-react";
import React, { useState, useEffect } from "react";
import tabelle_abrufen from '../../../functions/tabelle_abrufen'

export default function DatenbankTable() {

    //Daten der altuell ausgewählten Tabelle
    const [data, setData] = useState([{ "id": 1, "Beschreibung": "keine" }])
    //Alle Tabellen
    const [allTables, setAllTables] = useState(null)
    //Name der aktuell ausgewählten Tabelle
    const [currentTable, setCurrentTable] = useState("Tabelle auswählen")

    const headerData = Object.keys(data[0]).map(item => ({ header: item, key: item }))
    const rowData = data.map(item => ({ ...item, id: item["id"].toString() }))

    function handleChange(value, id, column) {
        var newData = [...data]
        var newObject = newData.filter(item => item.id === id)[0]
        const index = newData.indexOf(newData.filter(item => item.id === id)[0])
        newObject[column] = value
        newData[index] = newObject
        setData(newData)
    }

    useEffect(() => {
        fetch('/all_tables')
            .then(res => res.json())
            .then(data => {
                setAllTables(data.tables);
            });
    }, []);

    function neue_tabelle_laden(tabellenname) {
        setCurrentTable(tabellenname)
        tabelle_abrufen(tabellenname).then(res => setData(JSON.parse(res)))
    }
    /*
        function Datenbank_aktualisieren() {
            console.log(currentTable)
            console.log(JSON.stringify(data))
        }
    */
    function Datenbank_aktualisieren() {
        fetch('/update_db', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                new_table: data,
                new_table_name: currentTable,
            }),
        })
    }

    function InputText (props){
        return (
            <TableCell>
                <TextInput
                    id="text"
                    labelText=""
                    defaultValue={props.cell.value}
                    onChange={(e) => handleChange(e.target.value, Number(props.cell.id.split(":")[0]), props.column)}
                >
                </TextInput>
            </TableCell>
        )
    }

    return (
        <>
            {allTables !== null &&
                <Dropdown
                    className="all_tables_dropdown"
                    id="default"
                    label="Alle Tabellen"
                    items={allTables}
                    onChange={
                        ({ selectedItem }) => neue_tabelle_laden(selectedItem)
                    }
                />}

            <DataTable rows={rowData} headers={headerData} isSortable>
                {({ rows, headers, getHeaderProps, getTableProps }) => (
                    <TableContainer title={currentTable}>
                        <Table {...getTableProps()} useZebraStyles >
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
                                    <TableRow key={row.id}>
                                        {row.cells.map((cell) => (cell.id.includes('Wert') ?
                                            <TableCell key={cell.id}>
                                                <NumberInput
                                                    id="carbon-number"
                                                    value={cell.value}
                                                    onChange={(e) => handleChange(e.imaginaryTarget.valueAsNumber, Number(cell.id.split(":")[0]), "Wert")}
                                                />
                                            </TableCell>
                                            :
                                            cell.id.includes('Besonderheit') ?
                                                <TableCell key={cell.id}>
                                                    <TextInput
                                                        id="text"
                                                        labelText=""
                                                        defaultValue={cell.value}
                                                        onChange={(e) => handleChange(e.target.value, Number(cell.id.split(":")[0]), "Besonderheit")}
                                                    >
                                                    </TextInput>
                                                </TableCell>

                                                :
                                                cell.id.includes('Quelle') ?
                                                    //<InputText key={cell.id} cell={cell} column="Quelle"/>
                                                  
                                                    <TableCell key={cell.id}>
                                                        <TextInput
                                                            id="text"
                                                            labelText=""
                                                            defaultValue={cell.value}
                                                            onChange={(e) => handleChange(e.target.value, Number(cell.id.split(":")[0]), "Quelle")}
                                                        >
                                                        </TextInput>
                                                    </TableCell>
                                                   
                                                    :
                                                    <TableCell key={cell.id}>{cell.value}</TableCell>

                                        ))}
                                    </TableRow>
                                ))}
                            </TableBody>
                        </Table>
                    </TableContainer>
                )}
            </DataTable>
            <Button style={{ marginTop: "10px" }} onClick={() => Datenbank_aktualisieren()}>Datenbank aktualisieren</Button>
        </>
    )
}