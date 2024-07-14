import editIcon from "../../../assets/images/pencil-icon.svg";
import deleteIcon from "../../../assets/images/trash-can-icon.svg";
import { useState } from "react";
import { forwardRef } from "react";
import { useImperativeHandle } from "react";

// https://stackoverflow.com/questions/37949981/call-child-method-from-parent

const ClassTest = forwardRef((props, ref) => {
  const [editableInput, setEditableInput] = useState(false);
  const [editDeleteMenu, setEditDeleteMenu] = useState("hidden");
  const [hovering, setHovering] = useState(false);

  useImperativeHandle(ref, () => ({
    currentlyHovering,
    notCurrentlyHovering,
    hovering,
  }));

  function getHovering() {
    console.log(hovering);
  }

  function deleteComponent() {
    props.deleteMe(props.id);
  }

  function editComponent() {
    props.editMe();
  }

  // Edit delete menu is shown when buy item is hovered or input is being edited
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

  // When the input is done being edited checks to see if still being hovered over
  function maybeHideEditDeleteMenu() {
    if (!hovering) {
      setEditDeleteMenu("hidden");
    }
  }

  return (
    <div
      style={{
        visibility: editDeleteMenu,
        opacity: editDeleteMenuOpacity,
      }}
      className="edit-delete-container"
    >
      <div onClick={editComponent} className="edit-button">
        <img src={editIcon} alt="" className="edit-icon" />
      </div>
      <div onClick={deleteComponent} className="delete-button">
        <img src={deleteIcon} alt="" className="edit-icon" />
      </div>
    </div>
  );
});

export default ClassTest;
