import React from 'react';
import {
  TableRow,
  TableCell,
  TableBody,
  NumberInput,
} from 'carbon-components-react';

export default function WeitereParameterTablerow(props) {
  return (
    <TableBody>
      <TableRow>
        <TableCell>
          <h4>
            <u>{props.filter}</u>
          </h4>
        </TableCell>
        <TableCell />
        <TableCell />
      </TableRow>
      {JSON.parse(props.Zellchemie)
        .filter(item => item.Kategorie === props.filter)
        .map(item => (
          <TableRow key={item.id}>
            <TableCell>{item.Beschreibung}</TableCell>
            <TableCell key={item.id}>
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
          </TableRow>
        ))}
    </TableBody>
  );
}
