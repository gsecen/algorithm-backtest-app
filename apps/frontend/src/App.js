import AlgoBuilder from "./components/AlgoBuilder/AlgoBuilder";
import "./app.css";

// Like useContext for the react flow
// https://reactflow.dev/api-reference/react-flow-provider
import { ReactFlowProvider } from "@xyflow/react";

function App() {
  return (
    <div>
      <ReactFlowProvider>
        <AlgoBuilder></AlgoBuilder>
      </ReactFlowProvider>
    </div>
  );
}

export default App;
