import React from "react";

export default function SimpleTable(props){
    const headers = Object.keys(JSON.parse(props.data)[0])

    return(

        <>
        <table>
        {/*<table id="simpleTable"> */}
            <tbody>
                <tr>
                  {headers.map((item, index) => item !== "id" &&
                    <th key={index} style={{fontWeight: 'bold', padding: '2px'}}>{item}</th>)}  
                </tr>
                {JSON.parse(props.data).map((row, index) =>
                    <tr key={index}>
                        {headers.map((item, index) => item !== "id" &&
                        <td key={index} style={{padding: '2px'}}>{row[item]}</td>
                        )}
                    </tr>
                    )}
            </tbody>
        </table>
</>
    )
}