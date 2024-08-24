import { useState, useRef, useEffect } from "react";
import { Handle, Position, useNodeId } from "@xyflow/react";
import ActionsBar from "../ActionsBar/ActionsBar";
import Alert from "../../Alert/Alert";
import "./buy.css";

const Buy = ({ data }) => {
  const myId = useRef(useNodeId());
  const [ticker, setTicker] = useState("");
  const [isFocused, setIsFocused] = useState(false);

  const actionsBarRef = useRef();
  const alertRef = useRef();

  // every time ticker changes do the following
  useEffect(() => {
    // If ticker symbol is blank buy node still needs to be edited so show alert
    if (ticker.trim() === "") {
      alertRef.current.showAlertExclamtion();
    } else {
      alertRef.current.hideAlertExclamtion();
    }
  }, [ticker]);

  // function puts the ticker symbol input into focus and makes it editable
  function makeInputEditable() {
    const input = document.getElementById(`ticker-input-${myId.current}`);
    input.disabled = false;
    input.readOnly = false;
    input.focus();
  }

  // function makes the ticker symbol input uneditable and unfocusable
  function makeInputUnEditable() {
    const input = document.getElementById(`ticker-input-${myId.current}`);
    input.disabled = true;
    input.readOnly = true;
  }

  return (
    <div
      className="buy-container"
      onMouseEnter={() => {
        actionsBarRef.current.currentlyHovering();
      }}
      onMouseLeave={() => {
        actionsBarRef.current.notCurrentlyHovering();
      }}
    >
      <Handle
        // https://reactflow.dev/api-reference/components/handle#is-connectable
        // You cannot connect anything from the handle
        isConnectableStart={false}
        type="target"
        position={Position.Top}
      />
      <p className="buy-dollar-sign">$</p>
      <input
        onChange={(event) => {
          setTicker(event.target.value.toUpperCase());
          event.target.value = event.target.value.toUpperCase();
        }}
        onBlur={() => {
          makeInputUnEditable();
          actionsBarRef.current.checkHoverOnEditComplete();
          setIsFocused(false);
        }}
        onFocus={() => {
          setIsFocused(true);
        }}
        className="ticker-symbol-input"
        id={`ticker-input-${myId.current}`}
        type="text"
        placeholder="TICKER"
        readOnly
        disabled
      />
      <ActionsBar
        ref={actionsBarRef}
        focused={isFocused}
        editMeFunction={makeInputEditable}
      ></ActionsBar>
      <Alert
        ref={alertRef}
        errorMessage={"Enter Ticker Symbol (Yahoo Finance)"}
      ></Alert>
    </div>
  );
};

export default Buy;
