import React, { useState } from "react";
import "./specifiedWeight.css";

import EditDelete from "../../EditDelete/EditDelete";

const SpecifiedWeight = (props) => {
  const [weight, setWeight] = useState("Set Weight");
  const [editableInput, setEditableInput] = useState(false);
  const [editDeleteMenu, setEditDeleteMenu] = useState("hidden");
  const [hovering, setHovering] = useState(false);

  // Edit delete menu is shown when specified weight item is hovered or input is being edited
  let editDeleteMenuOpacity = 1;
  if (editDeleteMenu === "hidden") {
    editDeleteMenuOpacity = 0;
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

  // Puts the weight into proper format with 2 decimals and percentage sign
  function properFormatWeight(string) {
    // If string cannot be turned into a number
    if (!Number(string)) {
      return string;
    }

    return `${Number(string).toFixed(2)}%`;
  }

  properFormatWeight(weight);

  // Used when the user wants to edit weight percentage
  const Input = (
    <input
      onChange={(e) => {
        setWeight(e.target.value);
      }}
      // When input loses focus (clicked outside of input)
      onBlur={() => {
        toggleEditable();
        maybeHideEditDeleteMenu();
        // props.updateSpecifiedWeight(props.id, tickerSymbol);
      }}
      className="specified-weight-input"
      autoFocus={true}
      value={weight}
      type={"number"}
    />
  );

  // Used when the user is not trying to edit weight percentage
  const P = (
    <p className="specified-weight-text">{properFormatWeight(weight)}</p>
  );

  return (
    <div
      onMouseEnter={currentlyHovering}
      onMouseLeave={notCurrentlyHovering}
      className="specified-weight-container"
    >
      <div className="specified-weight-input-text-container">
        {editableInput ? Input : P}
      </div>

      <EditDelete
        editStyles={{
          visibility: editDeleteMenu,
          opacity: editDeleteMenuOpacity,
        }}
        editMe={toggleEditable}
      ></EditDelete>
    </div>
  );
};

export default SpecifiedWeight;
