import React from 'react';
import { Breadcrumb, BreadcrumbItem, Tabs, Tab } from 'carbon-components-react';
import Zellformate from './components/zellformate';
import Zellchemie from './components/zellchemie';

export default function Zellauslegung() {
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
          <Tabs {...props.tabs} aria-label="Tab navigation">
            <Tab {...props.tab} label="Übersicht">
              <div className="bx--row">
                <div className="bx--col-lg-8">
                  <Zellformate />
                </div>
                <div className="bx--col-lg-8">
                  <Zellchemie />
                </div>
              </div>
            </Tab>
            <Tab {...props.tab} label="Ergebnisse Zellauslegung" />
          </Tabs>
        </div>
      </div>
    </div>
  );
}
