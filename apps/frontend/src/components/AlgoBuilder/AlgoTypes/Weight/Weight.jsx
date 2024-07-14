import React, { useState } from "react";
import "./weight.css";
import Buy from "../Buy/Buy";
import TypeSelector from "../../TypeSelector/TypeSelector";
import SpecifiedWeight from "../SpecifiedWeight/SpecifiedWeight";
import WeightSelector from "../WeightSelector/WeightSelector";
import {
  spliceListById,
  spliceListsByIdAtSameIndex,
} from "../../../../utils/instructions";
import {
  createBuyComponent,
  cloneBuyComponent,
  updateBuyComponentTicker,
} from "../../../../utils/buy";

import {
  createSpecifiedWeightComponent,
  buildSpecifiedWeights,
  cloneSpecifiedWeightComponent,
  updateSpecifiedWeightComponentWeight,
  deleteSpecifiedWeightAndChildById,
} from "../../../../utils/specifiedWeight";

const Weight = () => {
  // Will hold child tasks
  const [tasks, setTasks] = useState([]);

  // Will hold the specified weights
  const [specifiedWeights, setSpecifiedWeights] = useState([]);

  // Will hold the weighting type (equal, or specified)
  const [weighting, setWeighting] = useState("Equal");

  // Will hold toggle to add and remove type selector menu
  const [typeSelectToggle, setTypeSelectorToggle] = useState(false);

  // Will hold algo builder components which can be added to algo
  const AlgoComponents = {
    Buy: <Buy></Buy>,
  };

  function deleteChildById(id) {
    // // Searching for child with id
    // tasks.forEach((item, index) => {
    //   if (item.props.id === id) {
    //     // Remove child from tasks
    //     tasks.splice(index, 1);
    //   }
    // });
    // const newTasks = [...tasks];
    // setTasks(newTasks);
    // setTasks(deleteItemById(id, [...tasks]));
  }

  function showChildre() {
    console.log(tasks);
  }
  function showWeights() {
    console.log(specifiedWeights);
  }

  function addBuy() {
    // const randomNumber = Math.floor(Math.random() * 99999);
    // const newComponent = (
    //   <Buy id={randomNumber} deleteMe={deleteChildById} ticker={"TICKER"}></Buy>
    // );

    if (weighting === "Specified") {
      addNewSpecifiedWeight();
    }

    const Component = createBuyComponent(deleteChildById, changeTickerSymbol);
    setTasks([...tasks, Component]);
  }

  function changeSpecifiedWeight(id, newWeight) {
    // Finding child with id
    // specifiedWeights.forEach((item, index) => {
    //   if (item.props.id === id) {
    //     // Replace type specified weight with new type specified weight with updated weight
    //     const id = item.props.id;
    //     const specifiedWeight = newWeight;
    //     const Component = React.cloneElement(
    //       <SpecifiedWeight></SpecifiedWeight>,
    //       {
    //         id: id,
    //         key: id,
    //         specifiedWeight: specifiedWeight,
    //         deleteMe: deleteSpecifiedWeightById,
    //         updateSpecifiedWeight: changeSpecifiedWeight,
    //       }
    //     );

    //     // const Component = cloneSpecifiedWeightComponent(
    //     //   item,
    //     //   deleteSpecifiedWeightById,
    //     //   changeSpecifiedWeight
    //     // );

    //     specifiedWeights[index] = Component;
    //   }
    // });
    const updatedSpecifiedWeights = updateSpecifiedWeightComponentWeight(
      id,
      newWeight,
      specifiedWeights,
      deleteSpecifiedWeightById,
      changeSpecifiedWeight
    );
    setSpecifiedWeights([...updatedSpecifiedWeights]);
    // const newSpecifiedWeights = [...specifiedWeights];
    // setSpecifiedWeights(newSpecifiedWeights);
  }

  function changeTickerSymbol(id, newTickerSymbol) {
    // // Finding child with id
    // tasks.forEach((item, index) => {
    //   if (item.props.id === id) {
    //     // Replace type buy with new type buy with updated ticker symbol name
    //     const id = item.props.id;
    //     const tickerSymbol = newTickerSymbol;
    //     const Component = React.cloneElement(<Buy></Buy>, {
    //       id: id,
    //       ticker: tickerSymbol,
    //       deleteMe: deleteChildById,
    //       updateTickerSymbol: changeTickerSymbol,
    //     });

    //     // const Component = cloneBuyComponent(
    //     //   item,
    //     //   deleteChildById,
    //     //   changeTickerSymbol
    //     // );

    //     tasks[index] = Component;
    //   }
    // });
    // const newTasks = [...tasks];
    // setTasks(newTasks);

    const updatedTasks = updateBuyComponentTicker(
      id,
      newTickerSymbol,
      [...tasks],
      deleteChildById,
      changeTickerSymbol
    );

    setTasks(updatedTasks);
  }

  function addTypeSelector() {
    setTypeSelectorToggle(!typeSelectToggle);
  }
  function removeTypeSelector() {
    setTypeSelectorToggle(false);
  }

  function deleteSpecifiedWeightById(id) {
    // // Removing the specified weight from specified weights and its corresponding task from tasks
    // specifiedWeights.forEach((item, index) => {
    //   if (item.props.id === id) {
    //     // Remove specified weight from specified weights
    //     specifiedWeights.splice(index, 1);
    //     // Removing the weights corresponding task from tasks
    //     tasks.splice(index, 1);
    //   }
    // });

    // const newTasks = [...tasks];
    // setTasks(newTasks);

    // const newSpecifiedWeights = [...specifiedWeights];
    // setSpecifiedWeights(newSpecifiedWeights);

    const newDetails = spliceListsByIdAtSameIndex(id, specifiedWeights, tasks);

    console.log(newDetails);

    const newTasks = newDetails[1];
    const newWeights = newDetails[0];

    setTasks([...newTasks]);
    setSpecifiedWeights([...newWeights]);
  }

  function addNewSpecifiedWeight() {
    // const randomNumber = Math.floor(Math.random() * 99999);
    // const Component = (
    //   <SpecifiedWeight
    //     id={randomNumber}
    //     key={randomNumber}
    //     deleteMe={deleteSpecifiedWeightById}
    //     specifiedWeight={"Set Weight"}
    //     updateSpecifiedWeight={changeSpecifiedWeight}
    //   ></SpecifiedWeight>
    // );
    // specifiedWeights.push(Component);

    // const newSpecifiedWeights = [...specifiedWeights];
    const Component = createSpecifiedWeightComponent(
      deleteSpecifiedWeightById,
      changeSpecifiedWeight
    );
    setSpecifiedWeights([...specifiedWeights, Component]);
  }

  function buildSpecifiedWeights2() {
    // For each task we must add a specified weight to it
    // tasks.forEach((item, index) => {
    //   const randomNumber = Math.floor(Math.random() * 99999);
    //   const Component = (
    //     <SpecifiedWeight
    //       id={randomNumber}
    //       key={randomNumber}
    //       deleteMe={deleteSpecifiedWeightById}
    //       specifiedWeight={"Set Weight"}
    //       updateSpecifiedWeight={changeSpecifiedWeight}
    //     ></SpecifiedWeight>
    //   );
    //   specifiedWeights.push(Component);
    // });

    // const newSpecifiedWeights = [...specifiedWeights];
    // setSpecifiedWeights(newSpecifiedWeights);

    let specifiedWeights = buildSpecifiedWeights(
      tasks,
      deleteSpecifiedWeightById,
      changeSpecifiedWeight
    );

    setSpecifiedWeights([...specifiedWeights]);
  }

  function changeWeight() {
    setWeighting("Specified");
    buildSpecifiedWeights2();
  }

  function changeWeighting(type) {
    setWeighting(type);

    // Make sure weighting is not already specified
    if (weighting !== "Specified") {
      // Add specified weights to all tasks
      buildSpecifiedWeights2();
    }
  }

  function renderWeightidk(index) {
    const item = specifiedWeights[index];
    const id = item.props.id;
    const specifiedWeight = item.props.specifiedWeight;
    const Component = React.cloneElement(<SpecifiedWeight></SpecifiedWeight>, {
      key: id,
      id: id,
      specifiedWeight: specifiedWeight,
      deleteMe: deleteSpecifiedWeightById,
      updateSpecifiedWeight: changeSpecifiedWeight,
    });

    return Component;
  }

  const TypeSelectorComponent = <TypeSelector addBuy={addBuy}></TypeSelector>;

  return (
    <div>
      <button onClick={addTypeSelector}>toggle type selector</button>
      <WeightSelector changeWeighting={changeWeighting}></WeightSelector>
      <ul>
        {tasks.map((item, index) => {
          // Doing this becuase components will be stored in tasks array so props and functions
          // need to be passed down with updated data. This is done by cloning element with updated props.
          const id = item.props.id;
          const name = item.type.name;
          const ticker = item.props.ticker;
          // const Component = React.cloneElement(AlgoComponents[name], {
          //   key: id,
          //   id: id,
          //   ticker: ticker,
          //   deleteMe: deleteChildById,
          //   updateTickerSymbol: changeTickerSymbol,
          // });
          const Component = cloneBuyComponent(
            item,
            deleteChildById,
            changeTickerSymbol
          );

          return (
            <li>
              {weighting === "Equal" ? null : renderWeightidk(index)}
              <ul>
                <li key={index}>{Component}</li>
              </ul>
            </li>
          );
        })}
      </ul>
      {TypeSelectorComponent}
      <button onClick={showChildre}>show children</button>
      <button onClick={showWeights}>show weights</button>
      <button onClick={changeWeight}>change weight to specified</button>
    </div>
  );
};

export default Weight;
