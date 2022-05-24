import { Tab, Tabs } from "carbon-components-react";
import React from "react";
import DatenbankTable from "./DatenbankTable";

export default function Datenbank() {
    return (
        <div style={{ textAlign: "center" }}>
            <div style={{ display: "inline-block" }}>
            
                <Tabs  style={{ marginBottom: "20px" }}>
                    <Tab className="Tab"label="Prozessschritte">
                        To be continued
                    </Tab>
                    <Tab label="Zellformate">
                        Tab Label 23
                    </Tab>
                    <Tab label="Materialien">
                        Tab Label 3
                    </Tab>
                    <Tab label="Prozessrouten">
                        Tab Label 4 with a very long long title
                    </Tab>
                    <Tab label="Allgemeine Paramter">
                        Tab Label 5
                    </Tab>
                    <Tab label="Zellchemien">
                        Tab Label 5
                    </Tab>
                    <Tab label="Quellen">
                        Tab Label 5
                    </Tab>
                </Tabs>
                <DatenbankTable/>
            </div>
        </div>
    )
}