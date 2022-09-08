const zellchemieReducer = (state = null, action) => {
  switch (action.type) {
    case 'ZELLCHEMIE_CHANGE':
      return action.payload;
    default:
      return state;
  }
};
export default zellchemieReducer;
