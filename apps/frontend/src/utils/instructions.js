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

/**
 * Finds react element in firsList with id, removes it, removes react element in secondList that has same index as item which was removed in firstList.
 * @param {int} id The react elements id prop value which you want to search for in firstList.
 * @param {Array.<ReactElement>} firstList The list of react elements from which you search for with id and remove.
 * @param {Array.<ReactElement>} secondList The list of react elements from which you will also remove element from which will be same index as element removed from firstList.
 * @returns {[Array.<ReactElement>, Array.<ReactElement>]} firstList without react element with id, secondList without element that has same index as element removed in firstList.
 */
export const spliceListsByIdAtSameIndex = (id, firstList, secondList) => {
  // Removing the specified item by id from first list and its corresponding item (same index) from secondList
  firstList.forEach((item, index) => {
    if (item.props.id === id) {
      // Removing items from each of the lists
      firstList.splice(index, 1);
      secondList.splice(index, 1);
    }
  });

  return [firstList, secondList];
};
