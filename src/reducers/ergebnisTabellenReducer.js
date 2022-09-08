const ergebnisTabellenReducer = (state = null, action) => {
    switch (action.type) {
      case 'ERGEBNIS_TABELLE':
        return action.payload;
      default:
        return state;
    }
  };
  export default ergebnisTabellenReducer;
  