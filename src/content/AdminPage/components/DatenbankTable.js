import {
  Button,
  DataTable,
  Dropdown,
  NumberInput,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableHeader,
  TableRow,
  TextInput,
} from 'carbon-components-react';
import React, { useState } from 'react';
import tabelle_abrufen from '../../../functions/tabelle_abrufen';
import InputText from './TextInput';

export default function DatenbankTable(props) {
  //Daten der altuell ausgewählten Tabelle
  const [data, setData] = useState([{ id: 1, Beschreibung: 'keine' }]);
  //Name der aktuell ausgewählten Tabelle
  const [currentTableName, setCurrentTableName] = useState('Tabelle auswählen');
  const [currentTable, setCurrentTable] = useState('Tabelle auswählen');

  const headerData = Object.keys(data[0]).map(item => ({
    header: item,
    key: item,
  }));
  const rowData = data.map(item => ({ ...item, id: item['id'].toString() }));

  function handleChange(value, id, column) {
    var newData = [...data];
    var newObject = newData.filter(item => item.id === id)[0];
    const index = newData.indexOf(newData.filter(item => item.id === id)[0]);
    newObject[column] = value;
    newData[index] = newObject;
    setData(newData);
  }

  function neue_tabelle_laden(tabellenname) {
    const Dateiname = props.dropDownData.filter(
      item => item.Beschreibung === tabellenname
    )[0].Dateiname;
    setCurrentTableName(tabellenname);
    setCurrentTable(Dateiname);
    tabelle_abrufen(Dateiname).then(res => setData(JSON.parse(res)));
  }

  function Datenbank_aktualisieren() {
    fetch('/update_db', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        new_table: data,
        new_table_name: currentTable,
      }),
    });
  }

  const editable_columns = [
    'Besonderheit',
    'Quelle',
    'Nachname',
    'Vorname',
    'Jahr',
    'Titel',
    'Verlag',
    'doi',
    'ISBN',
    'text',
    'quelle',
  ];
  const dropdownData = props.dropDownData.map(item => item.Beschreibung);
  //console.log(dropdownData)

  return (
    <>
      <Dropdown
        className="all_tables_dropdown"
        id="default"
        label={props.title}
        //items={props.dropDownData}
        items={dropdownData}
        //items={zellformate}
        //items={allTables}
        onChange={({ selectedItem }) => neue_tabelle_laden(selectedItem)}
      />
      {
        //props.dropDownData.length === 1 &&
        //neue_tabelle_laden(props.dropDownData[0].Dateiname)
        //setCurrentTable(props.dropDownData[0].Dateiname) &&
        //setCurrentTableName(props.dropDownData[0].Dateiname) &&
        //neue_tabelle_laden(props.dropDownData[0].Dateiname
      }

      <DataTable rows={rowData} headers={headerData} isSortable>
        {({ rows, headers, getHeaderProps, getTableProps }) => (
          <TableContainer title={currentTableName}>
            <Table {...getTableProps()} useZebraStyles>
              <TableHead>
                <TableRow>
                  {headers.map(header => (
                    <TableHeader {...getHeaderProps({ header })}>
                      {header.header}
                    </TableHeader>
                  ))}
                </TableRow>
              </TableHead>
              <TableBody>
                {rows.map(row => (
                  <TableRow key={row.id}>
                    {row.cells.map(cell =>
                      cell.id.includes('Wert') ? (
                        <TableCell key={cell.id}>
                          <NumberInput
                            id="carbon-number"
                            value={cell.value}
                            onChange={e =>
                              handleChange(
                                e.imaginaryTarget.valueAsNumber,
                                Number(cell.id.split(':')[0]),
                                'Wert'
                              )
                            }
                          />
                        </TableCell>
                      ) : editable_columns.includes(cell.id.split(':')[1]) ? (
                        <InputText
                          key={cell.id}
                          cell={cell}
                          change={e =>
                            handleChange(
                              e.target.value,
                              Number(cell.id.split(':')[0]),
                              cell.id.split(':')[1]
                            )
                          }
                        />
                      ) : (
                        <TableCell key={cell.id}>{cell.value}</TableCell>
                      )
                    )}
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        )}
      </DataTable>
      <Button
        style={{ marginTop: '10px' }}
        onClick={() => Datenbank_aktualisieren()}>
        Datenbank aktualisieren
      </Button>
    </>
  );
}
