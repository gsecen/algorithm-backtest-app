import React from "react";
import "./typeSelector.css";

const TypeSelector = (props) => {
  return (
    <div>
      Add
      <ul>
        <li>
          <button onClick={props.addBuy}>Asset</button>
        </li>
      </ul>
    </div>
  );
};

export default TypeSelector;
