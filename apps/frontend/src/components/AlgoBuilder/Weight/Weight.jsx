import { useState, useRef, useEffect } from "react";
import {
  Handle,
  Position,
  useNodeId,
  useReactFlow,
  getOutgoers,
} from "@xyflow/react";
import {
  getImmediateNodeSourceEdges,
  changeAllEdgeTypes,
  setHiddenAllNodeChildren,
} from "../../../utils/reactFlow";
import ActionsBar from "../ActionsBar/ActionsBar";
import Alert from "../../Alert/Alert";
import hideIcon from "../../../assets/images/closed-eye.svg";
import showIcon from "../../../assets/images/open-eye.svg";
import "./weight.css";

const Weight = ({ data }) => {
  const [weightingType, setWeightingType] = useState("Equal");
  const [displayWeight, setDisplayWeight] = useState("Equal");
  const [showDropdown, setShowDropdown] = useState(false);
  const [hideNodeChildren, setHideNodeChildren] = useState(false);
  const myId = useRef(useNodeId());

  const actionsBarRef = useRef();
  const alertRef = useRef();

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
    const immediateEdges = getImmediateNodeSourceEdges(
      myId.current,
      getEdges()
    );

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

    // Based on type change make sure ui shows what weighting type is
    if (type === "default") {
      setDisplayWeight("Equal");
    }
    if (type === "specifedWeight") {
      setDisplayWeight("Specified");
    }
  }

  function hideChildren() {
    setHiddenAllNodeChildren(
      !hideNodeChildren,
      myId.current,
      getNodes(),
      getEdges(),
      setNodes
    );
  }

  function showWeightingTypeDropdown() {
    setShowDropdown(!showDropdown);
  }

  return (
    <div
      className="weight-container"
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
      <Handle type="source" position={Position.Bottom} />

      <div className="weight-selector-container">
        <div
          onClick={() => {
            hideChildren();
            setHideNodeChildren(!hideNodeChildren);
          }}
          className="hide-weight-children-container"
        >
          <img
            src={hideNodeChildren ? hideIcon : showIcon}
            alt=""
            className="hide-weight-children-icon"
          />
        </div>
        <p className="weight-selector-text">
          WEIGHT <span>{displayWeight}</span>
        </p>

        <div
          className={`weight-selector-dropdown-container ${
            showDropdown ? "" : "hidden"
          }`}
        >
          <p className="weight-selector-dropdown-title">Set Weighting Type</p>
          <p
            className="weight-selector-dropdown-item"
            onClick={() => {
              changeWeightingType("default");
            }}
          >
            Equal
            <span>
              All of the child nodes receive an equal proportion of the weight
            </span>
          </p>
          <p
            className="weight-selector-dropdown-item"
            onClick={() => {
              changeWeightingType("specifiedWeight");
            }}
          >
            Specified
            <span>Weights of child nodes are specified with a percentage</span>
          </p>
        </div>

        <div className="weight-actions-alert-container">
          <ActionsBar
            ref={actionsBarRef}
            editMeFunction={showWeightingTypeDropdown}
            focused={showDropdown}
          ></ActionsBar>
          <Alert
            ref={alertRef}
            errorMessage={"Specified weights must add up to 100%"}
          ></Alert>
        </div>
      </div>

      {/* <div className="weight-actions-alert-container">
        <ActionsBar ref={actionsBarRef}></ActionsBar>
        <Alert
          ref={alertRef}
          errorMessage={"Specified weights must add up to 100%"}
        ></Alert>
      </div> */}

      {/* <p>Weight type: {weightingType}</p>
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
      </ul> */}
    </div>
  );
};

export default Weight;
