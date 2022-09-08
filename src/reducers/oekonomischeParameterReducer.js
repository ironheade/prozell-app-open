const oekonomischeParameterReducer = (state = null, action) => {
  switch (action.type) {
    case 'OEKONOMISCHE_PARAMETER_STATE':
      return action.payload;
    default:
      return state;
  }
};
export default oekonomischeParameterReducer;
