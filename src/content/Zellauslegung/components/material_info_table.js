import React from 'react';
import {
  TableRow,
  Table,
  TableHead,
  TableHeader,
  TableBody,
  TableCell,
  NumberInput,
} from 'carbon-components-react';

export default function MaterialInfoTable(props) {
  return (
    <div>
      <h4>{props.header}</h4>
      <Table useZebraStyles size="compact" className="zellchemie_table">
        <TableHead>
          <TableRow>
            <TableHeader>
              <p>Beschreibung</p>
            </TableHeader>
            <TableHeader>
              <p>Wert</p>
            </TableHeader>
            <TableHeader>
              <p>Einheit</p>
            </TableHeader>
          </TableRow>
        </TableHead>

        <TableBody>
          {props.content.map(item => (
            <TableRow key={item.id}>
              <TableCell>{item.Beschreibung}</TableCell>
              <TableCell key={item.id}>
                <NumberInput
                  size="sm"
                  id="carbon-number"
                  value={item.Wert}
                  onChange={e =>
                    props.onChange(
                      props.header,
                      item.Beschreibung,
                      e.imaginaryTarget.value
                    )
                  }
                  invalidText="Ungültiger Wert"
                />

                {/*
                            <input
                                key={item.id}
                                value={item.Wert}
                                onChange={(e) => props.onChange(props.header, item.Beschreibung, e.target.value)}
                                id={item.id}
                                />
                            */}
              </TableCell>
              <TableCell>{item.Einheit}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
}
