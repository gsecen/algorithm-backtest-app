// This file contains functions which help with the react flow nodes
import { ReactFlow, useReactFlow } from "@xyflow/react";
import {
  getOutgoers,
  applyNodeChanges,
  applyEdgeChanges,
  getConnectedEdges,
} from "@xyflow/react";

/**
 * Gets all the immediate children of a node.
 * @param {string} id Id of the node you want to get children for.
 * @param {Array.<ReactFlowNode>} nodes List of all react flow nodes.
 * @param {Array.<ReactFlowEdge>} edges List of all react flow edges.
 * @returns {Array.<ReactFlowNode>} List of all immediate children from node.
 */
function getImmediateNodeChildren(id, nodes, edges) {
  // Gets all the nodes connected to node via the edges connected from the node source
  // https://reactflow.dev/api-reference/utils/get-outgoers
  return getOutgoers({ id: id }, nodes, edges);
}

/**
 * Gets all the children of a node.
 * @param {string} id Id of the node you want to get children for.
 * @param {Array.<ReactFlowNode>} nodes List of all react flow nodes.
 * @param {Array.<ReactFlowEdge>} edges List of all react flow edges.
 * @param {Array} children Empty array which will store nodes children.
 * @returns {Array.<ReactFlowNode>} List of all children from node.
 */
function getAllNodeChildren(id, nodes, edges, children = []) {
  // DFS function which adds all the nodes from the root node to children array
  // Same as DFS on a tree

  let immediateChildren = getImmediateNodeChildren(id, nodes, edges);

  immediateChildren.forEach((node) => children.push(node));

  immediateChildren.forEach((node) => {
    let nodeId = node.id;
    getAllNodeChildren(nodeId, nodes, edges, children);
  });

  return children;
}

/**
 * Deletes node and all of its children.
 * @param {string} id Id of the node you want to delete and delete all of its children.
 * @param {Array.<ReactFlowNode>} nodes List of all react flow nodes.
 * @param {Array.<ReactFlowEdge>} edges List of all react flow edges.
 * @param {function} deleteElementsFunction deleteElements method from useReactFlow hook.
 */
export const deleteNodeAndAllNodeChildren = (
  id,
  nodes,
  edges,
  deleteElementsFunction
) => {
  // Get all children of node
  const children = getAllNodeChildren(id, nodes, edges);

  // Add node to children array to be deleted
  children.push({ id: id });

  // Delete elements from the react flow
  // Will be the deleteElements method from useReactFlow hook to delete nodes from the react flow state
  // https://reactflow.dev/api-reference/types/react-flow-instance#deleteelements
  deleteElementsFunction({ nodes: children });
};

/**
 * Deletes all children of node.
 * @param {string} id Id of the node you want to delete all of its children.
 * @param {Array.<ReactFlowNode>} nodes List of all react flow nodes.
 * @param {Array.<ReactFlowEdge>} edges List of all react flow edges.
 * @param {function} deleteElementsFunction deleteElements method from useReactFlow hook.
 */
export const deleteAllNodeChildren = (
  id,
  nodes,
  edges,
  deleteElementsFunction
) => {
  // Get all children of node
  const children = getAllNodeChildren(id, nodes, edges);

  // Delete elements from the react flow
  // Will be the deleteElements method from useReactFlow hook to delete nodes from the react flow state
  // https://reactflow.dev/api-reference/types/react-flow-instance#deleteelements
  deleteElementsFunction({ nodes: children });
};

/**
 * Sets the hidden attribute in all the nodes children to true or false.
 * @param {boolean} hidden What you want the hidden attribute to be set to.
 * @param {string} id Id of the node you want to set hidden attribute in all of its children.
 * @param {Array.<ReactFlowNode>} nodes List of all react flow nodes.
 * @param {Array.<ReactFlowEdge>} edges List of all react flow edges.
 * @param {function} setNodesFunction setNodes method from useNodesState hook.
 */
export const setHiddenAllNodeChildren = (
  hidden,
  id,
  nodes,
  edges,
  setNodesFunction
) => {
  // Get all children of node
  const children = getAllNodeChildren(id, nodes, edges);

  // Set hidden property to true or false in all children nodes
  children.forEach((node) => {
    node.hidden = hidden;
  });

  // Applies the node changes to the nodes in nodes
  // https://reactflow.dev/api-reference/utils/apply-node-changes
  const newNodes = applyNodeChanges(children, nodes);

  // Updating the nodes in the react flow state
  setNodesFunction(newNodes);
};

