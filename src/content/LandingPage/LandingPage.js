import React, { useState, useEffect } from 'react';
import {
  Breadcrumb,
  BreadcrumbItem,
  Button,
  Tabs,
  Tab,
} from 'carbon-components-react';
import { InfoSection, InfoCard } from '../../components/Info';
import PersonFavorite32 from '@carbon/icons-react/lib/person--favorite/32';
import Application32 from '@carbon/icons-react/lib/application/32';

import { Apple32 } from '@carbon/icons-react';
import Anleitung from './Anleitung';

const props = {
  tabs: {
    selected: 0,
    role: 'navigation',
  },
  tab: {
    role: 'presentation',
    tabIndex: 0,
  },
};


const LandingPage = () => {
  const [currentTime, setCurrentTime] = useState(0);
  const [chosenTab, setChosenTab] = useState(0)

  useEffect(() => {
    fetch('/time')
      .then(res => res.json())
      .then(data => {
        setCurrentTime(data.time);
      });
  }, []);

 const Unterstützer = ["Max Mitrenga","Patrick Berghäuser","Mona Kabus", "Felix Buck", "Anna Kollenda","Julian Mayer"]

  return (
    <div className="bx--grid bx--grid--full-width landing-page">
      <div className="bx--row __banner">
        <div className="bx--col-lg-16">
          <Breadcrumb noTrailingSlash aria-label="Page navigation">
            <BreadcrumbItem>
              <a href="/">Startseite</a>
            </BreadcrumbItem>
          </Breadcrumb>
          <h1 className="__heading">ProZell Kostenrechner</h1>
        </div>
      </div>
      <div className="bx--row landing-page__r2">
        <div className="bx--col bx--no-gutter">
          <Tabs {...props.tabs} aria-label="Tab navigation" selected={chosenTab} >
            <Tab {...props.tab} label="Übersicht" onClick={()=>setChosenTab(0)}>
              <div className="bx--grid bx--grid--no-gutter bx--grid--full-width">
                <div className="bx--row landing-page__tab-content">
                  <div className="bx--col-md-4 bx--col-lg-7">
                    <h2 className="landing-page__subheading">
                      Was ist der ProZell Kostenrechner?
                    </h2>
                    <p>Last refresh: {currentTime}</p>
                    <p className="landing-page__p">
                      Der ProZell Kostenrechner ist die flexible Umsetzung eines
                      Modells zur Bepreisung der einzelnen Prozesschritte einer
                      Batteriezellfertigung, der ökonomischen Evaluation neuer
                      Prozessschritte und zur weiteren Optimierung der
                      Prozessroute.
                    </p>
                    <Button onClick={() => setChosenTab(1)}>Anleitung</Button>
                  </div>
                  <div className="bx--col-md-4 bx--offset-lg-1 bx--col-lg-8">
                    <img
                      className="landing-page__illo"
                      src={`${process.env.PUBLIC_URL}/batteries5.png`}
                      alt="Carbon illustration"
                    />
                  </div>
                </div>
              </div>
            </Tab>
            <Tab {...props.tab} label="Anleitung" onClick={()=>setChosenTab(1)}>
              <div className="bx--grid" style={{paddingLeft:300, paddindRight:300}}>
                <div className="bx--row  landing-page__tab-content">

                  <Anleitung/>

                </div>
              </div>
            </Tab>
            <Tab {...props.tab} label="Impressum" onClick={()=>setChosenTab(2)}>
              <div className="bx--grid bx--grid--no-gutter bx--grid--full-width">
                <div className="bx--row landing-page__tab-content">
                <div className="bx--col-lg-12"> 
                    <p>V1.0 - Release (11.03.2022)</p>
                    <p>V1.1 (28.03.2022)</p>
                    <ul style={{listStyle:"inherit", paddingLeft:40}}>
                      <li>Fehlerbehebun in der Zellauslegung</li>
                      <li>Hinzufügen einer Anleitung</li>
                      </ul>

                  </div>
                  <div className="bx--col-lg-4">
                    <p>
                       <span style={{fontWeight:"bold"}}>Kontakt:</span><br/>Konrad Bendzuck <br/> k.bendzuck@tu-braunschweig.de <br/> 0531/ 391 94648
                    </p>
                    <br/>
                    <p><span style={{fontWeight:"bold"}}>Unterstützung durch:</span></p>
                    {Unterstützer.map(item => <p>{item}</p>)}

                  </div>
                </div>
              </div>
            </Tab>
          </Tabs>
        </div>
      </div>
      <InfoSection heading="Principles" className="landing-page__r3">
        <InfoCard
          heading="Carbon is Open"
          body="It's a distributed effort, guided by the principles of the open-source movement. Carbon's users are also it's makers, and everyone is encouraged to contribute."
          icon={<PersonFavorite32 />}
        />
        <InfoCard
          heading="Carbon is Modular"
          body="Carbon's modularity ensures maximum flexibility in execution. It's components are designed to work seamlessly with each other, in whichever combination suits the needs of the user."
          icon={<Application32 />}
        />
        <InfoCard
          heading="Carbon is Consistent"
          body="Based on the comprehensive IBM Design Language, every element and component of Carbon was designed from the ground up to work elegantly together to ensure consistent, cohesive user experiences."
          icon={<Apple32 />}
        />
      </InfoSection>
    </div>
  );
};

export default LandingPage;
