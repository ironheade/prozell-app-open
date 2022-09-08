const materialInfosReducer = (state = 'null', action) => {
  // handle a particular action type
  if (action.type === 'MATERIALINFOS_CHANGE') {
    // return the new state
    return action.payload;
  }
  // always return state
  return state;
};

export default materialInfosReducer;
