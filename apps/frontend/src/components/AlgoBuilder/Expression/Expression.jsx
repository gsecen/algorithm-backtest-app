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

  // For the comparator selector dropdown
  const [showComparatorDropdown, setShowComparatorDropdown] = useState(false);
  const [selectedComparator, setSelectedComparator] =
    useState("Set Comparator");

  // For asset/fred selector dropdown
  const [showDataAssetDropdown, setShowDataAssetDropdown] = useState(true);
  const [firstSelectedDataAssetType, setFirstSelectedDataAssetType] =
    useState("Type");
  const [firstSelectedDataAsset, setFirstSelectedDataAsset] =
    useState("Asset/Data");

  // Function gets what to put in the placeholder for asset or series id input
  function getFirstSelectedDataAssetPlaceholder() {
    if (firstSelectedDataAssetType === "Type") {
      return "Ticker / Series Id";
    }
    if (firstSelectedDataAssetType === "Yahoo Finance") {
      return "TICKER";
    }
    if (firstSelectedDataAssetType === "FRED") {
      return "SERIES ID";
    }
  }

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
          <div className="expression-function-container">
            <span
              className="expression-text-edit-container"
              onClick={() => {
                setShowFunctionDropdown(!showFunctionDropdown);
              }}
            >
              {firstSelectedWindow}d {firstSelectedFunction}
            </span>
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
                      setShowFunctionSelectorDropdown(false);
                    }}
                    className="expression-function-selector-dropdown-item"
                  >
                    Moving Average Of Price
                  </li>
                  <li
                    onClick={() => {
                      setFirstSelectedFunction("Moving Average Of Return");
                      setShowFunctionSelectorDropdown(false);
                    }}
                    className="expression-function-selector-dropdown-item"
                  >
                    Moving Average Of Return
                  </li>
                  <li
                    onClick={() => {
                      setFirstSelectedFunction("Max Drawdown");
                      setShowFunctionSelectorDropdown(false);
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
                  if (event.target.value === "") {
                    setFirstSelectedWindow("");
                  }
                  // Make sure value is not a float
                  else {
                    setFirstSelectedWindow(Math.ceil(event.target.value));
                  }
                }}
                onBlur={(event) => {
                  // Make sure value is not empty
                  if (event.target.value === "") {
                    setFirstSelectedWindow(20);
                  }
                }}
                value={firstSelectedWindow}
              />
            </div>
          </div>
          of
          <div className="expression-asset-data-container">
            <span className="expression-text-edit-container">
              {firstSelectedDataAssetType} {firstSelectedDataAsset}
            </span>
            <div
              className={`expression-function-dropdown-container ${
                showFunctionDropdown ? "" : "hidden"
              }`}
            >
              <p className="expression-function-dropdown-text">Type</p>
              <div className="expression-function-selector-dropdown-container">
                <div
                  className="expression-function-selected"
                  onClick={() => {
                    setShowFunctionSelectorDropdown(
                      !showFunctionSelectorDropdown
                    );
                  }}
                >
                  {firstSelectedDataAssetType}
                </div>
                <ul
                  className={`expression-function-selector-dropdown ${
                    showFunctionSelectorDropdown ? "" : "hidden"
                  }`}
                >
                  <li
                    onClick={() => {
                      setFirstSelectedDataAssetType("Yahoo Finance");
                      setShowFunctionSelectorDropdown(false);
                    }}
                    className="expression-function-selector-dropdown-item"
                  >
                    Yahoo Finance
                  </li>
                  <li
                    onClick={() => {
                      setFirstSelectedDataAssetType("FRED");
                      setShowFunctionSelectorDropdown(false);
                    }}
                    className="expression-function-selector-dropdown-item"
                  >
                    FRED (St. Louis FED)
                  </li>
                </ul>
              </div>
              <p className="expression-function-dropdown-text">
                {getFirstSelectedDataAssetPlaceholder()}
              </p>
              <input
                type="text"
                className="expression-function-trading-days-input"
                onChange={(event) => {
                  setFirstSelectedDataAsset(event.target.value);
                }}
                placeholder={getFirstSelectedDataAssetPlaceholder()}
              />
            </div>
          </div>
          is
          <div className="expression-comparator-container">
            <span
              onClick={() => {
                setShowComparatorDropdown(!showComparatorDropdown);
              }}
              className="expression-text-edit-container"
            >
              {selectedComparator}
            </span>
            <div
              className={`expression-comparator-dropdown-container ${
                showComparatorDropdown ? "" : "hidden"
              }`}
            >
              <ul className="expression-comparator-dropdown">
                <li
                  onClick={() => {
                    setSelectedComparator("less than");
                  }}
                  className="expression-comparator-dropdown-item"
                >
                  less than
                </li>
                <li
                  onClick={() => {
                    setSelectedComparator("greater than");
                  }}
                  className="expression-comparator-dropdown-item"
                >
                  greater than
                </li>
                <li
                  onClick={() => {
                    setSelectedComparator("equal to");
                  }}
                  className="expression-comparator-dropdown-item"
                >
                  equal to
                </li>
              </ul>
            </div>
          </div>
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
