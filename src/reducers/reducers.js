
export const zellchemieReducer = (state = null, action) => {
    if (action.type === 'ZELLCHEMIE_CHANGE') {
        return action.payload;
    }
    return state;
  };
 

export const gebaeudeReducer = (state = null, action) => {
    if (action.type === 'GEBAEUDE_STATE') {
        return action.payload;
    }
    return state;
};
