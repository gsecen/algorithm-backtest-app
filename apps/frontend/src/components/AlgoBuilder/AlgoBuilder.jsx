import React, { useCallback, useMemo, useState, useRef } from "react";
import {
  ReactFlow,
  MiniMap,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  addEdge,
  applyNodeChanges,
  useReactFlow,
  getIncomers,
  getOutgoers,
} from "@xyflow/react";

import "@xyflow/react/dist/style.css";
import TestNode from "./TestNode/TestNode";
import NodeSelector from "./NodeSelector/NodeSelector";
import Buy from "./Buy/Buy";
import Expression from "./Expression/Expression";
import Weight from "./Weight/Weight";

import True from "./edges/True/True";
import False from "./edges/False/False";
import SpecifiedWeight from "./edges/SpecifiedWeight/SpecifiedWeight";

import {
  deleteNodeAndAllNodeChildren,
  setHiddenAllNodeChildren,
  changeNodeType,
  copyNode,
} from "../../utils/reactFlow";

const nodeTypes = {
  weight: Weight,
  testNode: TestNode,
  buy: Buy,
  nodeSelector: NodeSelector,
  expression: Expression,
};

const edgeTypes = {
  true: True,
  false: False,
  specifiedWeight: SpecifiedWeight,
};

// How we are going to build the request is by starting at the root node
// and recursively getting its children and childrens children by using the
//  getOutgoers() function to check what nodes are connected
// https://reactflow.dev/api-reference/utils/get-outgoers
// think of it as dfs a tree the nodes are the nodes and the edges are the edges
// just like a tree

// when deleteing a node check if it has children and delete them aswell

// to hide nodes simply hide parent and hide all children aswell

// to copy nodes get node and all of its children and change the id of all the
// the nodes. Then when pasting the nodes, add the new node with children with all
// different ids to new parent node
// we also need to get the edges connecting those nodes and edit the targets and stuff

// https://reactflow.dev/api-reference/types/node-change#nodeaddchange
// this can replace nodes

// Relying on useNodes unecessarily can be a common cause of performance issues. Whenever any node changes, this hook will cause the component to re-render. Often we actually care about something more specific, like when the number of nodes changes: where possible try to use useStore instead.

// we can use the usereactflow hook to query data about our flow state without our nodes rerendering!

