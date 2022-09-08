import React from "react";
import DownloadButton from "./DownloadButton";

export default function SimpleTableProzessroute(props){
    const newData = []
    props.data.map(item => newData.push(item[Object.keys(item)[0]]))
    return(
        <>
        <div style={{
            display:"flex", 
        flexDirection:"row",
        //alignItems:"center"
        }}>
        <h3>Prozessroute</h3>
        <DownloadButton name="Prozessroute" data={JSON.stringify(newData)}/>
        </div>
        {props.data.map((item,index) =>
        <div key={index}>
            <p>{Object.keys(item)[0]}</p>
            <ul>
                {item[Object.keys(item)[0]].map((listItem,index) => 
                <li key={index} style={{paddingLeft:"20px"}}>{listItem}</li>
                    )}
            </ul>
        </div>
            
            )}
        </>
    )
}