// src/components/ButtonComponent.js
import React, { useState } from 'react';

const ButtonComponent = () => {
  // const [presetInfo, setPresetInfo] = useState('');

  const presetInfo = {
    'presetInfo' : 1
  }

  const handleButtonClick = async () => {
    const response = await fetch('http://localhost:8000/send-info', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(presetInfo),
    });

    const data = await response.json();
    console.log(data);
  };

  return (
    <div>
      <input
        type="text"
        value={presetInfo}
        onChange={(e) => setPresetInfo(e.target.value)}
      />
      <button onClick={handleButtonClick}>发送信息到后端</button>
    </div>
  );
};

export default ButtonComponent;
