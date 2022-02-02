/*
import * as React from "react";
import {
  List,
  arrayMove,
  arrayRemove
} from "baseui/dnd-list";

export default function MyList() {
  const [items, setItems] = React.useState([
    "Item 1",
    "Item 2",
    "Item 3"
  ]);
  return (
    <List
      items={items}
      removable
      onChange={({ oldIndex, newIndex }) =>
        setItems(
          newIndex === -1
            ? arrayRemove(items, oldIndex)
            : arrayMove(items, oldIndex, newIndex)
        )
      }
      removableByMove
    />
  );
}
*/

/*

import React, {useState} from 'react'
import DnDList from "react-dnd-list";

export default function MyList() {

    
    const Item = props => {
        const dnd = props.dnd
      
        return (
          <li
           // style={{ ...dnd.item.styles, ...dnd.handler.styles, color: "red", fontSize:'22px' }}
            style={{ ...dnd.item.styles, ...dnd.handler.styles, fontSize:'22px', border:'2px solid black', padding:'5px', borderRadius:'2px', margin:'5px' }}
            className={dnd.item.classes}
            ref={dnd.item.ref}
            {...dnd.handler.listeners}
          >
            {props.item}
          </li>
        )
      }
    const [list, setList] = useState(['11111111', '2', '3'])
    return (
        <div>
     <ul onChange={console.log(list)}>
        <DnDList
          items={list}
          itemComponent={Item}
          setList={setList}
          //onChange={console.log(list)}
        />
      </ul>
      <button onClick={()=>setList([...list, "1"])}>Dont click me</button>
      <button onClick={console.log(list)}>Click me</button>
      </div>
    )
  }
  
  

*/
import React, { useState } from 'react';
import DnDList from 'react-dnd-list';

export default function MyList() {
  const Item = props => {
    const dnd = props.dnd;

    return (
      <li
        // style={{ ...dnd.item.styles, ...dnd.handler.styles, color: "red", fontSize:'22px' }}
        style={{
          ...dnd.item.styles,
          ...dnd.handler.styles,
          fontSize: '22px',
          border: '2px solid black',
          padding: '5px',
          borderRadius: '2px',
        }}
        className={dnd.item.classes}
        ref={dnd.item.ref}
        {...dnd.handler.listeners}>
        {props.item}
      </li>
    );
  };

  const [list, setList] = useState(['1', '2', '3', '4', '5', '6', '7']);

  return (
    <div>
      <ul onChange={console.log(list)}>
        <DnDList
          items={list}
          itemComponent={Item}
          setList={setList}
          //onChange={console.log(list)}
        />
      </ul>
      <button onClick={() => setList([...list, '1'])}>Dont click me</button>
      <button onClick={console.log(list)}>Click me</button>
    </div>
  );
}
