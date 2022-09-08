const zellchemieNameReducer = (state = null, action) => {
  switch (action.type) {
    case 'ZELLCHEMIENAME_CHANGE':
      return action.payload;
    default:
      return state;
  }
};
export default zellchemieNameReducer;

