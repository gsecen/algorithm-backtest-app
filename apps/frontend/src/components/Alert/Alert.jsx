import { useState, useImperativeHandle, forwardRef } from "react";
import "./alert.css";

const Alert = forwardRef(({ errorMessage }, ref) => {
  const [showAlert, setShowAlert] = useState(true);
  const [showText, setShowText] = useState(false);

  function showAlertExclamtion() {
    setShowAlert(true);
  }
  function hideAlertExclamtion() {
    setShowAlert(false);
  }

  useImperativeHandle(ref, () => ({
    showAlertExclamtion,
    hideAlertExclamtion,
  }));

  return (
    <div className={`alert-container ${showAlert ? "" : "hidden"}`}>
      <p
        onMouseEnter={() => {
          setShowText(!showText);
        }}
        onMouseLeave={() => {
          setShowText(!showText);
        }}
        className="exclamation-mark"
      >
        !
      </p>
      <p className={`error-message-text ${showText ? "" : "hidden"}`}>
        {errorMessage}
      </p>
    </div>
  );
});

export default Alert;
