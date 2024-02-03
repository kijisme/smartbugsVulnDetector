import React, { useState } from 'react';
import { Button} from 'antd';

import Motal from './compoments/Motal'

const App = () => {

  const [isPopupOpen, setPopupOpen] = useState(false);

  // 点击事件处理程序，用于切换弹窗的显示状态
  const handleButtonClick = () => {
    setPopupOpen(true);
  };

  return (
      <div>
          <Button type="primary" onClick={handleButtonClick}>点我：登录/注册</Button>
          {isPopupOpen && (<Motal/>)}
      </div>
  );
};
export default App;