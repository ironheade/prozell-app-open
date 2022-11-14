import React, { useState } from 'react';
import { Breadcrumb, BreadcrumbItem, Tabs, Tab } from 'carbon-components-react';
import Zellformate from './components/zellformate';
import Zellchemie from './components/zellchemie';
import Zellergebnisse from './components/Zellergebnisse'


export default function Zellauslegung() {
  const [chosenTab, setChosenTab] = useState(0)
  function Ergebnisse() {setChosenTab(1)}

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

  return (
    <div className="bx--grid bx--grid--full-width zellauslegung">
      <div className="bx--row __banner">
        <div className="bx--col-lg-16">
          <Breadcrumb noTrailingSlash aria-label="Page navigation">
            <BreadcrumbItem>
              <a href="/">Startseite</a>
            </BreadcrumbItem>
            <BreadcrumbItem>
              <a href="/#/Zellauslegung">Zellauslegung</a>
            </BreadcrumbItem>
          </Breadcrumb>
          <h1 className="__heading">Zellauslegung &amp; Zellchemie</h1>
        </div>
      </div>

      <div className="bx--row landing-page__r2">
        <div className="bx--col bx--no-gutter">
          <Tabs {...props.tabs} aria-label="Tab navigation" selected={chosenTab}>
            <Tab {...props.tab} label="Übersicht" onClick={()=>setChosenTab(0)}>
              <div className="bx--row">
              <div className="bx--col-lg-1"></div>
                <div className="bx--col-lg-6">
                  <Zellformate />
                </div>
                <div className="bx--col-lg-1"></div>
                <div className="bx--col-lg-7">
                  <Zellchemie click={Ergebnisse}/>
                </div>
                <div className="bx--col-lg-1"></div>
              </div>
            </Tab>
            <Tab {...props.tab} label="Ergebnisse Zellauslegung" onClick={()=>setChosenTab(1)}>

              <div className="bx--row">
                <Zellergebnisse/>
              </div>

              </Tab>
          </Tabs>
        </div>
      </div>
    </div>
  );
}
