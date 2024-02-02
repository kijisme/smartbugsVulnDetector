import React, { useState } from 'react';

const Modal = ({ isOpen, onClose }) => {
  const [modalContent, setModalContent] = useState("Initial Content");

  const handleButtonClick = () => {
    // 在按钮点击时修改弹窗内容
    setModalContent("Updated Content");
  };

  return (
    <div className="modal" style={{ display: isOpen ? 'block' : 'none' }}>
      <div className="modal-content">
        <span className="close" onClick={onClose}>&times;</span>
        <p>{modalContent}</p>
        <button onClick={handleButtonClick}>Update Content</button>
      </div>
    </div>
  );
};

export default Modal;
