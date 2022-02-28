import React from 'react'

export default function ProzessCard(props){
    return(
        <div id="Prozess_Card_aussen">
            <div className='box'>
                <img src={'/icons/process_icons/'+props.Dateiname+'.png'} className="Prozess_Card_img" alt={props.Name}/>
            </div>
            {props.Name === "Material" || props.Name === "Zelle" ?
            <div className="Prozess_Card_innen_Anfang_Ende box">
                <h3>{props.Name}
                </h3>
            </div>
            :
            <div className="Prozess_Card_innen box">
                <p>{props.Name}
                </p>
            </div>
            }
        </div>
    )
}