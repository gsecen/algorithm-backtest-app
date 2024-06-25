import React, { useState } from "react";
import "./buy.css";

import EditDelete from "../../../AlgoBuilder/EditDelete/EditDelete";
import Exclamtion from "../../../Exclamation/Exclamtion";

/**
 *
 * @property {function} deleteMe The function from parent which will element.
 * @property {function} updateTickerSymbol The function from parent which will update elements ticker symbol.
 * @property {int} id The elements unqiue id.
 * @property {string} tickerSymbol The ticker symbol which will be displayed to the user.
 * @returns {ReactNode} Algorithms type buy react element.
 */
const Buy = (props) => {
  const [tickerSymbol, setTickerSymbol] = useState(props.tickerSymbol);
  const [editableInput, setEditableInput] = useState(false);
  const [editDeleteMenu, setEditDeleteMenu] = useState("hidden");
  const [hovering, setHovering] = useState(false);

  // Variables which will be passed down to the edit delete menu
  const myId = props.id;
  const deleteMeFunction = props.deleteMe;

  // Edit delete menu is shown when buy item is hovered or input is being edited
  let editDeleteMenuOpacity = 1;
  if (editDeleteMenu === "hidden") {
    editDeleteMenuOpacity = 0;
  }

  // Exclamation is shown if ticker symbol is "TICKER" which means it still needs to be edited
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

  // When the input is done being edited checks to see if still hovering over buy item
  function maybeHideEditDeleteMenu() {
    if (!hovering) {
      setEditDeleteMenu("hidden");
    }
  }

  // Used when the user wants to edit ticker symbol
  const Input = (
    <input
      onChange={(e) => {
        setTickerSymbol(e.target.value.toUpperCase());
      }}
      // When input loses focus (clicked outside of input)
      onBlur={() => {
        toggleEditable();
        maybeHideEditDeleteMenu();
        props.updateTickerSymbol(props.id, tickerSymbol);
      }}
      className="ticker-symbol-input"
      autoFocus={true}
      value={tickerSymbol}
      type="text"
    />
  );

  // Used when the user is not trying to edit input
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
        id={myId}
        deleteMe={deleteMeFunction}
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
