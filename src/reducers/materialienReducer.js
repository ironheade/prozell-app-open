const materialienReducer = (state = null, action) => {
  // handle a particular action type
  if (action.type === 'MATERIALIEN_CHANGE') {
    // return the new state
    return action.payload;
  }
  // always return state
  return state;
};

export default materialienReducer;
