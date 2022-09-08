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
        <TableCell style={{ backgroundColor: 'black' }}>
          <h4 style={{ color: 'white' }}>
            {props.filter}
          </h4>
        </TableCell>
        <TableCell style={{ backgroundColor: 'black' }}/>
        <TableCell style={{ backgroundColor: 'black' }}/>
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
                  props.onChange(item.Beschreibung, e.imaginaryTarget.valueAsNumber)
                }
              />
            </TableCell>
            <TableCell>{item.Einheit}</TableCell>
          </TableRow>
        ))}
    </TableBody>
  );
}
