const zellformatReducer = (state = null, action) => {
  switch (action.type) {
    case 'ZELLFORMAT_CHANGE':
      return action.payload;
    default:
      return state;
  }
};
export default zellformatReducer;
