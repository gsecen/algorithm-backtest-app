import { useState, useRef } from "react";
import { Handle, Position, useReactFlow, useNodeId } from "@xyflow/react";
import { changeIds, changeNodeType, pasteNode } from "../../../utils/reactFlow";
import ActionsBar from "../ActionsBar/ActionsBar";
import plusIcon from "../../../assets/images/plus-circle.svg";
import buyIcon from "../../../assets/images/dollar-sign.svg";
import weightIcon from "../../../assets/images/balanced-scale.svg";
import pasteIcon from "../../../assets/images/paste.svg";
import ifElseIcon from "../../../assets/images/not-equal.svg";
import "./nodeSelector.css";

// Sub component which will hold the node selector dropdown list item
const NodeSelectorDropdownItem = ({
  icon,
  iconColor,
  title,
  information,
  onClickFunction,
}) => {
  return (
    <li onClick={onClickFunction} className="node-selector-dropdown-item">
      <div
        style={{ backgroundColor: iconColor }}
        className="node-selector-dropdown-icon-container"
      >
        <img src={icon} alt="" className="node-selector-dropdown-icon" />
      </div>
      <p className="node-selector-dropdown-text">
        {title}
        <span>{information}</span>
      </p>
    </li>
  );
};

const NodeSelector = ({ data }) => {
  const [showDropdown, setShowDropdown] = useState(true);
  const myId = useRef(useNodeId());

  const actionsBarRef = useRef();

  const { getNode, getNodes, setNodes, getEdges, setEdges } = useReactFlow();

  function addBuyNode() {
    changeNodeType(myId.current, "buy", getNodes(), getNode, setNodes);
  }

  function addExpressionNode() {
    changeNodeType(myId.current, "expression", getNodes(), getNode, setNodes);
  }

  function addWeightNode() {
    changeNodeType(myId.current, "weight", getNodes(), getNode, setNodes);
  }

  function paste() {
    // Get copied nodes data
    const copiedNodeData = getNode("1").data.copiedNode;

    // // Change the ids of everything
    // const changedIdStructure = changeIds(
    //   copiedNode[0],
    //   copiedNode[1],
    //   copiedNode[2]
    // );

    const copiedRootNode = copiedNodeData[0];
    const copiedNodes = copiedNodeData[1];
    const copiedEdges = copiedNodeData[2];

    pasteNode(
      myId.current,
      getNodes(),
      getEdges(),
      copiedRootNode,
      copiedNodes,
      copiedEdges,
      getNode,
      setNodes,
      setEdges
    );
  }

  return (
    <div
      className="node-selector-container"
      onMouseEnter={() => {
        actionsBarRef.current.currentlyHovering();
      }}
      onMouseLeave={() => {
        actionsBarRef.current.notCurrentlyHovering();
      }}
    >
      <Handle
        type="target"
        position={Position.Top}
        isConnectableStart={false}
      />

      <div
        onClick={() => {
          setShowDropdown(!showDropdown);
        }}
        className="node-selector-menu"
      >
        <img src={plusIcon} alt="" className="node-selector-menu-icon" />
        <p className="node-selector-menu-text">
          Add a Node <span>Assets, Weights, FRED...</span>
        </p>
        <ActionsBar ref={actionsBarRef}></ActionsBar>
      </div>

      <div
        className={`node-selector-dropdown-container ${
          showDropdown ? "" : "hidden"
        }`}
      >
        <p className="node-selector-dropdown-title">Add Node</p>
        <ul className="node-selector-dropdown">
          <NodeSelectorDropdownItem
            icon={buyIcon}
            title={"Asset"}
            information={
              "Add any asset who's data is provided by Yahoo Finance"
            }
            onClickFunction={addBuyNode}
          ></NodeSelectorDropdownItem>
          <NodeSelectorDropdownItem
            icon={weightIcon}
            // iconColor={"rgb(49, 128, 90)"}
            title={"Weight (Allocation)"}
            information={"Decide how funds are allocated to nodes and assets"}
            onClickFunction={addWeightNode}
          ></NodeSelectorDropdownItem>
          <NodeSelectorDropdownItem
            icon={ifElseIcon}
            // iconColor={"rgb(36, 101, 217)"}
            title={"If/Else Statements"}
            information={"Use indicators and functions to create if/else logic"}
            onClickFunction={addExpressionNode}
          ></NodeSelectorDropdownItem>
          <NodeSelectorDropdownItem
            icon={pasteIcon}
            title={"Paste"}
            information={"Paste copied nodes"}
            onClickFunction={paste}
          ></NodeSelectorDropdownItem>
        </ul>
      </div>
    </div>
  );
};

export default NodeSelector;