export const createNode = (id, type, x, y, data = {}) => {
  return {
    id: id,
    type: type,
    position: { x: x, y: y },
    data: data,
    origin: [0.5, 0], // https://reactflow.dev/api-reference/types/node-origin
    // Origin is at the center top so when replacing nodes and positioning nodes it does it based off
    // of the handle at the top so there is no funny movement when replacing and modifying positions.
  };
};

/**
 * Changes the node type to the type specified.
 * @param {string} id Id of the node you want to change type for.
 * @param {string} type The type you want to change the node too.
 * @param {Array.<ReactFlowNode>} nodes List of all react flow nodes.
 * @param {function} getNodeFunction getNode method from useReactFlow hook.
 * @param {function} setNodesFunction setNodes method from useNodesState hook.
 */
export const changeNodeType = (
  id,
  type,
  nodes,
  getNodeFunction,
  setNodesFunction
) => {
  // Get old nodes details
  const oldNode = getNodeFunction(id);

  // New node should have same position and id as old node so edges stay connected and be in same position
  const newNode = createNode(id, type, oldNode.position.x, oldNode.position.y);

  const newNodes = applyNodeChanges(
    // https://reactflow.dev/api-reference/types/node-change#nodereplacechange
    [{ id: id, item: newNode, type: "replace" }],
    nodes
  );

  // Updating the nodes in the react flow state
  setNodesFunction(newNodes);
};

/**
 * Gets all the immediate edges of a node whos source is the node. (Gets immediate children edges)
 * @param {string} id Id of the node you want to get edges for.
 * @param {Array.<ReactFlowEdge>} edges List of all react flow edges.
 * @returns {Array.<ReactFlowEdge>} List of all immediate edges from node whos source is the node.
 */
export const getImmediateNodeSourceEdges = (id, edges) => {
  let nodeEdges = [];

  // Find all edges whos source is the target id
  edges.forEach((edge) => {
    if (edge.source === id) {
      nodeEdges.push(edge);
    }
  });

  return nodeEdges;
};

/**
 * Gets all the immediate edges of a node whos target is the node. (Gets immediate parent edges)
 * @param {string} id Id of the node you want to get edges for.
 * @param {Array.<ReactFlowEdge>} edges List of all react flow edges.
 * @returns {Array.<ReactFlowEdge>} List of all immediate edges to node whos target is the node.
 */
function getImmediateNodeTargetEdges(id, edges) {
  let nodeEdges = [];

  // Find all edges whos target is the target id
  edges.forEach((edge) => {
    if (edge.target === id) {
      nodeEdges.push(edge);
    }
  });

  return nodeEdges;
}

function createEdge(id, type, source, target, data = {}) {
  return {
    id: id,
    type: type,
    source: source,
    target: target,
    data: data,
  };
}

/**
 * Changes all the edges types to the type specified.
 * @param {string} type The type you want to change the edges too.
 * @param {Array.<ReactFlowEdge>} edges List of all react flow edges.
 * @param {Array.<ReactFlowEdge>} edgesToChange List edges that will be changed.
 * @param {function} setEdgesFunction setEdges method from useEdgesState hook.
 */
export const changeAllEdgeTypes = (
  type,
  edges,
  edgesToChange,
  setEdgesFunction
) => {
  let changes = [];

  // Copy all the same edge information to new edge just change the type
  edgesToChange.forEach((edge) => {
    let newEdge = createEdge(
      edge.id,
      type,
      edge.source,
      edge.target,
      edge.data
    );
    changes.push({ id: edge.id, item: newEdge, type: "replace" });
  });

  const newEdges = applyEdgeChanges(
    // https://reactflow.dev/api-reference/types/node-change#nodereplacechange
    changes,
    edges
  );

  setEdgesFunction(newEdges);
};

/**
 * Copies node, all children nodes, all children edges, and replaces all ids accordingly so everything is still connected.
 * @param {string} id Id of the node you want to copy everything for.
 * @param {Array.<ReactFlowNode>} nodes List of all react flow nodes.
 * @param {Array.<ReactFlowEdge>} edges List of all react flow edges.
 * @param {function} getNodeFunction getNode method from useReactFlow hook.
 * @param {Array} newNodes Empty array which will store new nodes.
 * @param {Array} newEdges Empty array which will store new edges.
 * @param {Object} newIds Empty object which will store old and new node ids.
 * @returns {[Array.<ReactFlowNode>, Array.<ReactFlowEdge>]} New id of root node, array of new nodes, array of new edges.
 */
