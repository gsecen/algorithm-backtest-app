import { useEffect, useRef, useState } from "react";
import { Handle, Position, useReactFlow, useNodeId } from "@xyflow/react";
import { createNode } from "../../../utils/reactFlow";
import "./expression.css";
import ActionsBar from "../ActionsBar/ActionsBar";
import Alert from "../../Alert/Alert";

const Expression = () => {
  const myId = useRef(useNodeId());
  const { getNode, getNodes, setNodes, addNodes, addEdges } = useReactFlow();

  const actionsBarRef = useRef();
  const alertRef = useRef();

  // For the expression function selector dropdown
  const [showFunctionDropdown, setShowFunctionDropdown] = useState(false);
  const [showFunctionSelectorDropdown, setShowFunctionSelectorDropdown] =
    useState(false);
  const [firstSelectedFunction, setFirstSelectedFunction] =
    useState("Choose Function");
  const [firstSelectedWindow, setFirstSelectedWindow] = useState(20);

  const FunctionSelectorDropdown = () => {
    return (
      <div
        className={`expression-function-dropdown-container ${
          showFunctionDropdown ? "" : "hidden"
        }`}
      >
        <p className="expression-function-dropdown-text">Function</p>
        <div className="expression-function-selector-dropdown-container">
          <div
            className="expression-function-selected"
            onClick={() => {
              setShowFunctionSelectorDropdown(!showFunctionSelectorDropdown);
            }}
          >
            {firstSelectedFunction}
          </div>
          <ul
            className={`expression-function-selector-dropdown ${
              showFunctionSelectorDropdown ? "" : "hidden"
            }`}
          >
            <li
              onClick={() => {
                setFirstSelectedFunction("Moving Average Of Price");
              }}
              className="expression-function-selector-dropdown-item"
            >
              Moving Average Of Price
            </li>
            <li
              onClick={() => {
                setFirstSelectedFunction("Moving Average Of Return");
              }}
              className="expression-function-selector-dropdown-item"
            >
              Moving Average Of Return
            </li>
            <li
              onClick={() => {
                setFirstSelectedFunction("Max Drawdown");
              }}
              className="expression-function-selector-dropdown-item"
            >
              Max Drawdown
            </li>
          </ul>
        </div>
        <p className="expression-function-dropdown-text">
          Window (# of trading days)
        </p>
        <input
          type="number"
          className="expression-function-trading-days-input"
          onChange={(event) => {
            setFirstSelectedWindow(event.target.value);
          }}
          value={firstSelectedWindow}
        />
      </div>
    );
  };

  // Add the true and false nodes to this expression on mount
  useEffect(() => {
    // Get current node details
    const myDetails = getNode(myId.current);

    // Create ids for true and false nodes which will be connected to current node (must be strings)
    const trueNodeId = `${Math.floor(Math.random() * 9999999)}`;
    const falseNodeId = `${Math.floor(Math.random() * 9999999)}`;

    // Create nodes and edges for nodes
    const trueNode = createNode(
      trueNodeId,
      "nodeSelector",
      myDetails.position.x + 100,
      myDetails.position.y + 100
    );
    const falseNode = createNode(
      falseNodeId,
      "nodeSelector",
      myDetails.position.x - 100,
      myDetails.position.y + 100
    );
    const trueEdge = {
      id: `${Math.floor(Math.random() * 9999999)}`,
      source: myId.current,
      target: trueNodeId,
      type: "true",
    };
    const falseEdge = {
      id: `${Math.floor(Math.random() * 9999999)}`,
      source: myId.current,
      target: falseNodeId,
      type: "false",
      animated: true,
    };

    // Add nodes and edges to react flow
    addNodes([trueNode, falseNode]);
    addEdges([trueEdge, falseEdge]);
  }, []);

  return (
    <div>
      <Handle type="target" position={Position.Top} />
      <div
        className="expression-container"
        onMouseEnter={() => {
          actionsBarRef.current.currentlyHovering();
        }}
        onMouseLeave={() => {
          actionsBarRef.current.notCurrentlyHovering();
        }}
      >
        <div className="expression-text-container">
          If the
          <span
            className="expression-text-edit-container"
            onClick={() => {
              setShowFunctionDropdown(!showFunctionDropdown);
            }}
          >
            {firstSelectedWindow}d {firstSelectedFunction}
          </span>
          {/* Function dropdown */}
          {/* <FunctionSelectorDropdown></FunctionSelectorDropdown> */}
          <div
            className={`expression-function-dropdown-container ${
              showFunctionDropdown ? "" : "hidden"
            }`}
          >
            <p className="expression-function-dropdown-text">Function</p>
            <div className="expression-function-selector-dropdown-container">
              <div
                className="expression-function-selected"
                onClick={() => {
                  setShowFunctionSelectorDropdown(
                    !showFunctionSelectorDropdown
                  );
                }}
              >
                {firstSelectedFunction}
              </div>
              <ul
                className={`expression-function-selector-dropdown ${
                  showFunctionSelectorDropdown ? "" : "hidden"
                }`}
              >
                <li
                  onClick={() => {
                    setFirstSelectedFunction("Moving Average Of Price");
                  }}
                  className="expression-function-selector-dropdown-item"
                >
                  Moving Average Of Price
                </li>
                <li
                  onClick={() => {
                    setFirstSelectedFunction("Moving Average Of Return");
                  }}
                  className="expression-function-selector-dropdown-item"
                >
                  Moving Average Of Return
                </li>
                <li
                  onClick={() => {
                    setFirstSelectedFunction("Max Drawdown");
                  }}
                  className="expression-function-selector-dropdown-item"
                >
                  Max Drawdown
                </li>
              </ul>
            </div>
            <p className="expression-function-dropdown-text">
              Window (# of trading days)
            </p>
            <input
              type="number"
              className="expression-function-trading-days-input"
              onChange={(event) => {
                setFirstSelectedWindow(event.target.value);
              }}
              value={firstSelectedWindow}
            />
          </div>
          of
          <span className="expression-text-edit-container">
            Yahoo Finance TSLA
          </span>
          is
          <span className="expression-text-edit-container">greater than</span>
          <span className="expression-text-edit-container">5%</span>
          of
          <span className="expression-text-edit-container">FRED FEDFUNDS</span>
        </div>
        <div className="expression-actions-alert-container">
          <ActionsBar
            ref={actionsBarRef}
            // editMeFunction={showWeightingTypeDropdown}
            // focused={showDropdown}
          ></ActionsBar>
          <Alert
            ref={alertRef}
            errorMessage={"Expression can have no empty inputs"}
          ></Alert>
        </div>
      </div>

      <Handle type="source" position={Position.Bottom} />
    </div>
  );
};

export default Expression;
