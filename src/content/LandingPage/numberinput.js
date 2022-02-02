import React, { useState } from 'react';
import { NumberInput } from 'carbon-components-react';

export default function MyNumberInput() {
  const [currentNumber, setCurrentNumber] = useState(0);

  return (
    <div style={{ width: 400 }}>
      <NumberInput
        size="sm"
        id="carbon-number"
        min={0}
        max={100}
        value={currentNumber}
        onChange={e => setCurrentNumber(e.imaginaryTarget.value)}
        label="NumberInput label"
        helperText="Optional helper text."
        invalidText="Number is not valid"
      />
      <p>{currentNumber}</p>
    </div>
  );
}
