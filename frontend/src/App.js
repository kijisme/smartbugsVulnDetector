import React, { useState } from 'react';
import Modal from './compoments/Modal';

const App = () => {
  const [isModalOpen, setModalOpen] = useState(false);

  const openModal = () => {
    setModalOpen(true);
  };

  const closeModal = () => {
    setModalOpen(false);
  };

  return (
    <div>
      <button onClick={openModal}>Open Modal</button>

      <Modal isOpen={isModalOpen} onClose={closeModal} />
    </div>
  );
};

export default App;
