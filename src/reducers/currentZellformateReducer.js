const currentZellformateReducer = (state = null, action) => {
    // handle a particular action type
    if (action.type === 'CURRENTZELLFORMATE_REDUCER') {
      // return the new state
      return action.payload;
    }
    // always return state
    return state;
  };
  
  export default currentZellformateReducer;
  