import React from 'react';

/**
 * A sample Button component for testing.
 */
const CustomButton = ({ label, onClick, disabled }) => {
  return (
    <button onClick={onClick} disabled={disabled}>
      {label}
    </button>
  );
};

export default CustomButton;
