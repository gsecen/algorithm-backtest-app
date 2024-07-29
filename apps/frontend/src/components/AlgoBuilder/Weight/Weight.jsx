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
  // Set nodes specified weights hashmap to an empty hashmap on mount
  useEffect(() => {
    updateNodeData(myId.current, {
      weightingType: "Equal",
      specifiedWeights: {},
    });
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

    // if we are setting the weighting type to equal, remove all specified weights
    if (type === "default") {
      updateNodeData(myId.current, {
        weightingType: type,
        specifiedWeights: {},
      });
    } else {
      updateNodeData(myId.current, { weightingType: type });
    }
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
      <button
        onClick={() => {
          console.log(getNode(myId.current));
        }}
      >
        console log my data
      </button>
      <ul>
        <li>
          <button
            onClick={() => {
              changeWeightingType("default");
            }}
          >
            set weight to equal
          </button>
        </li>
        <li>
          <button
            onClick={() => {
              changeWeightingType("specifiedWeight");
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
