const zellmaterialienReducer = (state = null, action) => {
  // handle a particular action type
  if (action.type === 'ZELLMATERIALIEN_STATE') {
    // return the new state
    return action.payload;
  }
  // always return state
  return state;
};

export default zellmaterialienReducer;
