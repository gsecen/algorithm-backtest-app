import React, { useState } from "react";
import "./exclamation.css";

const Exclamtion = (props) => {
  const [showText, setShowText] = useState(false);

  const ErrorText = (
    <div className="red-exclamation-text">{props.errorMessage}</div>
  );

  function toggleText() {
    setShowText(!showText);
  }

  return (
    <div style={props.editStyles} className="red-exclamation-container">
      <div
        onMouseEnter={toggleText}
        onMouseLeave={toggleText}
        className="red-exclamation"
      >
        <p className="exclamtion">!</p>
      </div>

      {showText ? ErrorText : null}
    </div>
  );
};

export default Exclamtion;
