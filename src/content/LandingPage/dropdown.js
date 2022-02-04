import React, { useState } from 'react';
import { Dropdown } from 'carbon-components-react';

const items = ['1', '2', '3'];

export default function MyDropdown() {
  const [currentItem, setCurrentItem] = useState('');
  return (
    <div style={{ width: 400 }}>
      <Dropdown
        id="default"
        titleText="Dropdown label"
        helperText="This is some helper text"
        label="Dropdown menu options"
        items={items}
        //itemToString={(item) => (item ? item.text : '')}
        onChange={({ selectedItem }) => setCurrentItem(selectedItem)}
        selectedItem={currentItem}
      />
      <p>{currentItem}</p>
    </div>
  );
}
