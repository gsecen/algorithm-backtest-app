// This file contains functions which help with the buy component
import Buy from "../components/AlgoBuilder/AlgoTypes/Buy/Buy";

/**
 * Creates a algo type buy component
 * @param {function} deleteMeFunction Function used so that buy component can delete itself.
 * @param {function} updateTickerFunction Function used to that buy component can update ticker symbol.
 * @returns {<ReactElement>} Algo type buy component.
 */
export const createBuyComponent = (deleteMeFunction, updateTickerFunction) => {
  const randomNumber = Math.floor(Math.random() * 99999);
  const Component = (
    <Buy
      key={randomNumber}
      id={randomNumber}
      deleteMe={deleteMeFunction}
      updateTickerSymbol={updateTickerFunction}
      ticker={"TICKER"}
    ></Buy>
  );

  return Component;
};