const AlgoBuilder = () => {
  const [test, setTest] = useState(0);

  const tester = {
    id: "node-1",
    type: "testNode",
    position: { x: 0, y: 0 },
    data: { value: 123, showParentChildren: showParentChildrenFunction },
  };

  const initialNodes = [
    {
      id: "1",
      position: { x: 0, y: 0 },
      data: { label: "1" },
      origin: [0.5, 0.5],
    },
    {
      id: "2",
      position: { x: 0, y: 100 },
      origin: [0.5, 0.5],
      data: { label: "2" },
    },

    // { id: "3", type: "buy", position: { x: 0, y: 200 }, data: {} },
    // { id: "4", type: "nodeSelector", position: { x: 0, y: 300 }, data: {} },
    // { id: "5", type: "expression", position: { x: 0, y: 500 }, data: {} },
  ];

  function showParentChildrenFunction() {
    console.log(nodes);
  }

  const initialEdges = [
    { id: "e1-2", source: "1", target: "2", data: { copiedData: [] } },
  ];

  const [elements, setElements] = useState(initialNodes);

  const [nodes, setNodes, onNodesChange] = useNodesState(elements);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);
  const connectingNodeId = useRef(null);
  const connectingNode = useRef(null);
  const reactFlowWrapper = useRef(null);

  const { screenToFlowPosition, deleteElements, getNode } = useReactFlow();

  const buy = {
    id: "12345",
    type: "buy",
    position: { x: 100, y: 100 },
    data: { setter: setNodes },
  };

  function printNodes() {
    console.log(nodes);
  }

  function addNode() {
    const random = Math.floor(Math.random() * 9999999);
    const newNode = {
      id: `${random}`,
      position: { x: 0, y: 0 },
      data: { label: random, setter: printNodes },
      type: "buy",
    };

    setNodes([...nodes, newNode]);
  }

  // function removeNode() {
  //   const tt = applyNodeChanges(
  //     //https://reactflow.dev/api-reference/types/node-change
  //     [{ type: "remove", id: "1" }],
  //     nodes
  //   );

  //   setNodes(tt);
  // }

  function testRemove() {
    deleteElements({ nodes: [{ id: "1" }, { id: "2" }] });
  }

  function animate() {
    const tt = applyNodeChanges(
      //https://reactflow.dev/api-reference/types/node-change
      [
        { type: "position", id: "1", position: { x: 100, y: 100 } },
        { type: "position", id: "2", position: { x: 50, y: 50 } },
      ],
      nodes
    );

    setNodes(tt);
  }

  function changeLabel() {
    setNodes((nds) =>
      nds.map((node) => {
        if (node.id === "1") {
          // it's important that you create a new node object
          // in order to notify react flow about the change
          return {
            ...node,
            data: {
              ...node.data,
              label: "cat",
            },
          };
        }

        return node;
      })
    );
  }
  // console.log("rendered");

  const onConnect = useCallback(
    (params) => setEdges((eds) => addEdge(params, eds)),
    [setEdges]
  );

  function showNodes() {
    console.log(getOutgoers({ id: "2" }, nodes, edges));
    console.log(nodes);
  }

  const onConnectStart = useCallback((_, { nodeId }) => {
    // connectingNodeId.current = nodeId;
    // console.log(_);
    // console.log(_.srcElement.dataset);
    // console.log(_);
    // console.log(nodeId);

    connectingNode.current = getNode(nodeId);
    // console.log(connectingNode);
  }, []);

  const onConnectEnd = useCallback(
    (event) => {
      // console.log(event);
      // if (!connectingNodeId.current) return;
      if (!connectingNode.current.id) return;
      const targetIsPane = event.target.classList.contains("react-flow__pane");
      if (targetIsPane) {
        // we need to remove the wrapper bounds, in order to get the correct position
        const id = String(Math.floor(Math.random() * 10000000));
        const newNode = {
          id,
          position: screenToFlowPosition({
            x: event.clientX,
            y: event.clientY,
          }),
          data: {},
          origin: [0.5, 0.0],
          type: "nodeSelector",
        };
        setNodes((nds) => nds.concat(newNode));

        // Check to see if node connecting from is a weight node
        if (connectingNode.current.type === "weight") {
          // Check to see if weighting type is currently specified
          if (connectingNode.current.data.weightingType === "specifiedWeight") {
            // Add the specfied weight node
            setEdges((eds) =>
              eds.concat({
                id,
                source: connectingNode.current.id,
                target: id,
                type: "specifiedWeight",
              })
            );
          } else {
            setEdges((eds) =>
              eds.concat({ id, source: connectingNode.current.id, target: id })
            );
          }
        } else {
          setEdges((eds) =>
            eds.concat({ id, source: connectingNode.current.id, target: id })
          );
        }
      }
      // console.log(event);
    },
    [screenToFlowPosition]
  );

  function getAllNodeChilds() {
    // console.log(getAllNodeChildren("2", nodes, edges));
  }

  function deleteNodeAndChildren() {
    deleteNodeAndAllNodeChildren("2", nodes, edges, deleteElements);
  }

  function hideNode2() {
    setHiddenAllNodeChildren(true, "2", nodes, edges, setNodes);
  }
  function unhideNode2() {
    setHiddenAllNodeChildren(false, "2", nodes, edges, setNodes);
  }
  function replaceNode2() {
    changeNodeType("2", "buy", nodes, getNode, setNodes);
    console.log("replacing");
  }

  function copyNode2() {
    console.log(copyNode("2", nodes, edges, getNode));
  }

  return (
    <div
      className="wrapper"
      ref={reactFlowWrapper}
      style={{ width: "100vw", height: "100vh" }}
    >
      <button onClick={animate}>animate</button>
      <button onClick={showNodes}>show nodes</button>
      <button onClick={addNode}>add new node</button>
      <button onClick={changeLabel}>change node label</button>
      <button onClick={testRemove}>remove node</button>
      <button onClick={getAllNodeChilds}>get all node children</button>
      <button onClick={copyNode2}>copy node 2 show in console</button>
      <button onClick={deleteNodeAndChildren}>
        delete node and all node childrne
      </button>
      <button onClick={hideNode2}>make id 2 node hiddden</button>
      <button onClick={unhideNode2}>make id 2 node unhiddden</button>
      <button onClick={replaceNode2}>replace node 2</button>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        onConnectStart={onConnectStart}
        onConnectEnd={onConnectEnd}
        nodeTypes={nodeTypes}
        edgeTypes={edgeTypes}
        onNodesDelete={(event) => {
          console.log(event);
        }}
        copiednode={"d"}
      >
        <Controls />
        <MiniMap />
        <Background variant="dots" gap={12} size={1} />
      </ReactFlow>
    </div>
  );
};

export default AlgoBuilder;
