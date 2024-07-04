import { useRef, useState } from "react";
import "./specifiedWeight.css";

import EditDelete from "../../EditDelete/EditDelete";
import ActionsBar from "../../ActionsBar/ActionsBar";

const SpecifiedWeight = (props) => {
  // const [weight, setWeight] = useState("Set Weight");
  const [weight, setWeight] = useState(props.specifiedWeight);
  const [editableInput, setEditableInput] = useState(false);

  function toggleEditable() {
    setEditableInput(!editableInput);
  }

  const actionsBarRef = useRef();

  // Variables which will be passed down to the edit delete menu
  const myId = props.id;
  const deleteMeFunction = props.deleteMe;

  // Puts the weight into proper format with 2 decimals and percentage sign
  function properFormatWeight(string) {
    // If string cannot be turned into a number or its blank
    if (!Number(string) || string === "") {
      return "Set Weight";
    }

    return `${Number(string).toFixed(2)}%`;
  }

  // Used when the user wants to edit weight percentage
  const Input = (
    <input
      onChange={(e) => {
        setWeight(e.target.value);
      }}
      // When input loses focus (clicked outside of input)
      onBlur={() => {
        toggleEditable();
        actionsBarRef.current.checkHoverOnEditComplete();
        props.updateSpecifiedWeight(props.id, weight);
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
      onMouseEnter={() => {
        actionsBarRef.current.currentlyHovering();
      }}
      onMouseLeave={() => {
        actionsBarRef.current.notCurrentlyHovering();
      }}
      className="specified-weight-container"
    >
      <div className="specified-weight-input-text-container">
        {editableInput ? Input : P}
      </div>

      <ActionsBar
        ref={actionsBarRef}
        id={myId}
        editing={editableInput}
        editMe={toggleEditable}
        deleteMe={deleteMeFunction}
      ></ActionsBar>
    </div>
  );
};

export default SpecifiedWeight;
