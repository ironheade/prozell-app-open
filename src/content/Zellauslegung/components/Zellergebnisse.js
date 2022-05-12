import React from 'react';
import { useSelector } from 'react-redux';
import {
  TableRow,
  TableCell,
  TableBody,
  Table,
  TableHead,
  TableHeader,
} from 'carbon-components-react';
import { DonutChart } from '@carbon/charts-react';

import { CSVLink } from 'react-csv';

export default function Zellergebnisse() {
  const Zellergebnisse = useSelector(state => state.zellergebnisse);

  var donutData = [];
  var excludeList = [
    'Gesamtgewicht Zelle',
    'Gesamtdichte Anodenbeschichtung',
    'Gesamtdichte Kathodenbeschichtung',
  ];
  Zellergebnisse !== null &&
    JSON.parse(Zellergebnisse)
      .filter(
        item =>
          item.Kategorie === 'Gewichte und Dichten' &&
          !excludeList.includes(item.Beschreibung)
      )
      .map(item =>
        donutData.push({ group: item.Beschreibung, value: item.Wert })
      );

  const headers = [
    { label: 'Beschreibung', key: 'Beschreibung' },
    { label: 'Wert', key: 'Wert' },
    { label: 'Einheit', key: 'Einheit' },
  ];

  const csvReport = {
    headers: headers,
    filename: 'Clue_Mediator_Report.csv',
  };

  var costDonutData = [];
  var excludeListCost = [
    'Kilopreis Anodenbeschichtung',
    'Kilopreis Kathodenbeschichtung',
    'Materialkosten einer Zelle',
  ];
  Zellergebnisse !== null &&
    JSON.parse(Zellergebnisse)
      .filter(
        item =>
          item.Kategorie === 'Kosten' &&
          !excludeListCost.includes(item.Beschreibung)
      )
      .map(item =>
        costDonutData.push({ group: item.Beschreibung, value: item.Wert })
      );

  const costDonutOptions = {
    title: 'Kostenverteilung Zelle',
    resizable: true,
    legend: {
      position: 'left',
      orientation: 'vertical',
      truncation: {
        numCharacter: 45,
      },
    },
    donut: {
      center: {
        label: 'Gesamtkosten Zelle [€]',
        "numberFormatter": (number) => Math.round(number*100)/100    
      },
      alignment: 'center',
    },
    height: '400px',
    width: '600px',
  };

  const donutOptions = {
    title: 'Gewichtsverteilung Zelle',
    resizable: true,
    legend: {
      position: 'left',
      orientation: 'vertical',
      truncation: {
        numCharacter: 45,
      },
    },
    donut: {
      center: {
        label: 'Gewicht Zelle [g]',
        "numberFormatter": (number) => Math.round(number*100)/100  
      },
      alignment: 'center',
    },
    height: '400px',
    width: '600px',
  };

  return (
    <>
    <div className="bx--col-lg-1"></div>
      {Zellergebnisse !== null && (
        <div className="bx--col-lg-6">
          <h2>Ergebnisstabelle</h2>
          <Table useZebraStyles size="compact" className="zellchemie_table">
            <TableHead>
              <TableRow>
                <TableHeader>Beschreibung</TableHeader>
                <TableHeader>Wert</TableHeader>
                <TableHeader>Einheit</TableHeader>
              </TableRow>
            </TableHead>

            {[
              ...new Set(
                JSON.parse(Zellergebnisse).map(item => item.Kategorie)
              ),
            ].map(item_outer => (
              <TableBody key={item_outer}>
                <TableRow>
                  <TableCell style={{ backgroundColor: 'black' }}>
                    <h4 style={{ color: 'white' }}>{item_outer}</h4>
                  </TableCell>
                  <TableCell style={{ backgroundColor: 'black' }} />
                  <TableCell style={{ backgroundColor: 'black' }} />
                </TableRow>
                {JSON.parse(Zellergebnisse)
                  .filter(item => item.Kategorie === item_outer)
                  .map(item => (
                    <TableRow key={item.Beschreibung}>
                      <TableCell>{item.Beschreibung}</TableCell>
                      <TableCell>
                        {typeof item.Wert !== 'string'
                          ? Math.round(item.Wert * 100) / 100
                          : item.Wert}
                      </TableCell>
                      <TableCell>{item.Einheit}</TableCell>
                    </TableRow>
                  ))}
              </TableBody>
            ))}
          </Table>
          {/* 
          <CSVLink
            {...csvReport}
            data={JSON.parse(Zellergebnisse)}
            separator=";">
            Excel-CSV Export
          </CSVLink>
          <br />
          <CSVLink {...csvReport} data={JSON.parse(Zellergebnisse)}>
            CSV Export
          </CSVLink>
          */}
        </div>
      )}
      <div className="bx--col-lg-2"></div>

      {Zellergebnisse !== null && (
        <div className="bx--col-lg-6">
          <h2>Graphen</h2>
          <div className="bx--row">
            <DonutChart data={donutData} options={donutOptions} />
            <div style={{height:500}}></div>

            <DonutChart data={costDonutData} options={costDonutOptions} />
          </div>
        </div>
      )}
    </>
  );
}
