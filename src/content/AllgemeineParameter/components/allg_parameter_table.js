import React from 'react';
import {
  Table,
  TableHead,
  TableRow,
  TableHeader,
  TableBody,
  TableCell,
  NumberInput,
} from 'carbon-components-react';

export default function AllgParameterTable(props) {
  return (
    <Table useZebraStyles size="compact">
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
          <TableHeader>
            <p>Besonderheit</p>
          </TableHeader>
        </TableRow>
      </TableHead>
      <TableBody>
        {props.content !== null &&
          JSON.parse(props.content).map(item => (
            <TableRow key={item.id}>
              <TableCell>{item.Beschreibung}</TableCell>
              <TableCell>
                <NumberInput
                  size="sm"
                  min={0}
                  id="carbon-number"
                  invalidText="Ungültiger Wert"
                  value={item.Wert}
                  onChange={e =>
                    props.onChange(item.Beschreibung, e.imaginaryTarget.value)
                  }
                />
              </TableCell>
              <TableCell>{item.Einheit}</TableCell>
              <TableCell>{item.Besonderheit}</TableCell>
            </TableRow>
          ))}
      </TableBody>
    </Table>
  );
}
