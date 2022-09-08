const zellergebnisseReducer = (state = null, action) => {
    switch (action.type) {
      case 'ZELLERGEBNISSE_CHANGE':
        return action.payload;
      default:
        return state;
    }
  };
  export default zellergebnisseReducer;
  