import React from "react";
import "./editDelete.css";
import editIcon from "../../../assets/images/pencil-icon.svg";
import deleteIcon from "../../../assets/images/trash-can-icon.svg";

const EditDelete = (props) => {
  function deleteComponent() {
    props.deleteMe(props.id);
  }

  function editComponent() {
    props.editMe();
  }

  return (
    <div style={props.editStyles} className="edit-delete-container">
      <div onClick={editComponent} className="edit-button">
        <img src={editIcon} alt="" className="edit-icon" />
      </div>
      <div onClick={deleteComponent} className="delete-button">
        <img src={deleteIcon} alt="" className="edit-icon" />
      </div>
    </div>
  );
};

export default EditDelete;
