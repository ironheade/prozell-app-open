const quellenReducer = (state = null, action) => {
    switch (action.type) {
      case 'QUELLEN':
        return action.payload;
      default:
        return state;
    }
  };
  export default quellenReducer;
  
