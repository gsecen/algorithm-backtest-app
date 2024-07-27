import { useEffect, useRef } from "react";
import { Handle, Position, useReactFlow, useNodeId } from "@xyflow/react";
import { createNode } from "../../../utils/reactFlow";
import "./expression.css";

const Expression = () => {
  const myId = useRef(useNodeId());
  const { getNode, getNodes, setNodes, addNodes, addEdges } = useReactFlow();

  // Add the true and false nodes to this expression on mount
  useEffect(() => {
    // Get current node details
    const myDetails = getNode(myId.current);

    console.log(myDetails);

    // Create ids for true and false nodes which will be connected to current node (must be strings)
    const trueNodeId = `${Math.floor(Math.random() * 9999999)}`;
    const falseNodeId = `${Math.floor(Math.random() * 9999999)}`;

    // Create nodes and edges for nodes
    const trueNode = createNode(
      trueNodeId,
      "nodeSelector",
      myDetails.position.x + 50,
      myDetails.position.y + 50
    );
    const falseNode = createNode(
      falseNodeId,
      "nodeSelector",
      myDetails.position.x - 50,
      myDetails.position.y + 50
    );
    const trueEdge = {
      id: `${Math.floor(Math.random() * 9999999)}`,
      source: myId.current,
      target: trueNodeId,
      label: "True",
    };
    const falseEdge = {
      id: `${Math.floor(Math.random() * 9999999)}`,
      source: myId.current,
      target: falseNodeId,
      label: "False",
      animated: true,
    };

    // Add nodes and edges to react flow
    addNodes([trueNode, falseNode]);
    addEdges([trueEdge, falseEdge]);
  }, []);

  return (
    <div>
      <Handle type="target" position={Position.Top} />
      <div>if else conditions something...</div>

      <Handle type="source" position={Position.Bottom} />
    </div>
  );
};

export default Expression;
