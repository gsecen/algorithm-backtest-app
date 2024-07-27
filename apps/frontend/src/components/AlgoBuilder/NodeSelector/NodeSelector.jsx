import { useState, useRef } from "react";
import { Handle, Position, useReactFlow, useNodeId } from "@xyflow/react";
import { replaceNode } from "../../../utils/reactFlow";
import "./nodeSelector.css";

const NodeSelector = ({ data }) => {
  const [showDropdown, setShowDropdown] = useState(true);
  const myId = useRef(useNodeId());

  const { getNode, getNodes, setNodes } = useReactFlow();

  function test() {
    console.log(myId);
    replaceNode(myId.current, "buy", getNodes(), getNode, setNodes);
  }

  function test2() {
    replaceNode(myId.current, "expression", getNodes(), getNode, setNodes);
  }

  return (
    <div>
      <Handle type="target" position={Position.Top} />
      <div
        onClick={() => {
          setShowDropdown(!showDropdown);
        }}
        className="node-selector-block"
      >
        add asset, weight, if else... click for dropdown
      </div>
      <ul className={`node-selector-list ${showDropdown ? "" : "hidden"}`}>
        <li onClick={test} className="node-selector-list-item">
          Asset
        </li>
        <li onClick={test2} className="node-selector-list-item">
          If Else
        </li>
        <li className="node-selector-list-item">Group</li>
        <li className="node-selector-list-item">Weight</li>
        <li className="node-selector-list-item">Paste</li>
      </ul>
    </div>
  );
};

export default NodeSelector;
