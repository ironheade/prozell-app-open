import { Breadcrumb, BreadcrumbItem, Tab, Tabs } from 'carbon-components-react';
import React from 'react';
import NutzerGenerator from './components/Nutzer_generator';

export default function AdminPage() {
    return (
        <div className="bx--grid bx--grid--full-width AdminPage">
            <div className="bx--row __banner">
                <div className="bx--col-lg-16">
                    <Breadcrumb noTrailingSlash aria-label="Page navigation">
                        <BreadcrumbItem>
                            <a href="/">Startseite</a>
                        </BreadcrumbItem>
                        <BreadcrumbItem>
                            <a href="/#/AdminPage">Admin Seite</a>
                        </BreadcrumbItem>
                    </Breadcrumb>
                    <h1 className="__heading">Admin Seite</h1>
                </div>
            </div>
            <div className="bx--row landing-page__r2">
                <div className="bx--col bx--no-gutter">
                <Tabs aria-label="Tab navigation" >
                    <Tab label="Nutzer">
                        <NutzerGenerator/>
                    </Tab>
                    <Tab label="Datenbank">

                    </Tab>
                </Tabs>
                </div>
            </div>
        </div>
    )
}