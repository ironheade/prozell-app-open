import { TableCell, TextInput } from "carbon-components-react";
import React from "react";

export default function InputText (props){
    return (
        <TableCell key={props.cell.id}>
            <TextInput
                id="text"
                labelText=""
                defaultValue={props.cell.value}
                onChange={props.change}
            >
            </TextInput>
        </TableCell>
    )
}