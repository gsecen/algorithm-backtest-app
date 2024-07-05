import { useState, useRef } from "react";
import "./buy.css";

import ActionsBar from "../../ActionsBar/ActionsBar";
import Exclamtion from "../../../Exclamation/Exclamtion";

/**
 *
 * @property {function} deleteMe The function from parent which will delete element.
 * @property {function} updateTickerSymbol The function from parent which will update elements ticker symbol.
 * @property {int} id The elements unqiue id.
 * @property {string} ticker The ticker symbol which will be displayed to the user.
 * @returns {ReactNode} Algorithms type buy react element.
 */
const Buy = ({ id, deleteMe, updateTickerSymbol, ticker }) => {
  const [tickerSymbol, setTickerSymbol] = useState(ticker);
  const [isFocused, setIsFocused] = useState(false);

  const actionsBarRef = useRef();

  // Variables which will be passed down to the edit delete menu
  const myId = id;
  const deleteMeFunction = deleteMe;

  // Exclamation is shown if ticker symbol is "TICKER" which means it still needs to be edited
  let exclamationVisibility = "hidden";
  let exclamationOpacity = 0;
  if (tickerSymbol === "TICKER") {
    exclamationVisibility = "visible";
    exclamationOpacity = 1;
  }

  // Toggles whether the ticker symbol input is in focus
  function toggleFocus() {
    setIsFocused(!isFocused);
  }

  // Used when the user wants to edit ticker symbol
  const Input = (
    <input
      onChange={(e) => {
        setTickerSymbol(e.target.value.toUpperCase());
      }}
      // When input loses focus (clicked outside of input)
      onBlur={() => {
        toggleFocus();
        actionsBarRef.current.checkHoverOnEditComplete();
        updateTickerSymbol(id, tickerSymbol);
      }}
      className="ticker-symbol-input"
      autoFocus={true}
      value={tickerSymbol}
      type="text"
    />
  );

  // Used when the user is not trying to edit input
  const P = <p className="ticker-symbol-text">{tickerSymbol}</p>;

  return (
    <div
      onMouseEnter={() => {
        actionsBarRef.current.currentlyHovering();
      }}
      onMouseLeave={() => {
        actionsBarRef.current.notCurrentlyHovering();
      }}
      className="buy-item-container"
    >
      <div className="buy-symbol">
        <p className="dollar-sign">$</p>
      </div>
      {isFocused ? Input : P}

      <ActionsBar
        ref={actionsBarRef}
        id={myId}
        focused={isFocused}
        editMe={toggleFocus}
        deleteMe={deleteMeFunction}
      ></ActionsBar>

      <Exclamtion
        editStyles={{
          visibility: exclamationVisibility,
          opacity: exclamationOpacity,
        }}
        errorMessage={"You must enter a ticker symbol"}
      ></Exclamtion>
    </div>
  );
};

export default Buy;
