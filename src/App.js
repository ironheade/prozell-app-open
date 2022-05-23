import React, { useState } from 'react';
import './app.scss';
import { Content } from 'carbon-components-react';
import TutorialHeader from './components/TutorialHeader';
import { Route, Switch } from 'react-router-dom';
import LandingPage from './content/LandingPage';
import Zellauslegung from './content/Zellauslegung';
import Prozessauslegung from './content/Prozessauslegung';
import AllgemeineParameter from './content/AllgemeineParameter';
import Ergebnisse from './content/Ergebnisse';
import AdminPage from './content/AdminPage';
import { useDispatch, useSelector } from 'react-redux';
import tabelle_abrufen from './functions/tabelle_abrufen'

import {
  gebaeude_state,
  oekonomische_parameter_state,
  mitarbeiter_logistik_state,
  zellmaterialien_state,
  alle_zellen_laden,
  quellen,
  rueckgewinnung_state
} from './actions';


const App = () => {

  const dispatch = useDispatch();

  tabelle_abrufen('oekonomische_parameter').then(data =>
    dispatch(oekonomische_parameter_state(data))
  );
  tabelle_abrufen('mitarbeiter_logistik').then(data =>
    dispatch(mitarbeiter_logistik_state(data))
  );
  tabelle_abrufen('gebaeude_parameter').then(data =>
    dispatch(gebaeude_state(data))
  );
  tabelle_abrufen('materialien').then(data =>
    dispatch(zellmaterialien_state(data))
  );
  tabelle_abrufen('Zellformate').then(data =>
    dispatch(alle_zellen_laden(data))
  );
  tabelle_abrufen('rueckgewinnung').then(data =>
    dispatch(rueckgewinnung_state(data))
  );
  tabelle_abrufen('quellen').then(data =>
    dispatch(quellen(data))
  );

  const logged = useSelector(state => state.loggedIn)

  return (
    <>
      <TutorialHeader />
      <Content>
        <Switch>
          <Route exact path="/" component={LandingPage} />
          <Route path="/Zellauslegung" component={logged ? Zellauslegung : LandingPage} />
          <Route path="/Prozessauslegung" component={logged ? Prozessauslegung : LandingPage} />
          <Route path="/AllgemeineParameter" component={logged ? AllgemeineParameter : LandingPage} />
          <Route path="/Ergebnisse" component={logged ? Ergebnisse : LandingPage} /> 
          {/*<Route path="/Adminpage" component={logged ? AdminPage : LandingPage} />*/}
          <Route path="/Adminpage" component={AdminPage} />
        </Switch>
      </Content>
    </>
  );
};

export default App;