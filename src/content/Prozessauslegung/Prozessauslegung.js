import React from 'react';
import { Breadcrumb, BreadcrumbItem } from 'carbon-components-react';
import Prozessroute from './components/prozessroute'
import DarstellungProzessroute from './components/darstellung_prozessroute'



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
        
        <DarstellungProzessroute/>
        <Prozessroute/>
        {/*
          <div className="bx--row">
            <div className="bx--col-lg-6" style={{ marginTop: '50px' }}>
              <Prozessroute/>
            </div>

            <div className="bx--col-lg-6" style={{ marginTop: '50px' }}>
              <img  src={logo} style={{height: '200px'}} alt="fireSpot"/>
              <img  src={logo2} style={{height: '200px'}} alt="fireSpot"/>
            </div>
          </div>
*/}



    </div>
  );
}
