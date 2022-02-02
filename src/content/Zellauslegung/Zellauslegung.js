import React from 'react';
import { Breadcrumb, BreadcrumbItem } from 'carbon-components-react';

import Zellformate from './components/zellformate';

export default function Zellauslegung() {
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
      <div className="bx--row">
        <Zellformate />
      </div>
    </div>
  );
}
