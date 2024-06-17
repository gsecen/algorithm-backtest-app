import React, { useState } from "react";
import "./exclamation.css";

const Exclamtion = () => {
  const [showText, setShowText] = useState(false);

  const ErrorText = (
    <div className="red-exclamation-text">You must enter a ticker symbol</div>
  );

  function toggleText() {
    setShowText(!showText);
  }

  return (
    <div className="red-exclamation-container">
      <div
        onMouseEnter={toggleText}
        onMouseLeave={toggleText}
        className="red-exclamation"
      >
        !
      </div>

      {showText ? ErrorText : null}
    </div>
  );
};

export default Exclamtion;
