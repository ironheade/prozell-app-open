const loggedInReducer = (state = true, action) => {
  switch (action.type) {
    case 'LOGIN':
      return action.payload;
    default:
      return state;
  }
};
export default loggedInReducer;
