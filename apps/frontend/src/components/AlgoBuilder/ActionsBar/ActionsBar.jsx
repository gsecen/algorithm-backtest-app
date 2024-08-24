import { useState, useRef, useImperativeHandle, forwardRef } from "react";
import { Handle, Position, useReactFlow, useNodeId } from "@xyflow/react";
import {
  deleteNodeAndAllNodeChildren,
  deleteAllNodeChildren,
  copyNode,
} from "../../../utils/reactFlow";
import editIcon from "../../../assets/images/pencil.svg";
import deleteIcon from "../../../assets/images/trash-can.svg";
import otherIcon from "../../../assets/images/three-dots.svg";
import copyIcon from "../../../assets/images/copy.svg";
import deleteChildrenIcon from "../../../assets/images/delete-node.svg";
import "./actionsBar.css";

// https://stackoverflow.com/a/69464092
// 3. Hook Parent | Hook Child
// https://stackoverflow.com/questions/37949981/call-child-method-from-parent
// https://react.dev/reference/react/useImperativeHandle

// Imagine this component as a combination of class and component. Whatever is in the useImperativeHandle whether
// is it variables or functions, they are exposed to the parent and can be accessed and called by a parent
// component.

const ActionsBar = forwardRef(({ editMeFunction, focused, nodeType }, ref) => {
  // Keep track of if parent node is currently being used so we know to show actions bar
  const isItemFocused = focused;
  const [showActionsBar, setShowActionsBar] = useState(false);
  const [showSubMenu, setShowSubMenu] = useState(false);
  const [hovering, setHovering] = useState(false);

  // For different nodes show different menu variations

  const { getNodes, getEdges, deleteElements, getNode, updateNodeData } =
    useReactFlow();
  const myId = useRef(useNodeId());

  function deleteNode() {
    deleteNodeAndAllNodeChildren(
      myId.current,
      getNodes(),
      getEdges(),
      deleteElements
    );
  }

  function deleteNodeChildren() {
    deleteAllNodeChildren(myId.current, getNodes(), getEdges(), deleteElements);
  }

  function copy() {
    const copiedNodeData = copyNode(
      myId.current,
      getNodes(),
      getEdges(),
      getNode
    );

    // Store copied node data in the root node of the react flow
    updateNodeData("1", {
      copiedNode: copiedNodeData,
    });
  }

  // When an item is being hovered
  function currentlyHovering() {
    setHovering(true);
    setShowActionsBar(true);
  }

  // When an item is no longer being hovered
  function notCurrentlyHovering() {
    setHovering(false);

    // Check if item is being edited
    if (!isItemFocused) {
      setShowActionsBar(false);
    }
  }

  // When an item is done being edited, check to see if still being hovered
  function checkHoverOnEditComplete() {
    if (!hovering) {
      setShowActionsBar(false);
    }
  }

  useImperativeHandle(ref, () => ({
    currentlyHovering,
    notCurrentlyHovering,
    checkHoverOnEditComplete,
  }));

  return (
    <div className={`actions-bar-container ${showActionsBar ? "" : "hidden"}`}>
      {/* <ul>
        <li>
          <button>edit me</button>
          <button onClick={deleteNode}>delete me</button>
          <button onClick={deleteNodeChildren}>delete children</button>
          <button onClick={copy}>copy me</button>
        </li>
      </ul> */}
      <ul className="actions-bar-main-menu">
        <li onClick={editMeFunction} className="actions-bar-main-menu-item">
          <img className="actions-bar-icon" src={editIcon} alt="" />
        </li>
        <li className="actions-bar-main-menu-item">
          <img className="actions-bar-icon" src={deleteIcon} alt="" />
        </li>
        <li
          onClick={() => {
            setShowSubMenu(!showSubMenu);
          }}
          className="actions-bar-main-menu-item"
        >
          <img className="actions-bar-icon" src={otherIcon} alt="" />
        </li>
      </ul>

      <ul className={`actions-bar-sub-menu ${showSubMenu ? "" : "hidden"}`}>
        <li className="actions-bar-sub-menu-item">
          <img className="actions-bar-icon" src={copyIcon} alt="" />
          <p className="actions-bar-sub-menu-text">Copy</p>
        </li>
        <li className="actions-bar-sub-menu-item">
          <img className="actions-bar-icon" src={deleteChildrenIcon} alt="" />
          <p className="actions-bar-sub-menu-text">Remove Child Nodes</p>
        </li>
      </ul>
    </div>
  );
});

export default ActionsBar;
