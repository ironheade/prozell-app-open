const alleZellenReducer = (state = null, action) => {
  switch (action.type) {
    case 'ALLE_ZELLEN_LADEN':
      return action.payload;
    default:
      return state;
  }
};
export default alleZellenReducer;
