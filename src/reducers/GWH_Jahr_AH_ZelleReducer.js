const initialstate = {GWh_pro_jahr:0,Ah_pro_Zelle:0}
const GWH_Jahr_AH_ZelleReducer = (state = initialstate, action) => {
  switch (action.type) {
    case 'GWH_JAHR_AH_ZELLE_STATE':
      return action.payload;
    default:
      return state;
  }
};
  export default GWH_Jahr_AH_ZelleReducer;
  