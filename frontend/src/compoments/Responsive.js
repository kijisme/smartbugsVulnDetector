import React, { useState, useEffect } from 'react';

const ResponsiveComponent = () => {
    // 初始化变量
  const [windowSize, setWindowSize] = useState({
    width: window.innerWidth,
    height: window.innerHeight,
  });

  useEffect(() => {
    const handleResize = () => {
      setWindowSize({
        width: window.innerWidth,
        height: window.innerHeight,
      });
    };

    // 监听窗口大小变化
    window.addEventListener('resize', handleResize);

    // 初始化时获取窗口大小
    handleResize();

    // 清理事件监听器
    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, []); // 仅在组件挂载和卸载时执行

  return (
    <div>
      <p>窗口宽度: {windowSize.width}px</p>
      <p>窗口高度: {windowSize.height}px</p>
      {/* 根据窗口大小添加相应的样式 */}
      <div className={windowSize.width > 600 ? 'large-screen' : 'small-screen'}>
        {/* 内容 */}
      </div>
    </div>
  );
};

export default ResponsiveComponent;