export const copyNode = (
  id,
  nodes,
  edges,
  getNodeFunction,
  newNodes = [],
  newEdges = [],
  newIds = {}
) => {
  // Create new id which will be replacing nodes ids
  const newNodeId = `${Math.floor(Math.random() * 9999999)}`;

  // Get all node and edge details
  const immediateNodeChildren = getImmediateNodeChildren(id, nodes, edges);
  const immediateTargetEdges = getImmediateNodeTargetEdges(id, edges);

  // Get current nodes details
  const node = getNodeFunction(id);

  // Map old nodes id to what the new node is
  newIds[node.id] = newNodeId;

  // New node should have same position and data as old node with new id
  const newNode = createNode(
    newNodeId,
    node.type,
    node.position.x,
    node.position.y,
    node.data
  );

  newNodes.push(newNode);

  // For all the edges connected to the node change its target id to the new nodes id
  immediateTargetEdges.forEach((edge) => {
    const newEdgeId = `${Math.floor(Math.random() * 9999999)}`;

    // let source = edge.source;

    // If the source of the edge is a node whos id has been changed already, make edges source id the new nodes id
    // If the source of the edge has not been changed already, the edge is connected to root node so no need to add edge
    if (edge.source in newIds) {
      const source = newIds[edge.source];
      const newEdge = createEdge(
        newEdgeId,
        edge.type,
        source,
        newNodeId,
        edge.data
      );
      newEdges.push(newEdge);
    }
  });

  // For all of the children of node change its target edges accordingly
  immediateNodeChildren.forEach((node) => {
    copyNode(
      node.id,
      nodes,
      edges,
      getNodeFunction,
      newNodes,
      newEdges,
      newIds
    );
  });

  return [newNode.id, newNodes, newEdges];
};

export const pasteNode = (
  id,
  nodes,
  edges,
  rootNodeId,
  copiedNodes,
  copiedEdges,
  getNodeFunction,
  setNodesFunction,
  setEdgesFunction
) => {
  let nodeChanges = [];
  let edgeChanges = [];

  // Get details of the node you want to replace
  const nodeDetails = getNodeFunction(id);

  // Get the rootNode
  let rootNode = null;
  for (let i = 0; i < copiedNodes.length; i++) {
    if (copiedNodes[i].id === rootNodeId) {
      rootNode = copiedNodes[i];
      break;
    }
  }

  // console.log(nodeDetails);
  // console.log(rootNode);

  // Calculate x and y offsets needed to position rootNode in the node to be replaced position
  const xOffset = nodeDetails.position.x - rootNode.position.x;
  const yOffset = nodeDetails.position.y - rootNode.position.y;

  rootNode.position.x += xOffset;
  rootNode.position.y += yOffset;

  console.log("soido");
  console.log(rootNode);
  console.log(nodeDetails);
  nodeChanges.push({ id: nodeDetails.id, item: rootNode, type: "replace" });

  // For every copied node modify the position so the structure of the copied nodes stay the same,
  // and so that their root node will be in the spot of the node to be replaced
  copiedNodes.forEach((node) => {
    // Make sure not to add root node becuase it has already been added to react flow through replace change
    if (node.id !== rootNodeId) {
      node.position.x += xOffset;
      node.position.y += yOffset;
      nodeChanges.push({ item: node, type: "add" });
    }
  });

  // Get the edges whos target is the node to be replaced
  const targetEdges = getImmediateNodeTargetEdges(nodeDetails.id, edges);

  // Change the target id of the target edges to the new rootNodes id
  targetEdges.forEach((edge) => {
    const newEdge = createEdge(
      edge.id,
      edge.type,
      edge.source,
      rootNode.id,
      edge.data
    );
    edgeChanges.push({ id: edge.id, item: newEdge, type: "replace" });
  });

  // Build all changes to add edges
  copiedEdges.forEach((edge) => {
    edgeChanges.push({ item: edge, type: "add" });
  });

  // Apply changes and update react flow state
  const newNodes = applyNodeChanges(nodeChanges, nodes);
  const newEdges = applyEdgeChanges(edgeChanges, edges);

  setNodesFunction(newNodes);
  setEdgesFunction(newEdges);
};
