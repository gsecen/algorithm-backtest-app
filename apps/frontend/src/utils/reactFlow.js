// This file contains functions which help with the react flow nodes

import { getOutgoers, applyNodeChanges } from "@xyflow/react";

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
