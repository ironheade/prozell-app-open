const loggedInAdminReducer = (state = true, action) => {
  switch (action.type) {
    case 'LOGIN_ADMIN':
      return action.payload;
    default:
      return state;
  }
};
export default loggedInAdminReducer;
