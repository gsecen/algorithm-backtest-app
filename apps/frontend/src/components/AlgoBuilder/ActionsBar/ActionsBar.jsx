import { useState, forwardRef, useImperativeHandle } from "react";
import "./actionsBar.css";
import editIcon from "../../../assets/images/pencil-icon.svg";
import deleteIcon from "../../../assets/images/trash-can-icon.svg";

// https://stackoverflow.com/a/69464092
// 3. Hook Parent | Hook Child
// https://stackoverflow.com/questions/37949981/call-child-method-from-parent
// https://react.dev/reference/react/useImperativeHandle

// Imagine this component as a combination of class and component. Whatever is in the useImperativeHandle whether
// is it variables or functions, they are exposed to the parent and can be accessed and called by a parent
// component.

/**
 *
 * @property {function} deleteMe The function from parent which will delete element.
 * @property {function} editMe The function from parent which will edit element.
 * @property {boolean} focused The boolean from parent which will let actions bar know if parents input is in focus.
 * @property {int} id The elements unqiue id.
 * @returns {ReactNode} Actions bar react element.
 */
const ActionsBar = forwardRef(({ id, editMe, deleteMe, focused }, ref) => {
  const isItemFocused = focused;
  const [editDeleteMenu, setEditDeleteMenu] = useState("hidden");
  const [hovering, setHovering] = useState(false);

  function editComponent() {
    editMe();
  }

  function deleteComponent() {
    deleteMe(id);
  }

  useImperativeHandle(ref, () => ({
    currentlyHovering,
    notCurrentlyHovering,
    checkHoverOnEditComplete,
  }));

  // Edit delete menu is shown when item is hovered or input is being edited
  let editDeleteMenuOpacity = 1;
  if (editDeleteMenu === "hidden") {
    editDeleteMenuOpacity = 0;
  }

  // When an item is being hovered
  function currentlyHovering() {
    setHovering(true);
    setEditDeleteMenu("visible");
  }

  // When an item is no longer being hovered
  function notCurrentlyHovering() {
    setHovering(false);

    // Check if item is being edited
    if (!isItemFocused) {
      setEditDeleteMenu("hidden");
    }
  }

  // When an item is done being edited, check to see if still being hovered
  function checkHoverOnEditComplete() {
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
      className="actions-bar-container"
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

export default ActionsBar;
