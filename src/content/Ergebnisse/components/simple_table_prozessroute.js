import React from "react";

export default function SimpleTableProzessroute(props){
    return(
        <>
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