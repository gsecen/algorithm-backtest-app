import "./weightSelector.css";
import ActionsBar from "../../ActionsBar/ActionsBar";
import Exclamtion from "../../../Exclamation/Exclamtion";
import { useRef, useState } from "react";
import downArrowIcon from "../../../../assets/images/down-arrow.svg";
import checkMarkIcon from "../../../../assets/images/check-mark.svg";

const WeightSelector = ({ changeWeighting, error }) => {
  const actionsBarRef = useRef();

  const [showMenu, setShowMenu] = useState(false);
  const [showWeightingsOptions, setShowWeightingsOptions] = useState(false);

  const [weightType, setWeightType] = useState("Equal");

  function toggleSelectWeightMenu() {
    setShowMenu(!showMenu);
    setShowWeightingsOptions(false);
  }

  function changeWeightType(type) {
    setWeightType(type);
  }

  // Checkmark svg which is next to current selected weight type in menu
  const CheckMark = (
    <img
      alt=""
      className="weight-selector-menu-dropdown-item-icon"
      src={checkMarkIcon}
    ></img>
  );

  return (
    <div
      // Tab index is used to make div focusable
      tabIndex={0}
      onFocus={() => {
        console.log("focused");
      }}
      // When the select weight menu is clicked off
      onBlur={toggleSelectWeightMenu}
      onMouseEnter={() => {
        actionsBarRef.current.currentlyHovering();
      }}
      onMouseLeave={() => {
        actionsBarRef.current.notCurrentlyHovering();
      }}
      className="weight-selector-container"
    >
      <div className="weight-selector-items">
        <div className="weight-selector-text-container">
          <p className="weight-selector-text">WEIGHT {weightType}</p>
        </div>

        <ActionsBar
          ref={actionsBarRef}
          id={123}
          focused={false}
          editMe={toggleSelectWeightMenu}
          // deleteMe={deleteMeFunction}
        ></ActionsBar>

        <Exclamtion
          isError={error}
          errorMessage={"Specified weights must add to 100.00%"}
        ></Exclamtion>
      </div>
      <div className={`weight-selector-menu ${showMenu ? "show" : ""}`}>
        <p className="weight-selector-menu-title-text">SET WEIGHTING</p>
        <p className="weight-selector-menu-type-text">Type</p>
        <div
          onClick={() => {
            setShowWeightingsOptions(!showWeightingsOptions);
          }}
          className="weight-selector-menu-shown-option-container"
        >
          <p className="weight-selector-menu-shown-option-container-text">
            {weightType}
          </p>
          <img
            src={downArrowIcon}
            alt=""
            className="weight-selector-menu-shown-option-icon"
          />
        </div>
        <ul
          className={`weight-selector-menu-dropdown ${
            showWeightingsOptions ? "show" : ""
          }`}
        >
          <li
            onClick={() => {
              changeWeightType("Equal");
              changeWeighting("Equal");
            }}
            className="weight-selector-menu-dropdown-item"
          >
            <p className="weight-selector-menu-dropdown-item-text">Equal</p>
            {weightType === "Equal" ? CheckMark : null}
          </li>
          <li
            onClick={() => {
              changeWeightType("Specified");
              changeWeighting("Specified");
            }}
            className="weight-selector-menu-dropdown-item"
          >
            <p className="weight-selector-menu-dropdown-item-text">Specified</p>
            {weightType === "Specified" ? CheckMark : null}
          </li>
        </ul>
      </div>
    </div>
  );
};

export default WeightSelector;
