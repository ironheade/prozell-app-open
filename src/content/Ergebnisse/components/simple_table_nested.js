import React from "react";
import SimpleTable from "./simple_table";

export default function SimpleTableNested(props) {

    return (

        <>
            {props.data.map((item, index) =>
                <div key={index}>
                    <h4>{Object.keys(item)[0]}</h4>
                    <SimpleTable data={JSON.stringify(item[Object.keys(item)[0]])} />
                </div>
            )
            }

        </>



    )
}