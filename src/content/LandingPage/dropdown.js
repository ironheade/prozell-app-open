import React, { useState } from 'react';
import { Dropdown } from 'carbon-components-react';

const items = ['1', '2', '3'];

const items2 = [
  { id: 'option-0', text: 'Option 0' },
  { id: 'option-1', text: 'Option 1' },
  { id: 'option-2', text: 'Option 2' },
];

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
