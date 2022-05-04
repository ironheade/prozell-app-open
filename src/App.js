import React from 'react';
import './app.scss';
import { Content } from 'carbon-components-react';
import TutorialHeader from './components/TutorialHeader';
import { Route, Switch } from 'react-router-dom';
import LandingPage from './content/LandingPage';
import Zellauslegung from './content/Zellauslegung';
import Prozessauslegung from './content/Prozessauslegung';
import AllgemeineParameter from './content/AllgemeineParameter';
import Ergebnisse from './content/Ergebnisse';
import { useDispatch } from 'react-redux';

import {
  gebaeude_state,
  oekonomische_parameter_state,
  mitarbeiter_logistik_state,
  zellmaterialien_state,
  alle_zellen_laden,
  quellen
} from './actions';

const App = () => {
  async function tabelle_abrufen(tabelle_dateiname) {
    const res = await fetch('/tabelle_abrufen', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        tabelle: tabelle_dateiname,
      }),
    });
    const data = await res.json();
    return data.tabelle;
  }

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
  tabelle_abrufen('quellen').then(data =>
    dispatch(quellen(data))
  );

  return (
    <>
      <TutorialHeader />
      <Content>
        <Switch>
          <Route exact path="/" component={LandingPage} />
          <Route path="/Zellauslegung" component={Zellauslegung} />
          <Route path="/Prozessauslegung" component={Prozessauslegung} />
          <Route path="/AllgemeineParameter" component={AllgemeineParameter} />
          <Route path="/Ergebnisse" component={Ergebnisse} />
        </Switch>
      </Content>
    </>
  );
};

export default App;