import React, { Component } from 'react';
import './app.scss';
import { Content } from 'carbon-components-react';
import TutorialHeader from './components/TutorialHeader';
import { Route, Switch } from 'react-router-dom';
import LandingPage from './content/LandingPage';
import Zellauslegung from './content/Zellauslegung';
import Prozessauslegung from './content/Prozessauslegung';
import AllgemeineParameter from './content/AllgemeineParameter';
import Ergebnisse from './content/Ergebnisse';

class App extends Component {
  render() {
    return (
      <>
        <TutorialHeader />
        <Content>
          <Switch>
            <Route exact path="/" component={LandingPage} />
            <Route path="/Zellauslegung" component={Zellauslegung} />
            <Route path="/Prozessauslegung" component={Prozessauslegung} />
            <Route
              path="/AllgemeineParameter"
              component={AllgemeineParameter}
            />
            <Route path="/Ergebnisse" component={Ergebnisse} />
          </Switch>
        </Content>
      </>
    );
  }
}

export default App;
