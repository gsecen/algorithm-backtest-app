import { useRef } from "react";
import { Handle, Position, useReactFlow, useNodeId } from "@xyflow/react";
import {
  deleteNodeAndAllNodeChildren,
  deleteAllNodeChildren,
  copyNode,
} from "../../../utils/reactFlow";

const ActionsBar = ({ editMeFunction }) => {
  const { getNodes, getEdges, deleteElements, getNode, updateNodeData } =
    useReactFlow();
  const myId = useRef(useNodeId());

  function deleteNode() {
    deleteNodeAndAllNodeChildren(
      myId.current,
      getNodes(),
      getEdges(),
      deleteElements
    );
  }

  function deleteNodeChildren() {
    deleteAllNodeChildren(myId.current, getNodes(), getEdges(), deleteElements);
  }

  function copy() {
    const copiedNode = copyNode(myId.current, getNodes(), getEdges(), getNode);

    // Store copied node data in the root node of the react flow
    updateNodeData("1", {
      copiedNode: copiedNode,
    });
  }

  return (
    <div>
      <ul>
        <li>
          <button>edit me</button>
          <button onClick={deleteNode}>delete me</button>
          <button onClick={deleteNodeChildren}>delete children</button>
          <button onClick={copy}>copy me</button>
        </li>
      </ul>
    </div>
  );
};

export default ActionsBar;
