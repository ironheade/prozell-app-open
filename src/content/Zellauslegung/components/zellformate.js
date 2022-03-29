import React, { useState } from 'react';
import { Dropdown } from 'carbon-components-react';
import { useSelector, useDispatch } from 'react-redux';
import {
  zellformat_change,
  zellformat_name_state,
  GWh_Jahr_Ah_Zelle_change,
} from '../../../actions/index';
import {
  Table,
  TableHead,
  TableRow,
  TableHeader,
  TableBody,
  TableCell,
  NumberInput,
} from 'carbon-components-react';
//import './../_zellauslegung.scss'

export default function Zellformate() {
  const dispatch = useDispatch();
  //Infos zur aktuell ausgewählten Zelle (Maße, etc.)
  const zellformat = useSelector(state => state.zellformat);
  //Object der gerade ausgewählten Zelle (id, Name, Dateiname, Zelltyp)
  const zellformatName = useSelector(state => state.zellformatName);
  //alle Zellformate
  const currentCells = useSelector(state => state.alleZellen);
  //Ah pro Zelle und GWh/Jahr für die Fabrik separat gespeichert
  const GWH_Jahr_AH_Zelle = useSelector(state => state.GWH_Jahr_AH_Zelle);

  //Liste aller Möglichen Zellformate
  const [currentZellformate, setCurrentZellformate] = useState('Pouchzelle');

  /*
  //Wichtige Funktion! Die Funtkion arbeitet immer dann wenn Zellinfo sich ändert -> kann doppelten API Abruf durchführen
  //Funktion wird immer dann durchgeführt wenn such {Zellinfo} ändert (ausser beim ersten mal, dafür ist didMount da)
  //wenn Zellinfo = null muss auch didMount = false, verhindert das initiale rendern 
  const didMount = useRef(false);
  useEffect(() => {
    didMount.current ?
      (JSON.parse(Zellinfo).map(item=> console.log(item)))
    :
      didMount.current = true;
    
  }, [Zellinfo]);
  function setMountFalse(){
    didMount.current = false;
  }
*/

  //ruft nach Auswahl der Zelle die Informationen zur Zelle aus der Datenbank ab
  const Zell_handler = event => {
    const value = event.target.value;
    console.log(zellformatName);
    console.log({
      ...JSON.parse(currentCells).filter(item => item.Dateiname === value)[0],
    });
    //dispatch(zellformat_change(value))
    dispatch(
      zellformat_name_state({
        ...JSON.parse(currentCells).filter(item => item.Dateiname === value)[0],
      })
    );

    fetch('/Zellwahl', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        Zelle: value,
      }),
    })
      .then(res => res.json())
      .then(data =>
        //setZellinfo(data.Zellinfo)
        dispatch(zellformat_change(data.Zellinfo))
      );
  };

  function setGWh_pro_jahr(newValue) {
    var newState = { ...GWH_Jahr_AH_Zelle };
    newState['GWh_pro_jahr'] = newValue;
    dispatch(GWh_Jahr_Ah_Zelle_change(newState));
  }

  function setAh_pro_Zelle(newValue) {
    var newState = { ...GWH_Jahr_AH_Zelle };
    newState['Ah_pro_Zelle'] = newValue;
    dispatch(GWh_Jahr_Ah_Zelle_change(newState));
  }

  //aktualisiert den state zur aktuell ausgewählten Zelle
  function handleChange(Beschreibung, neuerWert) {
    const newArr = JSON.parse(zellformat).map(item => {
      if (item.Beschreibung === Beschreibung) {
        return { ...item, Wert: neuerWert };
      }
      return item;
    });
    dispatch(zellformat_change(JSON.stringify(newArr)));
  }



  return (
    <div>
      {currentCells !== null && (
        <div>
          <div style={{ width: 400 }}>
            <Dropdown
              className="zellformate__dropdown"
              id="default"
              //  titleText="Zelltypen"
              helperText="This is some helper text"
              label="Dropdown menu options"
              items={[
                ...new Set(
                  JSON.parse(currentCells).map(item => item.Zellformat)
                ),
              ]}
              onChange={
                ({ selectedItem }) =>
                  setCurrentZellformate(selectedItem) &
                  dispatch(zellformat_change(null)) &
                  dispatch(zellformat_name_state(null))
                //& setMountFalse()
              }
              selectedItem={currentZellformate}
            />
          </div>

          <div className="zellformate__radiobuttons" onChange={Zell_handler}>
            {JSON.parse(currentCells).map(
              item =>
                item.Zellformat === currentZellformate && (
                  <div key={item.id}>
                    <input
                      type="radio"
                      value={item.Dateiname}
                      name="Zellformat"
                      defaultChecked={
                        zellformatName !== null &&
                        item.Beschreibung === zellformatName.Beschreibung
                      }
                    />
                    <span>{item.Beschreibung}</span>
                  </div>
                )
            )}
          </div>

          {zellformat !== null && (
            <div>
              <h3>{zellformatName.Beschreibung}</h3>

              <NumberInput
                size="sm"
                id="carbon-number"
                invalidText="Ungültiger Wert"
                helperText="GWh/Jahr"
                value={GWH_Jahr_AH_Zelle['GWh_pro_jahr']}
                onChange={e => 
                  !isNaN(e.imaginaryTarget.valueAsNumber) &&
                  setGWh_pro_jahr(e.imaginaryTarget.valueAsNumber)
                }
              />
              {zellformatName.Zellformat === 'Pouchzelle' && 
                <NumberInput
                  size="sm"
                  id="carbon-number"
                  invalidText="Ungültiger Wert"
                  helperText="Ah/Zelle"
                  value={GWH_Jahr_AH_Zelle['Ah_pro_Zelle']}
                  onChange={e =>
                    !isNaN(e.imaginaryTarget.valueAsNumber) &&
                    setAh_pro_Zelle(e.imaginaryTarget.valueAsNumber)
                  }
                />
              }
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
                  </TableRow>
                </TableHead>
                <TableBody>
                  {JSON.parse(zellformat).map(item => (
                    //item.Wert == null ? (
                    //  <TableRow key={item.id} hidden />
                    //) : (
                    <TableRow key={item.id}>
                      <TableCell>{item.Beschreibung}</TableCell>
                      <TableCell key={item.id}>
                        <NumberInput
                          size="sm"
                          id="carbon-number"
                          invalidText="Ungültiger Wert"
                          value={item.Wert === null ? '' : item.Wert}
                          onChange={e =>
                            handleChange(
                              item.Beschreibung,
                              e.imaginaryTarget.valueAsNumber
                            )
                          }
                        />
                      </TableCell>
                      <TableCell>{item.Einheit}</TableCell>
                    </TableRow>
                  ))
                  //)
                  }
                </TableBody>
              </Table>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
