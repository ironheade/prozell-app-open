const mitarbeiterLogistikReducer = (state = null, action) => {
  switch (action.type) {
    case 'MITARBEITER_LOGISTIK_STATE':
      return action.payload;
    default:
      return state;
  }
};
export default mitarbeiterLogistikReducer;
