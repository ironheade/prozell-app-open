const rueckgewinnungReducer = (state = null, action) => {
    switch (action.type) {
      case 'RUECKGEWINNUNG':
        return action.payload;
      default:
        return state;
    }
  };
  export default rueckgewinnungReducer;
  
  

