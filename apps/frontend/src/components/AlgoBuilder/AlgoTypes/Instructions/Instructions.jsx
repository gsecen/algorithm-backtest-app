import { useState } from "react";

import {
  spliceListById,
  spliceListsByIdAtSameIndex,
} from "../../../../utils/instructions";

import WeightSelector from "../WeightSelector/WeightSelector";
import {
  buildSpecifiedWeights,
  createSpecifiedWeightComponent,
  updateSpecifiedWeightComponentWeight,
  cloneSpecifiedWeightComponent,
  doSpecifiedWeightsAddTo100,
} from "../../../../utils/specifiedWeight";

import {
  cloneBuyComponent,
  createBuyComponent,
  updateBuyComponentTicker,
} from "../../../../utils/buy";

const Instructions = () => {
  // Will hold all child algo type components
  const [tasks, setTasks] = useState([]);

  // Will hold the weighting type
  const [weightingType, setWeightingType] = useState("Equal");

  // Will hold specified weight components if weighting type is set to specified
  const [specifiedWeights, setSpecifiedWeights] = useState([]);

  // Logic to display if there is an error with specified weights (if they dont add up to 100%)
  let error = false;
  if (weightingType === "Specified") {
    if (!doSpecifiedWeightsAddTo100(specifiedWeights)) {
      error = true;
    }
  }

  function showChildren() {
    console.log(tasks);
    console.log(specifiedWeights);
  }

  // Function deletes a child component
  function deleteTaskById(id) {
    // If weighting type is equal only need to remove the 1 task
    if (weightingType === "Equal") {
      setTasks(spliceListById(id, [...tasks]));
    }

    // If weighting is specified must remove task and corresponding specified weight
    if (weightingType === "Specified") {
      const newTasksAndWeights = spliceListsByIdAtSameIndex(
        id,
        [...tasks],
        [...specifiedWeights]
      );

      const newTasks = newTasksAndWeights[0];
      const newWeights = newTasksAndWeights[1];

      setTasks(newTasks);
      setSpecifiedWeights(newWeights);
    }
  }

  // Function deletes specified weight and the specified weights child
  function deleteSpecifiedWeightById(id) {
    const newTasksAndWeights = spliceListsByIdAtSameIndex(
      id,
      [...specifiedWeights],
      [...tasks]
    );

    const newWeights = newTasksAndWeights[0];
    const newTasks = newTasksAndWeights[1];

    setTasks(newTasks);
    setSpecifiedWeights(newWeights);
  }

  // Function will update specified weight with id
  function updateSpecifiedWeight(id, newWeight) {
    const updatedWeights = updateSpecifiedWeightComponentWeight(
      id,
      newWeight,
      [...specifiedWeights],
      deleteSpecifiedWeightById,
      updateSpecifiedWeight
    );

    setSpecifiedWeights(updatedWeights);
  }

  // Function will add a new specified weight to specified weights if weighting type is set to specified
  function addSpecifiedWeight() {
    if (weightingType === "Specified") {
      const Component = createSpecifiedWeightComponent(
        deleteSpecifiedWeightById,
        updateSpecifiedWeight
      );

      setSpecifiedWeights([...specifiedWeights, Component]);
    }
  }

  // Function adds a specific weight for every task in tasks
  function addSpecificWeightsForTasks() {
    const weightsForTasks = buildSpecifiedWeights(
      [...tasks],
      deleteSpecifiedWeightById,
      updateSpecifiedWeight
    );

    setSpecifiedWeights(weightsForTasks);
  }

  // Function changes the weighting type
  function changeWeightingType(type) {
    // If weight was set to something else and is now set to specified
    if (weightingType !== "Specified" && type === "Specified") {
      // add specified weights for every task
      addSpecificWeightsForTasks();
    }

    // If the weighting type is changed to Equal remove all specifed weights
    if (type === "Equal") {
      setSpecifiedWeights([]);
    }

    setWeightingType(type);
  }

  function updateBuyTickerSymbol(id, newTickerSymbol) {
    const updatedTasks = updateBuyComponentTicker(
      id,
      newTickerSymbol,
      [...tasks],
      deleteTaskById,
      updateBuyTickerSymbol
    );

    setTasks(updatedTasks);
  }

  // Function adds a new buy component to tasks
  function addBuy() {
    const Component = createBuyComponent(deleteTaskById, updateBuyTickerSymbol);
    setTasks([...tasks, Component]);

    addSpecifiedWeight();
  }

  return (
    <div>
      <WeightSelector
        changeWeighting={changeWeightingType}
        error={error}
      ></WeightSelector>
      <ul>
        {tasks.map((item, index) => {
          const name = item.type.name;

          let Component = null;

          // If task is buy component
          if (name === "Buy") {
            Component = cloneBuyComponent(
              item,
              deleteTaskById,
              updateBuyTickerSymbol
            );
          }

          return (
            <li key={Math.floor(Math.random() * 99999)}>
              {/* If weighting type is set to specified must render the corresponding specified weight for task (same index) */}
              {weightingType === "Specified"
                ? cloneSpecifiedWeightComponent(
                    specifiedWeights[index],
                    deleteSpecifiedWeightById,
                    updateSpecifiedWeight
                  )
                : null}

              {/* If weighting type is equal dont indent the tasks again keep it in a div */}
              {weightingType === "Equal" ? (
                <div key={Math.floor(Math.random() * 99999)}>{Component}</div>
              ) : null}

              {/* If weighting type is specified indent the specified weights and tasks by putting it in ul */}
              {weightingType === "Specified" ? (
                <ul>
                  <li key={Math.floor(Math.random() * 99999)}>{Component}</li>
                </ul>
              ) : null}
            </li>
          );
        })}
      </ul>
      <button onClick={addBuy}>add buy</button>
      <button onClick={showChildren}>show children</button>
    </div>
  );
};

export default Instructions;
