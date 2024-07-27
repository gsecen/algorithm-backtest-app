import { useState } from "react";
import { Handle, Position } from "@xyflow/react";
import "./nodeSelector.css";

const NodeSelector = ({ data }) => {
  const [showDropdown, setShowDropdown] = useState(true);

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
        <li className="node-selector-list-item">Asset</li>
        <li className="node-selector-list-item">If Else</li>
        <li className="node-selector-list-item">Group</li>
        <li className="node-selector-list-item">Weight</li>
        <li className="node-selector-list-item">Paste</li>
      </ul>
    </div>
  );
};

export default NodeSelector;
