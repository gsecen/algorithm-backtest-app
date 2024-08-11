import { useState, useRef, useEffect } from "react";
import { Handle, Position, useNodeId } from "@xyflow/react";
import ActionsBar from "../ActionsBar/ActionsBar";
import Alert from "../../Alert/Alert";
import "./buy.css";

const Buy = ({ data }) => {
  const myId = useRef(useNodeId());
  const [ticker, setTicker] = useState("TICKER");

  const actionsBarRef = useRef();
  const alertRef = useRef();

  // every time ticker changes do the following
  useEffect(() => {
    // If ticker symbol is "TICKER" or blank buy node still needs to be edited so show alert
    if (ticker === "TICKER" || ticker.trim() === "") {
      alertRef.current.showAlertExclamtion();
    } else {
      alertRef.current.hideAlertExclamtion();
    }
  }, [ticker]);

  // function puts the ticker symbol input into focus and makes it editable
  function makeInputEditable() {
    const input = document.getElementById("ticker-input");
    input.disabled = false;
    input.readOnly = false;
    input.focus();
  }

  // function makes the ticker symbol input uneditable and unfocusable
  function makeInputUnEditable() {
    const input = document.getElementById("ticker-input");
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
      <input
        onChange={(event) => {
          setTicker(event.target.value.toUpperCase());
        }}
        onBlur={makeInputUnEditable}
        className="ticker-symbol-input"
        id="ticker-input"
        type="text"
        value={ticker}
        readOnly
        disabled
      />
      <ActionsBar
        ref={actionsBarRef}
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
