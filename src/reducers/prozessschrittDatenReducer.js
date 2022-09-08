const prozessschrittDatenReducer = (state = null, action) => {
    switch (action.type) {
      case 'PROZESS_DATEN_CHANGE':
        return action.payload;
      default:
        return state;
    }
  };
  export default prozessschrittDatenReducer;
  
