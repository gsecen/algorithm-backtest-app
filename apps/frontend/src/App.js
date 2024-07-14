import "./appVars.css";
import AlgoBuilder from "./components/AlgoBuilder/AlgoBuilder";
import Exclamtion from "./components/Exclamation/Exclamtion";
import Buy from "./components/AlgoBuilder/AlgoTypes/Buy/Buy";
import EditDelete from "./components/AlgoBuilder/EditDelete/EditDelete";
import Weight from "./components/AlgoBuilder/AlgoTypes/Weight/Weight";
import SpecifiedWeight from "./components/AlgoBuilder/AlgoTypes/SpecifiedWeight/SpecifiedWeight";
import ClassTest from "./components/AlgoBuilder/ClassTest/ClassTest";
import ActionsBar from "./components/AlgoBuilder/ActionsBar/ActionsBar";
import Instructions from "./components/AlgoBuilder/AlgoTypes/Instructions/Instructions";
import { useRef } from "react";

function App() {
  // const myRef = useRef();

  // function printmyref() {
  //   console.log(myRef.current.currentlyHovering());
  // }
  return (
    <div className="app">
      {/* <AlgoBuilder></AlgoBuilder> */}
      {/* <Exclamtion errorMessage={"You must enter a ticker symbol"}></Exclamtion> */}
      {/* <Buy></Buy> */}
      {/* <EditDelete></EditDelete> */}

      {/* <Weight></Weight> */}
      <Instructions></Instructions>
      {/* <ActionsBar ref={myRef}></ActionsBar> */}
      {/* <ClassTest ref={myRef}></ClassTest> */}
      {/* <button onClick={printmyref}>1</button> */}

      {/* <SpecifiedWeight></SpecifiedWeight> */}
    </div>
  );
}

export default App;
