const alleZellformateReducer = (state = null, action) => {
  switch (action.type) {
    case 'ALLE_ZELLFORMATE_STATE':
      return action.payload;
    default:
      return state;
  }
};
export default alleZellformateReducer;
