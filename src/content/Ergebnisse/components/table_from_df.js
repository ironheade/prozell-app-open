import React from "react";
import {
    TableRow,
    TableCell,
    TableBody,
    Table,
    TableHead,
    TableHeader
  } from 'carbon-components-react';

export default function DfTable(props){
    
    const data = JSON.parse(props.data)

    function getKeys(){
        return Object.keys(data[0])
      }
      
    function getHeader(){
    var keys = getKeys();
    return keys.map((key, index)=>{
        return <TableHeader key={index}>{key.toUpperCase()}</TableHeader>
    })
    }
    
    function getRowsData(){
    var items = data;
    var keys = getKeys();
    return items.map((row, index)=>{
        return <TableRow key={index}><RenderRow key={index} data={row} keys={keys}/></TableRow>
    })
    }

    const RenderRow = (props) =>{
        return props.keys.map((key, index)=>{
          var style={backgroundColor:"#e0e0e0", fontWeight:"bold"}
          return <TableCell style={index === 0 ? style:{}} key={index}>
              {typeof props.data[key] !== 'string' ?
              Math.round(props.data[key]*100)/100
              :
              props.data[key]
                }
              </TableCell>
        })
      }

    return(
      <>
        <Table useZebraStyles size="compact">
            <TableHead>
                <TableRow>{getHeader()}</TableRow>
            </TableHead>
            <TableBody>
                {getRowsData()}
            </TableBody>
        </Table>

      </>
    )
}