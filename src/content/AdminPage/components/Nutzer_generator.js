import { Button, DatePicker, DatePickerInput,  NumberInput, TextInput } from "carbon-components-react";
import React, { useState, useRef, useEffect } from "react";
import { CSVLink } from 'react-csv';
import { Download32 } from '@carbon/icons-react';
import tabelle_abrufen from "../../../functions/tabelle_abrufen";
import NutzerTable from "./NutzerTable";

export default function NutzerGenerator() {

    const [date, setDate] = useState(null)
    const [anzahlNutzer, setAnzahlNutzer] = useState(0)
    const [newUsers, setNewUsers] = useState("Nutzer generieren")
    const [commentUsers, setCommentUsers] = useState("")
    const downloadButton = useRef(null)
    const [allUsers, setAllUsers] = useState(null)

    useEffect(()=>{
        fetch('/Nutzer_abrufen', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                Zugangsdaten: "Zugangsdaten",
            }),
        }).then(res => res.json()).then(res => setAllUsers(res))
    },[newUsers])

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
                Kommentar: commentUsers
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

    useEffect(()=>{
        downloadButton.current.click()
    },[newUsers])

    return (
        <div style={{marginTop:"20px"}}>
        <div style={{border:"2px solid black", maxWidth:"400px", padding:"30px", marginRight:"50px", float:"left"}}>
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
            
            <TextInput
                style={{width:"220px"}}
                size="sm"
                id="carbon-text"
                labelText="Kommentar zum Nutzer"
                placeholder="z.B. TUM durch ArK"
                value={commentUsers}
                onChange={(e)=>setCommentUsers(e.target.value)}
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
                    ref = {downloadButton}
                    kind="secondary"
                    disabled={date !== null && anzahlNutzer !== 0 ? false : true}
                    iconDescription="Nutzer herunterladen"
                    hasIconOnly
                    renderIcon={Download32}
                    size="sm"
                    style={{ margin: "4px",marginTop:"20px", display:"none" }}
                    tooltipAlignment="start"
                />

            </CSVLink>


            {/*date !== null && Date.now() > date.startzeitMS && Date.now() < date.endzeitMS && <p>Login Erfolgreich!</p>*/}
        </div>
        {allUsers !== null &&
        <NutzerTable data={allUsers}/>
        }
        </div>
    )
}