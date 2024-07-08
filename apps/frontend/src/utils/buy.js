// This file contains functions which help with the buy component
import React from "react";
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
      ticker={"TICKER"}
      deleteMe={deleteMeFunction}
      updateTickerSymbol={updateTickerFunction}
    ></Buy>
  );

  return Component;
};

/**
 * Clones a algo type buy react component with updated data such as functions.
 * @param {*} BuyComponent Algo type buy component.
 * @param {function} deleteMeFunction Function used so that buy component can delete itself.
 * @param {function} updateTickerFunction Function used to that buy component can update ticker symbol.
 * @returns {<ReactElement>} Algo type buy component.
 */
export const cloneBuyComponent = (
  BuyComponent,
  deleteMeFunction,
  updateTickerFunction
) => {
  const id = BuyComponent.props.id;
  const ticker = BuyComponent.props.ticker;

  const Component = React.cloneElement(<Buy></Buy>, {
    key: id,
    id: id,
    ticker: ticker,
    deleteMe: deleteMeFunction,
    updateTickerSymbol: updateTickerFunction,
  });

  return Component;
};
