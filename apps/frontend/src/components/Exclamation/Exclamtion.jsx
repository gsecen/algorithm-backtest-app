import { useState } from "react";
import "./exclamation.css";

/**
 * @property {string} errorMessage The message from parent to show if there is an error.
 * @property {boolean} isError The boolean from parent which will let Exclamtion know if parent has error.
 * @returns {ReactNode} Exclamation react element.
 */
const Exclamtion = ({ errorMessage, isError }) => {
  const [showText, setShowText] = useState(false);

  let exclamationVisibility = "hidden";
  let exclamationOpacity = 0;

  // Exclamation is shown if there is an error
  if (isError) {
    exclamationVisibility = "visible";
    exclamationOpacity = 1;
  }

  const ErrorText = <div className="red-exclamation-text">{errorMessage}</div>;

  function toggleText() {
    setShowText(!showText);
  }

  return (
    <div
      style={{ visibility: exclamationVisibility, opacity: exclamationOpacity }}
      className="red-exclamation-container"
    >
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
