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
import  tabelle_abrufen  from '../../functions/tabelle_abrufen'
import { Apple32 } from '@carbon/icons-react';
import Anleitung from './Anleitung';
import { useSelector } from "react-redux";

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
  const quellen = useSelector(state => state.quellen)

  console.log(quellen)

  useEffect(() => {
    fetch('/time')
      .then(res => res.json())
      .then(data => {
        setCurrentTime(data.time);
      });
  }, []);

  const Unterstützer = ["Max Mitrenga",
    "Patrick Berghäuser",
    "Mona Kabus",
    "Felix Buck",
    "Anna Kollenda",
    "Lukas Kemmer",
    "Maximilian Blaschke",
    "Josef Keilhofer",
    "Maximilian Lechner",
    "Julian Mayer",
    "Usama Khalid"]

  const Versionskontrolle = [
    {
      Version: "V1.0 - Release",
      Datum: "11.03.2022",
      Änderungen: []
    },
    {
      Version: "V1.1",
      Datum: "28.03.2022",
      Änderungen: [
        "Fehlerbehebun in der Zellauslegung",
        "Hinzufügen einer Anleitung"
      ]
    },
    {
      Version: "V1.2",
      Datum: "04.04.2022",
      Änderungen: [
        "Umbenennung der Zelltypen",
        "Hinzufügen von NCM 811/Graphit/Si Zellchemien",
        "PLatzhalter Prozessschritt 'Benetzen' hinzugefügt"
      ]
    },
    {
      Version: "V1.3",
      Datum: "05.04.2022",
      Änderungen:
        [
          "Fehlerbehebung in der Hardcase Wickelzelle"
        ]
    },
    {
      Version: "V1.4",
      Datum: "06.04.2022",
      Änderungen: [
        "Anzeige Trockenraum in der Ergebnisdarstellung korregiert",
        "Platzhalter für weitere Graphen in dern Ergebnissen eingefügt"
      ]
    }
  ]

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
            <Tab {...props.tab} label="Übersicht" onClick={() => setChosenTab(0)}>
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
            <Tab {...props.tab} label="Anleitung" onClick={() => setChosenTab(1)}>
              <div className="bx--grid" id="Anleitung" >
                <div className="bx--row  landing-page__tab-content">

                  <Anleitung />

                </div>
              </div>
            </Tab>
            <Tab {...props.tab} label="Impressum" onClick={() => setChosenTab(2)}>
              <div className="bx--grid bx--grid--no-gutter bx--grid--full-width">
                <div className="bx--row landing-page__tab-content">
                  <div className="bx--col-lg-12">
                    {Versionskontrolle.map((item, index) =>
                      <div key={index}>
                        <p>{item.Version} ({item.Datum})</p>
                        {item.Änderungen !== [] &&
                          <ul style={{ listStyle: "inherit", paddingLeft: 40 }}>
                            {item.Änderungen.map((item, index) =>
                              <li key={index}>{item}</li>
                            )}
                          </ul>
                        }
                      </div>
                    )}

                  </div>
                  <div className="bx--col-lg-4">
                    <p>
                      <span style={{ fontWeight: "bold" }}>Kontakt:</span><br />Konrad Bendzuck <br /> k.bendzuck@tu-braunschweig.de <br /> 0531/ 391 94648
                    </p>
                    <br />
                    <p><span style={{ fontWeight: "bold" }}>Unterstützung durch:</span></p>
                    {Unterstützer.map(item => <p key={item}>{item}</p>)}

                  </div>
                </div>
              </div>
            </Tab>
            <Tab {...props.tab} label="Quellen" onClick={() => setChosenTab(3)}>
              <div className="bx--grid bx--grid--no-gutter bx--grid--full-width">
                <div className="bx--row landing-page__tab-content">
                  <div className="bx--col-lg-16">
                    <h3>Quellen</h3>
                  <table style={{borderSpacing:"10px",borderCollapse:"separate"}}>
                    <tbody>
                    {quellen !== null && JSON.parse(quellen).map(item =>
                      <tr key={item.id}>
                        <td>[{item.Nachname}, {item.Jahr}]</td>
                        <td>      </td>
                        <td>{item.Nachname}, {item.Vorname} ({item.Jahr}), "{item.Titel}", {item.Verlag}, {item.doi !== null && item.doi} {item.ISBN!== null && item.ISBN}</td>
                      </tr>
                      )}
                      </tbody>
                  </table>
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
