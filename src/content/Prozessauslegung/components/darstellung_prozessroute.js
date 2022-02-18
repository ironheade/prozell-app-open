import React, { useState } from 'react'
import ProzessCard from './prozess_card'
import { useSelector } from 'react-redux';
import tabelle_abrufen from '../../../functions/tabelle_abrufen';

export default function DarstellungProzessroute(){

    //aktuelle Prozessroute aus dem Redux State
    const prozessRoute = useSelector(state => state.prozessRoute)
    //Alle Prozessschritte aus der DB, für den Abgleich des Materialnamens, lokaler State
    const [prozessschritte, setProzessschritte] = useState(null)
    //abrufen aller Prozessschritte aus der Datenbank, speichern in prozessschritte 
    tabelle_abrufen('prozessschritte').then(data => setProzessschritte(data))

    return(
            <div className="bx--row bx--no-gutter" style={{padding: "20px"}}>
                <ProzessCard Name="Material" Dateiname="material"/>
                {prozessschritte !== null &&
                prozessRoute.map(item_outer => 
                    item_outer[Object.keys(item_outer)[0]].map(item =>
                        <ProzessCard 
                            key={item} 
                            Name={item} 
                            Dateiname={JSON.parse(prozessschritte).filter(item_inner => item_inner.Beschreibung === item)[0].Dateiname}
                        />
                        ))}
                <ProzessCard Name="Zelle" Dateiname="zelle"/>
            </div>
    )}