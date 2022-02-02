import React from 'react';
import { Breadcrumb, BreadcrumbItem } from 'carbon-components-react';

export default function Prozessauslegung() {
  return (
    <div className="bx--grid bx--grid--full-width prozessauslegung">
      <div className="bx--row __banner">
        <div className="bx--col-lg-16">
          <Breadcrumb noTrailingSlash aria-label="Page navigation">
            <BreadcrumbItem>
              <a href="/">Startseite</a>
            </BreadcrumbItem>
            <BreadcrumbItem>
              <a href="/#/Prozessauslegung">Prozessauslegung</a>
            </BreadcrumbItem>
          </Breadcrumb>
          <h1 className="__heading">Prozessauslegung</h1>
        </div>
      </div>
    </div>
  );
}
