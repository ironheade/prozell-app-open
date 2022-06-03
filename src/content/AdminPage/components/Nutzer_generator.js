import { Button, DatePicker, DatePickerInput,  NumberInput } from "carbon-components-react";
import React, { useState } from "react";
import { CSVLink } from 'react-csv';
import { Download32 } from '@carbon/icons-react';

export default function NutzerGenerator() {

    const [date, setDate] = useState(null)
    const [anzahlNutzer, setAnzahlNutzer] = useState(0)
    const [newUsers, setNewUsers] = useState("Nutzer generieren")


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

    return (
        <div style={{border:"2px solid black", maxWidth:"400px", padding:"30px", marginTop:"20px"}}>
            <h3>Neue Nutzer hinzufügen</h3>
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
                style={{marginTop:"20px"}}
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
                    style={{ margin: "4px",marginTop:"20px" }}
                    tooltipAlignment="start"
                />

            </CSVLink>

            {/*date !== null && Date.now() > date.startzeitMS && Date.now() < date.endzeitMS && <p>Login Erfolgreich!</p>*/}
        </div>
    )
}