// This file contains functions which help with the specified weight component
import SpecifiedWeight from "../components/AlgoBuilder/AlgoTypes/SpecifiedWeight/SpecifiedWeight";
/**
 * Creates a algo type specified weight component
 * @param {function} deleteMeFunction Function used so that buy component can delete itself.
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
      deleteMe={deleteMeFunction}
      specifiedWeight={"Set Weight"}
      updateSpecifiedWeight={updateWeightFunction}
    ></SpecifiedWeight>
  );

  return Component;
};
