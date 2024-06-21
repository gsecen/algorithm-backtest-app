import React, { useState } from "react";
import "./buy.css";

import EditDelete from "../../../AlgoBuilder/EditDelete/EditDelete";
import Exclamtion from "../../../Exclamation/Exclamtion";

const Buy = () => {
  const [tickerSymbol, setTickerSymbol] = useState("TICKER");
  const [editableInput, setEditableInput] = useState(false);
  const [editDeleteMenu, setEditDeleteMenu] = useState("hidden");
  const [hovering, setHovering] = useState(false);

  let editDeleteMenuOpacity = 1;
  if (editDeleteMenu === "hidden") {
    editDeleteMenuOpacity = 0;
  }

  let exclamationVisibility = "hidden";
  let exclamationOpacity = 0;
  if (tickerSymbol === "TICKER") {
    exclamationVisibility = "visible";
    exclamationOpacity = 1;
  }

  function toggleEditable() {
    setEditableInput(!editableInput);
  }

  function currentlyHovering() {
    setHovering(true);
    setEditDeleteMenu("visible");
  }

  function notCurrentlyHovering() {
    setHovering(false);
    if (!editableInput) {
      setEditDeleteMenu("hidden");
    }
  }

  function maybeHideEditDeleteMenu() {
    if (!hovering) {
      setEditDeleteMenu("hidden");
    }
  }

  const Input = (
    <input
      onChange={(e) => {
        setTickerSymbol(e.target.value);
      }}
      // When input loses focus (clicked outside of input)
      onBlur={() => {
        toggleEditable();
        maybeHideEditDeleteMenu();
      }}
      className="ticker-symbol-input"
      autoFocus={true}
      value={tickerSymbol}
      // maxLength={20}
      type="text"
    />
  );

  const P = <p className="ticker-symbol-text">{tickerSymbol}</p>;

  return (
    <div
      onMouseEnter={currentlyHovering}
      onMouseLeave={notCurrentlyHovering}
      className="buy-item-container"
    >
      <div className="buy-symbol">
        <p className="dollar-sign">$</p>
      </div>
      {editableInput ? Input : P}

      <EditDelete
        editStyles={{
          visibility: editDeleteMenu,
          opacity: editDeleteMenuOpacity,
        }}
        editMe={toggleEditable}
        className="edit-delete-item"
      ></EditDelete>

      <Exclamtion
        editStyles={{
          visibility: exclamationVisibility,
          opacity: exclamationOpacity,
        }}
        errorMessage={"You must enter a ticker symbol"}
      ></Exclamtion>
    </div>
  );
};

export default Buy;
