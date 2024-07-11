// This file contains functions which help with the specified weight component
import React from "react";
import SpecifiedWeight from "../components/AlgoBuilder/AlgoTypes/SpecifiedWeight/SpecifiedWeight";
/**
 * Creates a algo type specified weight component
 * @param {function} deleteMeFunction Function used so that specified weight component can delete itself.
 * @param {function} updateTickerFunction Function used to that specified weight component can update weight.
 * @returns {<ReactElement>} Algo type specified weight component.
 */
export const createSpecifiedWeightComponent = (
  deleteMeFunction,
  updateWeightFunction
) => {
  const randomNumber = Math.floor(Math.random() * 99999);
  const Component = (
    <SpecifiedWeight
      id={randomNumber}
      key={randomNumber}
      specifiedWeight={"Set Weight"}
      deleteMe={deleteMeFunction}
      updateSpecifiedWeight={updateWeightFunction}
    ></SpecifiedWeight>
  );

  return Component;
};

/**
 * Will create a specified weight component for each task when weighting type changes to specified.
 * @param {Array.<ReactElement>} items The list of react elements you need to create specified weights for.
 * @param {function} deleteMeFunction Function used so that specified weight component can delete itself.
 * @param {function} updateWeightFunction Function used to that specified weight component can update weight.
 * @returns {Array.<ReactElement>} List of specified weight components.
 */
export const buildSpecifiedWeights = (
  items,
  deleteMeFunction,
  updateWeightFunction
) => {
  let specifiedWeights = [];
  // For each task we must add a specified weight to it
  items.forEach((item) => {
    const Component = createSpecifiedWeightComponent(
      deleteMeFunction,
      updateWeightFunction
    );
    specifiedWeights.push(Component);
  });

  return specifiedWeights;
};

/**
 * Clones a algo type specified weight component with updated data such as functions.
 * @param {<ReactElement>} SpecifiedWeightComponent
 * @param {function} deleteMeFunction Function used so that specified weight component can delete itself.
 * @param {function} updateWeightFunction Function used to that specified weight component can update weight.
 * @returns {<ReactElement>} Algo type specified weight component.
 */
export const cloneSpecifiedWeightComponent = (
  SpecifiedWeightComponent,
  deleteMeFunction,
  updateWeightFunction
) => {
  const id = SpecifiedWeightComponent.props.id;
  const specifiedWeight = SpecifiedWeightComponent.props.specifiedWeight;

  const Component = React.cloneElement(<SpecifiedWeight></SpecifiedWeight>, {
    id: id,
    key: id,
    specifiedWeight: specifiedWeight,
    deleteMe: deleteMeFunction,
    updateSpecifiedWeight: updateWeightFunction,
  });

  return Component;
};

/**
 * Changes specified weight of specified weight component with id.
 * @param {int} id The prop id of the specified weight component whos specified weight will be changed.
 * @param {string} specifiedWeight The specified weight to update specified components specified weight to.
 * @param {Array.<ReactElement>} items The list of react elements from which the specified weight component is in.
 * @param {function} deleteMeFunction Function used so that specified weight component can delete itself.
 * @param {function} updateWeightFunction Function used to that specified weight component can update weight.
 * @returns {Array.<ReactElement>} List of react elements with updated specified weight component.
 */
export const updateSpecifiedWeightComponentWeight = (
  id,
  specifiedWeight,
  items,
  deleteMeFunction,
  updateWeightFunction
) => {
  // Search for item with specified id
  items.forEach((item, index) => {
    if (item.props.id === id) {
      const id = item.props.id;

      // Clone component with specified weight
      const Component = React.cloneElement(
        <SpecifiedWeight></SpecifiedWeight>,
        {
          id: id,
          key: id,
          specifiedWeight: specifiedWeight,
          deleteMe: deleteMeFunction,
          updateSpecifiedWeight: updateWeightFunction,
        }
      );

      // Replacing old component with clone
      items[index] = Component;
    }
  });

  return items;
};

export const deleteSpecifiedWeightAndChildById = (
  id,
  tasks,
  specifiedWeights
) => {
  // Removing the specified weight from specified weights and its corresponding task from tasks
  specifiedWeights.forEach((item, index) => {
    if (item.props.id === id) {
      // Remove specified weight from specified weights
      specifiedWeights.splice(index, 1);
      // Removing the weights corresponding task from tasks
      tasks.splice(index, 1);
    }
  });

  return [specifiedWeights, tasks];
};

export const doSpecifiedWeightsAddTo100 = (specifiedWeights) => {
  // Keep track of total weight of all specified weight components
  let totalWeight = 0;

  // Removing the specified weight from specified weights and its corresponding task from tasks
  specifiedWeights.forEach((item, index) => {
    const weight = item.props.specifiedWeight;

    // If weight cannot be turned into a number or its blank
    if (!Number(weight) || weight === "") {
      totalWeight = -1000000;
    } else {
      totalWeight += Number(weight);
    }
  });

  if (totalWeight === 100) {
    return true;
  }

  return false;
};
