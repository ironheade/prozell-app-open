const zellformatNameReducer = (state = null, action) => {
  switch (action.type) {
    case 'ZELLFORMATNAME_CHANGE':
      return action.payload;
    default:
      return state;
  }
};
export default zellformatNameReducer;
