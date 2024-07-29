import { FC, useState } from "react";
import {
  EdgeProps,
  getBezierPath,
  EdgeLabelRenderer,
  BaseEdge,
  Edge,
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
  console.log(weight);

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
