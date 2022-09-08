import React from 'react';
import {
  TableRow,
  TableCell,
  TableBody,
  Dropdown,
  Button,
  NumberInput,
} from 'carbon-components-react';
import { SubtractAlt32 } from '@carbon/icons-react';

export default function ZellchemieTableRow(props) {
  var listOfUsedMaterials = JSON.parse(props.Zellchemie)
    .filter(item => item.Kategorie === props.filter)
    .map(item => item.Beschreibung); //Auflistung aller genutzten Materialien einer Kategorie, für die Filterung später
  var items = JSON.parse(props.materialien) //alle Materialien
    .filter(item => item.Kategorie === props.filter) //alle Materialien der passenden Kategorie
    .filter(item =>
      listOfUsedMaterials.includes(item.Beschreibung) ? false : true
    ) //Herausfiltern aller bereits genutzten Materialien, siehe oben
    .map(item => item.Beschreibung);
  //  items.length == 0 ? console.log("empty"): console.log("not empty")
  //items.length === 0 ? (items = []) : (items = items);
  items.length === 0 && (items = []);

  return (
    <TableBody>
      <TableRow>
        <TableCell style={{ backgroundColor: 'white' }} />
        <TableCell style={{ backgroundColor: 'black' }}>
          <h4 style={{color:"white"}}>
            {props.filter}
          </h4>
        </TableCell>
        <TableCell style={{ backgroundColor: 'black' }}/>
        <TableCell style={{ backgroundColor: 'black' }}>
          {items.length !== 0 && (
            <Dropdown
              id={props.filter}
              //type="inline"
              size="sm"
              label="weitere Materialien"
              items={items}
              onChange={event => props.onChange(event.selectedItem)}
            />
          )}
        </TableCell>
      </TableRow>
      {JSON.parse(props.Zellchemie)
        .filter(item => item.Kategorie === props.filter)
        .map(item => (
          <TableRow key={item.id}>
            <TableCell style={{ textAlign:"right", backgroundColor: 'white', minHeight: "200px" }}>
              {props.unique === false && (
                <Button
                  size="sm"
                  renderIcon={SubtractAlt32}
                  hasIconOnly
                  kind="danger--tertiary"
                  iconDescription="Material entfernen"
                  key={item.id}
                  onClick={() => props.onClick(item.Beschreibung)}
                />
              )}
            </TableCell>
            <TableCell>{item.Beschreibung}</TableCell>

            <TableCell key={item.id}>
              {props.Anteil === true && (
                <NumberInput
                  size="sm"
                  id="carbon-number"
                  min={0}
                  max={100}
                  value={item.Wert == null ? 0 : item.Wert}
                  onChange={e =>
                    props.onIncrement(
                      item.Beschreibung,
                      e.imaginaryTarget.valueAsNumber 
                    )
                  }
                  invalidText="Ungültiger Wert"
                />
              )}
            </TableCell>
            <TableCell />
          </TableRow>
        ))}
    </TableBody>
  );
}
