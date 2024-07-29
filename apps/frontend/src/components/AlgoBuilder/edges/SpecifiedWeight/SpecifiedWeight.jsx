import { FC, useState, useRef, useEffect } from "react";
import {
  EdgeProps,
  getBezierPath,
  EdgeLabelRenderer,
  BaseEdge,
  Edge,
  useReactFlow,
  useNodesData,
} from "@xyflow/react";

import "./specifiedWeight.css";

const SpecifiedWeight = ({
  id,
  sourceX,
  sourceY,
  targetX,
  targetY,
  sourcePosition,
  targetPosition,
  data,
}) => {
  const [weight, setWeight] = useState("Set Weight");

  const { getEdge, updateNodeData, getNode } = useReactFlow();
  const mySourceId = useRef(getEdge(id).source);
  const myTargetId = useRef(getEdge(id).target);

  // Let parent weight node know that a new specified weight edge has been added to it
  useEffect(() => {
    // Get parent weight nodes current specified weights hashmap
    let specifiedWeightsHashmap = getNode(mySourceId.current).data
      .specifiedWeights;

    // Add my id and defualt weight to hashmap
    specifiedWeightsHashmap[id] = weight;

    // Update parent weight nodes specifiedWeights hashmap
    updateNodeData(mySourceId.current, {
      specifiedWeights: specifiedWeightsHashmap,
    });
  }, []);

  const [edgePath, labelX, labelY] = getBezierPath({
    sourceX,
    sourceY,
    sourcePosition,
    targetX,
    targetY,
    targetPosition,
  });

  // Puts the weight into proper format with 2 decimals and percentage sign
  function formatWeight(string) {
    // If string cannot be turned into a number or its blank
    if (!Number(string) || string === "") {
      return "Set Weight";
    }

    return `${Number(string).toFixed(2)}%`;
  }

  function updateParentWeightNodesData() {
    // Get parent weight nodes current specified weights hashmap
    let specifiedWeightsHashmap = getNode(mySourceId.current).data
      .specifiedWeights;

    // Update my weight in the hashmap
    specifiedWeightsHashmap[id] = weight;

    // Update parent weight nodes specifiedWeights hashmap
    updateNodeData(mySourceId.current, {
      specifiedWeights: specifiedWeightsHashmap,
    });
  }

  return (
    <>
      <BaseEdge id={id} path={edgePath} />
      <EdgeLabelRenderer>
        <div
          style={{
            position: "absolute",
            transform: `translate(-50%, -50%) translate(${labelX}px,${labelY}px)`,
            background: "#6699ff",
            padding: 10,
            borderRadius: 5,
            fontSize: 12,
            fontWeight: 700,

            pointerEvents: "all",
          }}
          className="nodrag nopan"
        >
          <button
            onClick={() => {
              console.log(myTargetId);
              console.log(mySourceId);
            }}
          >
            get my target node id and my source id
          </button>
          <p>Specified Weight</p>
          <input
            onFocus={(event) => {
              event.target.type = "number";
              event.target.step = "0.01";
              event.target.value = weight;
            }}
            onBlur={(event) => {
              event.target.type = "text";
              event.target.value = formatWeight(weight);
              updateParentWeightNodesData();
            }}
            onChange={(event) => {
              setWeight(event.target.value);
            }}
            placeholder="Set Weight"
          />
        </div>
      </EdgeLabelRenderer>
    </>
  );
};

export default SpecifiedWeight;
