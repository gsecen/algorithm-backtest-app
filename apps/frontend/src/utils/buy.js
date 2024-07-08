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

/**
 * Changes buy component with specified id's ticker symbol to specified ticker symbol.
 * @param {int} id The prop id of the buy component whos ticker symbol will be changed.
 * @param {string} tickerSymbol The ticker symbol to update buy component ticker symbol to.
 * @param {Array.<ReactElement>} items The list of react elements from which the buy component is in.
 * @param {function} deleteMeFunction Function used so that buy component can delete itself.
 * @param {function} updateTickerFunction Function used to that buy component can update ticker symbol.
 * @returns {Array.<ReactElement>} List of react elements with updated buy component.
 */
export const updateBuyComponentTicker = (
  id,
  tickerSymbol,
  items,
  deleteMeFunction,
  updateTickerFunction
) => {
  // Search for item with specified id
  items.forEach((item, index) => {
    if (item.props.id === id) {
      const id = item.props.id;

      // Clone component with specified ticker symbol
      const Component = React.cloneElement(<Buy></Buy>, {
        key: id,
        id: id,
        ticker: tickerSymbol,
        deleteMe: deleteMeFunction,
        updateTickerSymbol: updateTickerFunction,
      });

      // Replacing old component with clone
      items[index] = Component;
    }
  });

  return items;
};
