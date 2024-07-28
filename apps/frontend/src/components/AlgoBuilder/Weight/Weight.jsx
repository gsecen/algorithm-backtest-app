import { useState, useRef, useEffect } from "react";
import {
  Handle,
  Position,
  useNodeId,
  useReactFlow,
  getOutgoers,
} from "@xyflow/react";
import {
  getImmediateNodeEdges,
  changeAllEdgeTypes,
} from "../../../utils/reactFlow";
import "./weight.css";

const Weight = ({ data }) => {
  const [weightingType, setWeightingType] = useState("Equal");
  const myId = useRef(useNodeId());
  const { getNode, getNodes, setNodes, getEdges, setEdges, updateNodeData } =
    useReactFlow();

  // Set nodes weighting type in data to equal on mount
  useEffect(() => {
    updateNodeData(myId.current, { weightingType: "Equal" });
  }, []);

  function changeWeightingType(type) {
    // If current weighting type is the same as the one you want to change to dont do anything
    if (type === weightingType) {
      return;
    }

    // Get immediate edges
    const immediateEdges = getImmediateNodeEdges(myId.current, getEdges());

    // Change edges to desired type
    changeAllEdgeTypes(type, getEdges(), immediateEdges, setEdges);

    setWeightingType(type);
  }

  return (
    <div>
      <Handle
        type="target"
        position={Position.Top}
        isConnectableStart={false}
      />
      <Handle type="source" position={Position.Bottom} />
      <p>Weight type: {weightingType}</p>
      <ul>
        <li>
          <button>set weight to equal</button>
        </li>
        <li>
          <button
            onClick={() => {
              changeWeightingType("step");
            }}
          >
            set weight to specified
          </button>
        </li>
      </ul>
    </div>
  );
};

export default Weight;
