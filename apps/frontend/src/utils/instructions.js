// This file contains functions which help with the instructions component

/**
 * Removes a react element from list by its id prop.
 * @param {int} id The react elements id prop value which you want to remove from the items list.
 * @param {Array.<ReactElement>} items The list of react elements from which you want to remove item from.
 * @returns {Array.<ReactElement>} List of react elements without react element with specified id prop.
 */
export const deleteItemById = (id, items) => {
  // Search for item with specified id
  items.forEach((item, index) => {
    if (item.props.id === id) {
      // Remove item from list
      items.splice(index, 1);
    }
  });

  return items;
};
