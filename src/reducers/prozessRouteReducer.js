const route = [{
    "Materialformulierung":[]
},{
    "Schichtherstellung": []
},{
    "Elektrodenkonditionierung": []
},{
    "Elektrodenkonfektionierung": []
},{
    "Zellassemblierung": []
},{
    "Elektrolytbefüllung": []
},{    
    "Formierung": []
}]

const prozessRouteReducer = (state = route, action) => {
    switch (action.type) {
      case 'PROZESSROUTE_CHANGE':
        return action.payload;
      default:
        return state;
    }
  };
  export default prozessRouteReducer;
  
