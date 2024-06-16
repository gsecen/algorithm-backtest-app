import React, { useState } from "react";
import "./startInstructions.css";

import TypeSelector from "../../TypeSelector/TypeSelector";
import Buy from "../Buy/Buy";
import { list } from "tar";

const StartInstructions = () => {
  // Will hold child tasks
  const [tasks, setTasks] = useState([]);

  // Will hold algo builder components which can be added to algo
  const AlgoComponents = {
    Buy: <Buy></Buy>,
  };

  function addBuy() {
    const randomNumber = Math.floor(Math.random() * 99999);
    const newComponent = <Buy key={randomNumber} id={randomNumber}></Buy>;

    setTasks([...tasks, newComponent]);
  }

  function showTypeSelector() {}
  function removeTypeSelector() {}

  return (
    <div>
      <ul>
        {tasks.map((item, index) => {
          // Doing this becuase components will be stored in tasks array so props and functions
          // need to be passed down with updated data. This is done by cloning element with updated props.
          const id = item.props.id;
          const name = item.type.name;
          const Component = React.cloneElement(AlgoComponents[name], {
            key: index,
            id: id,
          });

          return <li>{Component}</li>;
        })}
      </ul>
    </div>
  );
};

export default StartInstructions;
