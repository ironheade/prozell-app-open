import React, {useState, useEffect, useRef} from "react";
import {
    TableRow,
    TableCell,
    TableBody,
    Table,
    TableHead,
    TableHeader,
    Dropdown,
    Button
  } from 'carbon-components-react';
  import { useSelector, useDispatch } from "react-redux";
  import { prozessroute_change } from '../../../actions/index' 
  import { AddAlt32, SubtractAlt32 } from '@carbon/icons-react';

export default function Prozessroute(){
    //Route muss in dieser Form entstehen. 
    //Die Prozessabschnitte sind ursprünglich leer, werden dann aber gefüllt 
    //mit den Prozessschritten einer vorgefertigten ProzessRoute
    //Prozessroute in der DB:
    //   id | Beschreibung | Prozessabschnitt
    //   ------------------------------------
    //    1 | Mischen      | Materialformulierung
    //   ...

    const route = [{
        "Materialformulierung":[]
    },{
        "Schichtherstellung": []
    },{
        "Elektrodenkonditionierung": []
    },{
        "Elektrodenkonfektionierung": []
    },{
        "Zellassemblierung": []
    },{
        "Elektrolytbefüllung": []
    },{    
        "Formierung": []
    }]
    
    const [prozessschritte, setProzessschritte] = useState(null) //hier alle Prozessschritte die möglich sind, kann hier im state bleiben
    //const [prozessRoute, setProzessRoute] = useState(route) //muss in den redux State, in der gleichen Form wie das dictionary oben
    const [prozessRouten, setProzessRouten] = useState(null) //Liste der auswählbaren Prozessrouten
    const [tempProzessroute, setTempProzessroute] = useState(null) //temporär, speichert die Infos aus dem call
    
    const dispatch = useDispatch()

    const prozessRoute = useSelector(state => state.prozessRoute)

    //Abrufen der Tabelle einer Produktionslinie in den temporären State
    tabelle_abrufen('prozessrouten').then(data => setProzessRouten(data))
    //abrufen aller Prozessschritte aus der Datenbank, speichern in alle Prozessschritte 
    tabelle_abrufen('prozessschritte').then(data => setProzessschritte(data))

    
    //sobald sich die Prozessroute im temporären state ändert, wird die Prozessroute angepasst
    const didMount = useRef(false);
    useEffect(() => {
      didMount.current && tempProzessroute !== null ? 
      neue_prozessroute() 
      :(didMount.current = true);
    }, [tempProzessroute]);
    

    //alle Prozessschritte 
    function neue_prozessroute(){
        var newRoute = [...route] //Kopie der leeren Prozessroute
        newRoute.map(outer_item => //Leere Prozessroute (die Prozessabschnitte) durchgehen
            JSON.parse(tempProzessroute).map(inner_item => //neue Prozessroute durchgehen
                Object.keys(outer_item)[0] === inner_item.Prozessabschnitt && 
                outer_item[Object.keys(outer_item)[0]].push(inner_item.Beschreibung)
                )
            )
            dispatch(prozessroute_change(newRoute))
            setTempProzessroute(null)
    }  

    async function tabelle_abrufen(tabelle_dateiname) {
        const res = await fetch('/tabelle_abrufen', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            tabelle: tabelle_dateiname,
          }),
        });
        const data = await res.json();
        return data.tabelle;
      }
    
    //Prozessroute wird aus der Datenbank in den temporären State geladen
    function change_prozessroute(neue_prozessroute){
        tabelle_abrufen(neue_prozessroute.Dateiname).then(data => setTempProzessroute(data))
    }

    //Prozessschritt aus Object entfernen, Object in prozessRoute einbauen an richtiger Stelle
    function delete_prozessschritt(Prozessschritt, Prozessabschnitt){
        var newObject = {...Prozessabschnitt}
        var newArray = [...newObject[Object.keys(newObject)[0]]]
        var index = newArray.indexOf(Prozessschritt)
        newArray.splice(index, 1)
        newObject[Object.keys(newObject)[0]] = newArray

        var newState = [...prozessRoute]

        newState.map(item => console.log(item))
        var stateIndex = newState.findIndex(object => Object.keys(object)[0] === Object.keys(newObject)[0]) 
        newState[stateIndex] = newObject

        dispatch(prozessroute_change(newState))
    }
    //Prozessschritt zur Prozessroute hinzu fügen
    function add_prozessschritt(Prozessschritt, Prozessabschnitt){
        var newState = [...prozessRoute]
        var stateIndex = newState.findIndex(object => Object.keys(object)[0] === Prozessabschnitt) 
        var newObject = {...newState[stateIndex]}
        var newArray =  [...newObject[Object.keys(newObject)[0]]]

        {newArray.indexOf(Prozessschritt) > -1 ||
        newArray.push(Prozessschritt)}

        newObject[Object.keys(newObject)[0]] = newArray

        newState[stateIndex] = newObject
        
        dispatch(prozessroute_change(newState))
    }

    function move_up(){

    }

    function move_down(){

    }

    /* Funktion zum Ändern der position im Array
    function array_move(arr, old_index, new_index) {
    if (new_index >= arr.length) {
        var k = new_index - arr.length + 1;
        while (k--) {
            arr.push(undefined);
        }
    }
    arr.splice(new_index, 0, arr.splice(old_index, 1)[0]);
    console.log(arr); // for testing
};
    */

    return(
        <div className="bx--row bx--no-gutter">
            <div className="bx--col-lg-4">
                    {prozessRouten !== null && (
                    <Dropdown
                    id="Prozessrouten_dropdown"
                    //type="inline"
                    size="sm"
                    label="Prozessrouten"
                    items={JSON.parse(prozessRouten)}
                    itemToString={(item) => (item ? item.Beschreibung : '')}
                    onChange={event => change_prozessroute(event.selectedItem)}
                    />
                )}

                <Table useZebraStyles size="compact">
                    <TableBody><TableRow>
                    <TableCell style={{ backgroundColor: 'white' }}/>
                    <TableCell style={{ backgroundColor: 'white' }}><h3>Aktuelle Prozessroute</h3></TableCell>
                    </TableRow></TableBody>

                {prozessRoute.map(outer_item => 
                    
                        <TableBody>

                            <TableRow>
                                <TableCell style={{ backgroundColor: 'white' }}></TableCell>
                                <TableCell style={{ backgroundColor: 'black' }}><h4 style={{ color: 'white' }}>{Object.keys(outer_item)[0]}</h4></TableCell>
                            </TableRow>

                            {outer_item[Object.keys(outer_item)[0]].map(inner_item =>
                            <TableRow>
                                <TableCell style={{ textAlign:"right", backgroundColor: 'white'}}>
                                <Button
                                    size="sm"
                                    renderIcon={SubtractAlt32}
                                    hasIconOnly
                                    kind="danger--tertiary"
                                    iconDescription="Prozess entfernen"
                                    onClick={() => delete_prozessschritt(inner_item, outer_item)}
                                    />
                                </TableCell>
                                <TableCell>{inner_item}</TableCell>
                            </TableRow>
                                )}
                        </TableBody>                    
                        )}
                        </Table>
            </div>


            <div className="bx--col-lg-4">

                <Table useZebraStyles size="compact">
                    <TableBody><TableRow>
                    <TableCell style={{ backgroundColor: 'white' }}/>
                    <TableCell style={{ backgroundColor: 'white' }}><h3>Alle Prozessschritte</h3></TableCell>
                    </TableRow></TableBody>
                    
                    {prozessschritte !== null &&
                    [...new Set(JSON.parse(prozessschritte).map(item => item.Prozessabschnitt))].map(item_outer =>

                        <TableBody>
                        <TableRow>
                            <TableCell style={{ backgroundColor: 'white' }}></TableCell>
                            <TableCell style={{ backgroundColor: 'black' }}><h4 style={{ color: 'white' }}>{item_outer}</h4></TableCell>

                        </TableRow>
                        {JSON.parse(prozessschritte).filter(item => item.Prozessabschnitt === item_outer).map(item => 
                            <TableRow>
                                <TableCell style={{ textAlign:"right", backgroundColor: 'white' }}>
                                <Button
                                    size="sm"
                                    renderIcon={AddAlt32}
                                    hasIconOnly
                                    kind="tertiary"
                                    iconDescription="Prozess hinzufügen"
                                    key={item.id}
                                    onClick={() => add_prozessschritt(item.Beschreibung, item_outer)}
                                    />
                                </TableCell>
                                <TableCell>{item.Beschreibung}</TableCell>
                            </TableRow>
                            )}
                        </TableBody>


                    )}
                    </Table>
            </div>

        </div>
    )
}


