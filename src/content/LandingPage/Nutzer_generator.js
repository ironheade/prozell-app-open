import { Button, DatePicker, DatePickerInput, FormGroup, NumberInput, TextInput } from "carbon-components-react";
import React, { useState, useEffect } from "react";
import { CSVLink } from 'react-csv';
import { Download32 } from '@carbon/icons-react';
import { timeDays } from "d3";

export default function NutzerGenerator() {

    const [date, setDate] = useState(null)
    const [anzahlNutzer, setAnzahlNutzer] = useState(0)
    const [newUsers, setNewUsers] = useState("Nutzer generieren")

    const [nutzername, setNutzername] = useState(null)
    const [passwort, setPasswort] = useState(null)

    const [nutzerdaten, setNutzerdaten] = useState(null)

    async function nutzer_generieren(Anzahl, Startzeit, Endzeit, StartzeitMS, EndzeitMS) {
        const res = await fetch('/nutzer_generieren', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                Anzahl: Anzahl,
                Startzeit: Startzeit,
                Endzeit: Endzeit,
                StartzeitMS: StartzeitMS,
                EndzeitMS: EndzeitMS,
            }),
        });
        const data = await res.json();
        setNewUsers(data);

    }

    function handleDate(date) {
        date.length === 2 &&
            setDate({
                startzeit: date[0].toLocaleString(),
                startzeitMS: date[0].valueOf(),
                endzeit: date[1].toLocaleString(),
                endzeitMS: date[1].valueOf()
            })
    }

    async function CheckLog() {
        const res = await fetch('/user_check', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                Nutzer: nutzername,
                Passwort: passwort
            }),
        });
        const data = await res.json();
        return data;
    }

    function Login() {
        CheckLog().then(result => setNutzerdaten(result))
    }


    return (
        <>
            <h3>Neue Nutzer hinzufügen</h3>
            {nutzerdaten !== null && <p>{JSON.stringify(nutzerdaten)}</p>}
            <DatePicker dateFormat="d.m.Y"
                onChange={(event) => handleDate(event)}
                datePickerType="range">
                <DatePickerInput
                    id="date-picker-range-start"
                    placeholder="dd/mm/yyyy"
                    labelText="Startdatum"
                    type="text"
                />
                <DatePickerInput
                    id="date-picker-range-end"
                    placeholder="dd/mm/yyyy"
                    labelText="Enddatum"
                    type="text"
                />
            </DatePicker>
            <NumberInput
                size="sm"
                id="carbon-number"
                invalidText="Ungültiger Wert"
                label="Anzahl neuer Nutzer"
                value={anzahlNutzer}
                onChange={e =>
                    !isNaN(e.imaginaryTarget.valueAsNumber) ?
                        setAnzahlNutzer(e.imaginaryTarget.valueAsNumber) :
                        setAnzahlNutzer(0)
                }
            />

            <Button
                disabled={date !== null && anzahlNutzer !== 0 ? false : true}
                onClick={() => nutzer_generieren(anzahlNutzer, date.startzeit, date.endzeit, date.startzeitMS, date.endzeitMS)}

            >Nutzer generieren
            </Button>
            <CSVLink
                data={newUsers === null ? "Nutzer generieren" : newUsers}
                //asyncOnClick={true}
                //onClick={() => nutzer_generieren(anzahlNutzer, date.startzeit, date.endzeit, date.startzeitMS, date.endzeitMS)}
                filename={"logins.csv"}
                enclosingCharacter={``}
                separator="    "
            >
                <Button
                    kind="secondary"
                    disabled={date !== null && anzahlNutzer !== 0 ? false : true}
                    iconDescription="Nutzer herunterladen"
                    hasIconOnly
                    renderIcon={Download32}
                    size="sm"
                    style={{ margin: "4px" }}
                    tooltipAlignment="start"
                />

            </CSVLink>

            {date !== null && Date.now() > date.startzeitMS && Date.now() < date.endzeitMS && <p>Login Erfolgreich!</p>}


            <FormGroup
                legendText="Login"
                style={{
                    maxWidth: '400px'
                }}
            >

                <TextInput
                    id="one"
                    labelText="Nutzername"
                    value={nutzername !== null ? nutzername : ""}
                    onChange={(event) => setNutzername(event.target.value)}
                />
                <TextInput
                    id="two"
                    labelText="Passwort"
                    value={passwort !== null ? passwort : ""}
                    onChange={(event) => setPasswort(event.target.value)}

                />

                <Button onClick={() => Login()}>
                    Login
                </Button>

                {nutzerdaten !== null &&
                    <ul>
                        <li>{nutzerdaten.Startzeit}</li>
                        <li>{nutzerdaten.Endzeit}</li>
                        
                        {nutzerdaten.StartzeitMS-Date.now() <0 && nutzerdaten.EndzeitMS+86400000-Date.now() >0 &&<li>User logged in</li>}


                    </ul>}

            </FormGroup>

        </>
    )
}