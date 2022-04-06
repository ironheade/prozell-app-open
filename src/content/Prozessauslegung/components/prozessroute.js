import React, { useState, useEffect, useRef } from "react";
import {
    TableRow,
    TableCell,
    TableBody,
    Table,
    TableHead,
    TableHeader,
    Dropdown,
    Button,
    NumberInput,
    Accordion,
    AccordionItem,
    Tooltip
} from 'carbon-components-react';
import { useSelector, useDispatch } from "react-redux";
import {
    prozessroute_change,
    Prozessdaten_change
} from '../../../actions/index'
import { AddAlt32, SubtractAlt32 } from '@carbon/icons-react';
import tabelle_abrufen from '../../../functions/tabelle_abrufen'
import ProzessTooltip from "./ProzessTooltip";

export default function Prozessroute() {
    //Route muss in dieser Form entstehen. 
    //Die Prozessabschnitte sind ursprünglich leer, werden dann aber gefüllt 
    //mit den Prozessschritten einer vorgefertigten ProzessRoute
    //Prozessroute in der DB:
    //   id | Beschreibung | Prozessabschnitt
    //   ------------------------------------
    //    1 | Mischen      | Materialformulierung
    //   ...

    const route = [{
        "Materialformulierung": []
    }, {
        "Schichtherstellung": []
    }, {
        "Elektrodenkonditionierung": []
    }, {
        "Elektrodenkonfektionierung": []
    }, {
        "Zellassemblierung": []
    }, {
        "Elektrolytbefüllung": []
    }, {
        "Formierung": []
    }]

    const [prozessschritte, setProzessschritte] = useState(null) //hier alle Prozessschritte die möglich sind, kann hier im state bleiben
    //const [prozessRoute, setProzessRoute] = useState(route) //muss in den redux State, in der gleichen Form wie das dictionary oben
    const [prozessRouten, setProzessRouten] = useState(null) //Liste der auswählbaren Prozessrouten
    const [tempProzessroute, setTempProzessroute] = useState(null) //temporär, speichert die Infos aus dem call

    const dispatch = useDispatch()

    //aktuelle Prozessroute
    const prozessRoute = useSelector(state => state.prozessRoute)
    //Daten zur aktuellen Prozessroute
    const prozessschrittDaten = useSelector(state => state.prozessschrittDaten)

    const [tooltips, setTooltips] = useState(null)
    tabelle_abrufen('tooltips').then(data => setTooltips(data))

    //Abrufen der Tabelle einer Produktionslinie in den temporären State
    tabelle_abrufen('prozessrouten').then(data => setProzessRouten(data))
    //abrufen aller Prozessschritte aus der Datenbank, speichern in alle Prozessschritte 
    tabelle_abrufen('prozessschritte').then(data => setProzessschritte(data))

    //function importAll(r) {
    //    return r.keys().map(r);
    //  }

    //const images = importAll(require.context('../../../resources/process_icons/', false, /\.(png|jpe?g|svg)$/));


    //sobald sich die Prozessroute im temporären state ändert, wird die Prozessroute angepasst
    const didMount = useRef(false);
    useEffect(() => {
        didMount.current && tempProzessroute !== null ?
            neue_prozessroute()
            : (didMount.current = true);
    }, [tempProzessroute]);

    //sobald sich ein Material in der aktuellen Prozessroute ändert wird das nested State angepasst
    const didMount2 = useRef(false);
    useEffect(() => {
        didMount2.current ? add_prozessdaten() : (didMount2.current = true);
    }, [prozessRoute])



    //alle Prozessschritte 
    function neue_prozessroute() {
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

    //Prozessroute wird aus der Datenbank in den temporären State geladen
    function change_prozessroute(neue_prozessroute) {
        tabelle_abrufen(neue_prozessroute.Dateiname).then(data => setTempProzessroute(data))
    }

    //Prozessschritt aus Object entfernen, Object in prozessRoute einbauen an richtiger Stelle
    function delete_prozessschritt(Prozessschritt, Prozessabschnitt) {
        var newObject = { ...Prozessabschnitt }
        var newArray = [...newObject[Object.keys(newObject)[0]]]
        var index = newArray.indexOf(Prozessschritt)
        newArray.splice(index, 1)
        newObject[Object.keys(newObject)[0]] = newArray

        var newState = [...prozessRoute]

        var stateIndex = newState.findIndex(object => Object.keys(object)[0] === Object.keys(newObject)[0])
        newState[stateIndex] = newObject

        dispatch(prozessroute_change(newState))
    }
    //Prozessschritt zur Prozessroute hinzu fügen
    function add_prozessschritt(Prozessschritt, Prozessabschnitt) {
        var newState = [...prozessRoute]
        var stateIndex = newState.findIndex(object => Object.keys(object)[0] === Prozessabschnitt)
        var newObject = { ...newState[stateIndex] }
        var newArray = [...newObject[Object.keys(newObject)[0]]]

        newArray.indexOf(Prozessschritt) > -1 ||
            newArray.push(Prozessschritt)

        newObject[Object.keys(newObject)[0]] = newArray

        newState[stateIndex] = newObject

        dispatch(prozessroute_change(newState))
    }

    //function move_up(){}

    //function move_down(){}

    //füllt das nested Dict mit den Daten aus der Prozessroute
    function add_prozessdaten() {
        var newState = []
        prozessRoute.map(item => item[Object.keys(item)[0]].map(inner_item => //liste mit den Prozessschritten pro Abschnitt
            newState.push(tabelle_abrufen(JSON.parse(prozessschritte).filter(item => item.Beschreibung === inner_item)[0].Dateiname).then(result => ({
                [inner_item]: JSON.parse(result),
            }))) //jeweils die Dateinamen
        ))

        Promise.all(newState).then(values => {
            dispatch(Prozessdaten_change(values));
        });
    }

    //Anpassen einzelner Werte der verwendeten Prozessschritte im State, etwas komplizierter da der State verschachtelt ist

    function Prozessschritt_anpassen(Prozess, Beschreibung, neuerWert) {
        let newState = [...prozessschrittDaten]; //shallow copy of old state
        var prevIndex = newState.findIndex(
            item => Object.keys(item)[0] === Prozess
        ); //index im State für das zu Änderndn Object
        let newObject = { ...newState[prevIndex] }; //Kopie des Materials als Objec
        let innerIndex = newObject[Prozess].findIndex(
            item => item.Beschreibung === Beschreibung
        ); //index im neuen Objects für das zu Ändernden Wertes
        let innerObject = [...newObject[Prozess]]; //Kopie der Eigenschaften des Materials als Liste von Objects
        let innerinnerObject = { ...innerObject[innerIndex] }; //Kopie der betreffenden Spalte
        innerinnerObject.Wert = neuerWert; //Wert Überschreiben
        innerObject[innerIndex] = innerinnerObject; //Alle Spalten des Materials
        newObject[Prozess] = innerObject;
        newState[prevIndex] = newObject;
        dispatch(Prozessdaten_change(newState));
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

    return (
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
                        <TableCell style={{ backgroundColor: 'white' }} />
                        <TableCell style={{ backgroundColor: 'white' }}><h3>Aktuelle Prozessroute</h3></TableCell>
                    </TableRow></TableBody>

                    {prozessRoute.map(outer_item =>

                        <TableBody key={Object.keys(outer_item)[0]}>

                            <TableRow >
                                <TableCell style={{ backgroundColor: 'white' }}></TableCell>
                                <TableCell style={{ backgroundColor: 'black' }}><h4 style={{ color: 'white' }}>{Object.keys(outer_item)[0]}</h4></TableCell>
                            </TableRow>

                            {outer_item[Object.keys(outer_item)[0]].map(inner_item =>
                                <TableRow key={inner_item}>
                                    <TableCell style={{ textAlign: "right", backgroundColor: 'white' }}>
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
                        <TableCell style={{ backgroundColor: 'white' }} />
                        <TableCell style={{ backgroundColor: 'white' }}><h3>Alle Prozessschritte</h3></TableCell>
                    </TableRow></TableBody>

                    {prozessschritte !== null &&
                        [...new Set(JSON.parse(prozessschritte).map(item => item.Prozessabschnitt))].map(item_outer =>

                            <TableBody key={item_outer}>
                                <TableRow>
                                    <TableCell style={{ backgroundColor: 'white' }}></TableCell>
                                    <TableCell style={{ backgroundColor: 'black' }}><h4 style={{ color: 'white' }}>{item_outer}</h4></TableCell>

                                </TableRow>
                                {JSON.parse(prozessschritte).filter(item => item.Prozessabschnitt === item_outer).map(item =>
                                    <TableRow key={item.Beschreibung}>
                                        <TableCell style={{ textAlign: "right", backgroundColor: 'white' }}>
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
                                        
                                        <TableCell>
                                            {item.Beschreibung}
                                            <ProzessTooltip tooltips={tooltips} title={item.Beschreibung} quelle={item.Dateiname}/>
                                        </TableCell>
                                        
                                    </TableRow>
                                )}
                            </TableBody>

                        )}
                </Table>
            </div>

            <div className="bx--col-lg-8">
                <h3 style={{ marginLeft: "20px" }}>Details Prozessschritte</h3>
                {prozessschrittDaten !== null &&
                    <Accordion style={{ marginLeft: "20px" }}>
                        {prozessschrittDaten.map(item =>

                            <AccordionItem key={Object.keys(item)[0]} title={Object.keys(item)[0]}>

                                <Table useZebraStyles size="compact" >
                                    <TableHead>
                                        <TableRow>
                                            <TableHeader>Beschreibung</TableHeader>
                                            <TableHeader>Wert</TableHeader>
                                            <TableHeader>Einheit</TableHeader>
                                            <TableHeader>Besonderheit</TableHeader>
                                        </TableRow>
                                    </TableHead>

                                    <TableBody>
                                        {item[Object.keys(item)[0]].map(item2 =>
                                            <TableRow key={item2.Beschreibung}>
                                                <TableCell>
                                                    {item2.Beschreibung}
                                                </TableCell>
                                                <TableCell>
                                                    <NumberInput
                                                        size="sm"
                                                        min={0}
                                                        id="carbon-number"
                                                        invalidText="Ungültiger Wert"
                                                        value={item2.Wert}
                                                        onChange={e => Prozessschritt_anpassen(Object.keys(item)[0], item2.Beschreibung, e.imaginaryTarget.valueAsNumber)}
                                                    />
                                                </TableCell>
                                                <TableCell>
                                                    {item2.Einheit}
                                                </TableCell>
                                                <TableCell>
                                                    {item2.Besonderheit}
                                                </TableCell>
                                            </TableRow>
                                        )}
                                    </TableBody>
                                </Table>
                            </AccordionItem>

                        )}
                    </Accordion>}

            </div>

        </div>
    )
}


