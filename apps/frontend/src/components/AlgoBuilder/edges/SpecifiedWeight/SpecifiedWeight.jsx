import { FC, useState, useRef, useEffect } from "react";
import {
  EdgeProps,
  getBezierPath,
  EdgeLabelRenderer,
  BaseEdge,
  Edge,
  useReactFlow,
  useNodesData,
  applyNodeChanges,
  useNodeId,
} from "@xyflow/react";
import {
  setHiddenAllNodeChildren,
  setHiddenAllEdgeChildren,
} from "../../../../utils/reactFlow";
import ActionsBar from "../../ActionsBar/ActionsBar";
import hideIcon from "../../../../assets/images/closed-eye.svg";
import showIcon from "../../../../assets/images/open-eye.svg";

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
  const [isFocused, setIsFocused] = useState(false);
  const [hideChildren, setHideChildren] = useState(false);

  const {
    getEdge,
    updateEdgeData,
    updateNodeData,
    getNode,
    updateNode,
    getNodes,
    getEdges,
    setNodes,
  } = useReactFlow();
  const mySourceId = useRef(getEdge(id).source);
  const myTargetId = useRef(getEdge(id).target);

  const actionsBarRef = useRef();

  // Let parent weight node know that a new specified weight edge has been added to it and
  // add default specified weight data
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

    // Update my own weight data
    updateEdgeData(id, {
      specifiedWeight: weight,
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

  function updateMyData() {
    // Update my specified weight data
    updateEdgeData(id, {
      specifiedWeight: weight,
    });
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

  // function puts the specified weight input into focus and makes it editable
  function makeInputEditable() {
    const input = document.getElementById(`weight-input-${id}`);
    input.disabled = false;
    input.readOnly = false;
    input.focus();
  }

  // function makes the specified weight input uneditable and unfocusable
  function makeInputUnEditable() {
    const input = document.getElementById(`weight-input-${id}`);
    input.disabled = true;
    input.readOnly = true;
  }

  // Function will hide all the children of the edge also keeping edge intact so
  // edge will not disappear
  function hideTargetNodeChildren() {
    setHiddenAllEdgeChildren(
      !hideChildren,
      myTargetId.current,
      getNodes(),
      getEdges(),
      setNodes
    );
  }

  return (
    <>
      <BaseEdge id={id} path={edgePath} />
      <EdgeLabelRenderer>
        <div
          onMouseEnter={() => {
            actionsBarRef.current.currentlyHovering();
          }}
          onMouseLeave={() => {
            actionsBarRef.current.notCurrentlyHovering();
          }}
          style={{
            position: "absolute",
            transform: `translate(-50%, -50%) translate(${labelX}px,${labelY}px)`,
            // pointerEvents: "all",
          }}
          className="specified-weight-container"
        >
          <div className="specified-weight-input-container">
            <div
              onClick={() => {
                hideTargetNodeChildren();
                setHideChildren(!hideChildren);
              }}
              className="hide-specified-weight-children-container"
            >
              <img
                src={hideChildren ? hideIcon : showIcon}
                alt=""
                className="hide-specified-weight-children-icon"
              />
            </div>
            <input
              className="specified-weight-input"
              id={`weight-input-${id}`}
              onFocus={(event) => {
                event.target.placeholder = "";
                event.target.type = "number";
                event.target.step = "0.01";
                event.target.value = weight;
                setIsFocused(true);
              }}
              onBlur={(event) => {
                makeInputUnEditable();
                event.target.type = "text";
                event.target.value = formatWeight(weight);
                updateParentWeightNodesData();
                updateMyData();
                actionsBarRef.current.checkHoverOnEditComplete();
                setIsFocused(false);
              }}
              onChange={(event) => {
                setWeight(event.target.value);
              }}
              placeholder="Set Weight"
              readOnly
              disabled
            />
          </div>

          <div className="specified-weight-actions-bar-container">
            <ActionsBar
              ref={actionsBarRef}
              focused={isFocused}
              editMeFunction={makeInputEditable}
            ></ActionsBar>
          </div>
        </div>
      </EdgeLabelRenderer>
    </>
  );
};

export default SpecifiedWeight;
