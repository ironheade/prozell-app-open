const emptyReducer = (state = [], action) => {
  // handle a particular action type
  if (action.type === 'EMPTY_REDUCER') {
    // return the new state
    return action.payload;
  }
  // always return state
  return state;
};

export default emptyReducer;
