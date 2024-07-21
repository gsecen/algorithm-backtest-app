// This file contains functions which help with the react flow nodes

import { getOutgoers } from "@xyflow/react";

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
