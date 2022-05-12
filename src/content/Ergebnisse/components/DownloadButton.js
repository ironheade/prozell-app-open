import { Button } from "carbon-components-react";
import { Download32 } from '@carbon/icons-react';
import { CSVLink } from 'react-csv';


//npm install react-json-to-excel --save
export default function DownloadButton(props) {
    const description = props.name+" herunterladen"
    return (
        <>
            {props.data !== null &&
                <CSVLink
                    data={JSON.parse(props.data)}
                    filename={props.name + ".csv"}
                    enclosingCharacter={``}
                    style={{ "textDecoration": "none" }}
                //separator=","
                >
                    <Button
                        //kind="ghost"
                        kind="secondary"
                        iconDescription={description}
                        hasIconOnly
                        renderIcon={Download32}
                        size="sm"
                        style={{ margin:"4px" }}
                        tooltipAlignment="start"
                        />
             
                    {/*
                <Button 
                    kind="tertiary"
                    renderIcon={Download32} 
                    size="sm"
                    style={{ marginBottom: "10px"}}>
                        {props.name} herunterladen
                        </Button>
                        */}
                </CSVLink>
            }
        </>
    )
}