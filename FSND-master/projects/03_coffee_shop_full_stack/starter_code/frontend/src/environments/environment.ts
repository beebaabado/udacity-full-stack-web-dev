/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5001', // the running FLASK api server url
  auth0: {
    url: 'product-demos.us', // the auth0 domain prefix
    audience: 'makecoffee', // the audience set for the auth0 app
    clientId: '10Qj6uG2exop2w4ehTtx9ZLfivLgniNQ', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:8100', // the base url of the running ionic application. 
  }
};
