import React, { useState } from "react";
import "./startInstructions.css";

import TypeSelector from "../../TypeSelector/TypeSelector";
import Buy from "../Buy/Buy";

const StartInstructions = () => {
  // Will hold child tasks
  const [tasks, setTasks] = useState([]);

  // Will hold toggle to add and remove type selector menu
  const [typeSelectToggle, setTypeSelectorToggle] = useState(false);

  // Will hold algo builder components which can be added to algo
  const AlgoComponents = {
    Buy: <Buy></Buy>,
  };

  /**
   *
   * @param {*} id
   */
  function deleteChildById(id) {
    // Searching for child with id
    tasks.forEach((item, index) => {
      if (item.props.id === id) {
        // Remove child from tasks
        tasks.splice(index, 1);
      }
    });
    const newList = [...tasks];
    setTasks(newList);
  }

  function showChildre() {
    console.log(tasks);
  }

  function addBuy() {
    const randomNumber = Math.floor(Math.random() * 99999);
    const newComponent = (
      <Buy
        id={randomNumber}
        deleteMe={deleteChildById}
        tickerSymbol={"TICKER"}
      ></Buy>
    );

    setTasks([...tasks, newComponent]);
  }

  function changeTickerSymbol(id, newTickerSymbol) {
    // Finding child with id
    tasks.forEach((item, index) => {
      if (item.props.id === id) {
        // Replace type buy with new type buy with updated ticker symbol name
        const id = item.props.id;
        const tickerSymbol = newTickerSymbol;
        const Component = React.cloneElement(<Buy></Buy>, {
          id: id,
          tickerSymbol: tickerSymbol,
          deleteMe: deleteChildById,
          updateTickerSymbol: changeTickerSymbol,
        });

        tasks[index] = Component;
      }
    });
    const newList = [...tasks];
    setTasks(newList);
  }

  function addTypeSelector() {
    setTypeSelectorToggle(!typeSelectToggle);
  }
  function removeTypeSelector() {
    setTypeSelectorToggle(false);
  }

  const TypeSelectorComponent = <TypeSelector addBuy={addBuy}></TypeSelector>;

  return (
    <div>
      <button onClick={addTypeSelector}>toggle type selector</button>
      <ul>
        {tasks.map((item, index) => {
          // Doing this becuase components will be stored in tasks array so props and functions
          // need to be passed down with updated data. This is done by cloning element with updated props.
          const id = item.props.id;
          const name = item.type.name;
          const ticker = item.props.tickerSymbol;
          const Component = React.cloneElement(AlgoComponents[name], {
            id: id,
            tickerSymbol: ticker,
            deleteMe: deleteChildById,
            updateTickerSymbol: changeTickerSymbol,
          });

          return <li key={id}>{Component}</li>;
        })}
      </ul>
      {typeSelectToggle ? TypeSelectorComponent : <div>yes</div>}
      <button onClick={showChildre}>show children</button>
    </div>
  );
};

export default StartInstructions;
