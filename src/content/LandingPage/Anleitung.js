import React from 'react';

import Oberfläche from '../../resources/Anleitung_icons/interface.svg';
import searching from '../../resources/Anleitung_icons/searching.svg';
import services from '../../resources/Anleitung_icons/services.svg';
import sharing from '../../resources/Anleitung_icons/sharing.svg';

import abstand from '../../resources/Anleitung_icons/abstand.png';
import coil_stapel from '../../resources/Anleitung_icons/coil_stapel.png';
import coil_wickel from '../../resources/Anleitung_icons/coil_wickel.png';
import rundzelle from '../../resources/Anleitung_icons/rundzelle.png';
import sheet_stapel from '../../resources/Anleitung_icons/sheet_stapel.png';
import sheet_wickel from '../../resources/Anleitung_icons/sheet_wickel.png';
import stapel_hardcase from '../../resources/Anleitung_icons/stapel_hardcase.png';
import stapel_pouch from '../../resources/Anleitung_icons/stapel_pouch.png';
import whe from '../../resources/Anleitung_icons/whe.png';
import wickel_hardcase from '../../resources/Anleitung_icons/wickel_hardcase.png';

export default function Anleitung() {
  function Spacer() {
    return <div style={{ height: 400 }} />;
  }

  function Img(props) {
    return <img src={props.source} style={{ height: 200, marginTop: 35 }} />;
  }

  const Legende = [
    { id: 1, Beschreibung: 'Länge Zellfähnchen Anode/Kathode', Einheit: 'mm' },
    { id: 2, Beschreibung: 'Breite Zellfähnchen Anode/Kathode', Einheit: 'mm' },
    { id: 3, Beschreibung: 'Eckenradius', Einheit: 'mm' },
    { id: 4, Beschreibung: 'Länge Anode/Kathode', Einheit: 'mm' },
    { id: 5, Beschreibung: 'Breite Anode/Kathode', Einheit: 'mm' },
    { id: 6, Beschreibung: 'Länge Ableiter in Zelle Anode/Kathode', Einheit: 'mm' },
    { id: 7, Beschreibung: 'Beschichtungsabstand Anode/Kathode', Einheit: 'mm' },
    { id: 8, Beschreibung: 'Beschichtungshöhe Anode/Kathode', Einheit: 'mm' },
    { id: 9, Beschreibung: 'Überstand Anode - Kathode', Einheit: 'mm' },
    { id: 10, Beschreibung: 'Überstand Separator - Anode', Einheit: 'mm' },
    { id: 11, Beschreibung: 'Abstand Separator - Hülle', Einheit: 'mm' },
    { id: 12, Beschreibung: 'Sicherheitsabstand Schneiden', Einheit: 'mm' },
    { id: 13, Beschreibung: 'Beschichtungsabstand Anode/Kathode quer zur Bahn', Einheit: 'mm' },
    { id: 14, Beschreibung: 'Beschichtungsabstand Anode/Kathode in Bahnrichtung', Einheit: 'mm' },
    { id: 15, Beschreibung: 'Breite Festhülle', Einheit: 'mm' },
    { id: 16, Beschreibung: 'Länge Festhülle', Einheit: 'mm' },
    { id: 17, Beschreibung: 'Höhe Festhülle', Einheit: 'mm' },
    { id: 18, Beschreibung: 'Abstand Zellwickel - Deckel', Einheit: 'mm' },
    { id: 19, Beschreibung: 'Abstand Ableiter - Hülle', Einheit: 'mm' },
    { id: 20, Beschreibung: 'Radius Wickelkern', Einheit: 'mm' },
    { id: 21, Beschreibung: 'Breite Wickelkern', Einheit: 'mm' },
    { id: 22, Beschreibung: 'Zusatzwicklungen Separator (innen und außen)', Einheit: '-' },
    { id: 23, Beschreibung: 'Höhe Rundzelle', Einheit: 'mm' },
    { id: 24, Beschreibung: 'Radius Rundzelle', Einheit: 'mm' },
    { id: 25, Beschreibung: 'Wandstärke', Einheit: 'mm' }

  ]

  return (
    <>
      <div className="bx--col-lg-16" />
      <div className="bx--col-lg-9">
        <h3>Einleitung</h3>
        <p className="anleitungstext">
          Das vorliegende Programm vereinfacht die Kostenbetrachtung in der
          Batteriezellproduktion im großen Maßstab. Es ermöglicht die Gestaltung
          einer Lithium-Ionen Batterie aus einer der vorgegeben Zellbautypen,
          die anschließende Auslegung der Produktionsroute und nach einem
          letzten Blick auf allgemeine Parameter die Betrachtung der Ergebnisse.
          Dabei ist es nicht notwendig, die entsprechenden Punkte in der
          Kopfzeile von links nach Rechts zu bearbeiten. Im Folgenden werden die
          wichtigsten Auswahlmöglichkeiten des Programms erläutert.
        </p>
      </div>
      <div className="bx--col-lg-5 centerbox">
        <Img source={Oberfläche} />
      </div>
      <Spacer />

      <div className="bx--col-lg-5 centerbox">
        <Img source={searching} />
      </div>

      <div className="bx--col-lg-9">
        <h3>Zellauslegung</h3>
        <p className="anleitungstext">
          Die Zellauslegung beginnt mit der Auswahl des Zelltyps mittels eines
          Dropdown Fensters auf der linken Seite. Zur Auswahl stehen dabei{' '}
          <span style={{ fontWeight: 'bold' }}>
            Pouchzellen, Hardcase Zellen Rundzellen
          </span>{' '}
          und <span style={{ fontWeight: 'bold' }}>Prismatische Zellen</span>.
          Anschließend kann eine der vorgefertigten Zellen ausgewählt und
          angepasst werden. Als nächstes wird die Größe der Jahresproduktion in
          GWH/Jahr und, für Pouchzellen, die Ladung in Ah/Zelle angegeben.{' '}
          <br /> Auf der rechten Seite werden die Zusammensetzung und Chemie der
          Zelle festgelegt. Zunächst wird aus dem entsprechenden Dropdown
          Fenster eine der vorgefertigten Zellchemien ausgewählt. Im ersten
          Abschnitt
        </p>
      </div>

      <Spacer />

      <div className="bx--col-lg-9">
        <h3>Prozessauslegung</h3>
        <p className="anleitungstext">
          Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam
          nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat,
          sed diam voluptua. At vero eos et accusam et justo duo dolores et ea
          rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem
          ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur
          sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et
          dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam
          et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea
          takimata sanctus est Lorem ipsum dolor sit amet.
        </p>
      </div>
      <div className="bx--col-lg-5 centerbox">
        <Img source={services} />
      </div>
      <Spacer />

      <div className="bx--col-lg-5 centerbox">
        <Img source={sharing} />
      </div>

      <div className="bx--col-lg-9">
        <h3>Allgemeine Parameter</h3>
        <p className="anleitungstext">
          Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam
          nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat,
          sed diam voluptua. At vero eos et accusam et justo duo dolores et ea
          rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem
          ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur
          sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et
          dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam
          et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea
          takimata sanctus est Lorem ipsum dolor sit amet.
        </p>

      </div>
      <div className="bx--col-lg-16">
        <br />
        <h3>Zelltypen</h3>

        <div className="bx--row">

          <div className="bx--col-lg-8">
            <img src={wickel_hardcase} style={{ height: 500, marginTop: 35 }} />
            <figcaption>Hardcase gewickelt</figcaption>
          </div>

          <div className="bx--col-lg-8">
            <img src={rundzelle} style={{ height: 500, marginTop: 35 }} />
            <figcaption>Rundzelle</figcaption>
          </div>

          <div className="bx--col-lg-8">
            <img src={stapel_hardcase} style={{ height: 400, marginTop: 35 }} />
            <figcaption>Hardcase gestapelt</figcaption>
          </div>

          <div className="bx--col-lg-8">
            <img src={stapel_pouch} style={{ height: 300, marginTop: 35 }} />
            <figcaption>Pouchzelle gestapelt</figcaption>
          </div>

        </div>

        <br />
        <h3>Maße auf Coil</h3>

        <div className="bx--row">

          <div className="bx--col-lg-8">
            <img src={coil_stapel} style={{ height: 300, marginTop: 35 }} />
            <figcaption>Coil Wickelzelle</figcaption>
          </div>

          <div className="bx--col-lg-8">
            <img src={coil_wickel} style={{ height: 260, marginTop: 35 }} />
            <figcaption>Coil Stapelzelle</figcaption>
          </div>

        </div>

        <br />
        <h3>Wiederholeinheit</h3>

        <div className="bx--row">

          <div className="bx--col-lg-8">
            <img src={whe} style={{ height: 260, marginTop: 35 }} />
            <figcaption>Wiederholeinheit</figcaption>
          </div>

          <div className="bx--col-lg-8">
            <img src={abstand} style={{ height: 300, marginTop: 35 }} />
            <figcaption>Abstände Wiederholeinheit</figcaption>
          </div>

        </div>

        <br />
        <h3>Einzelsheet</h3>

        <div className="bx--row">

          <div className="bx--col-lg-6">
            <img src={sheet_stapel} style={{ height: 300, marginTop: 35 }} />
            <figcaption>Blatt Stapelzelle</figcaption>
          </div>

          <div className="bx--col-lg-8">
            <img src={sheet_wickel} style={{ height: 190, marginTop: 35 }} />
            <figcaption>Blatt Wickelzelle</figcaption>
          </div>

        </div>

      </div>
      <div className="bx--row">

        <div className="bx--col-lg-16">
          <br />
          <h3>Legende</h3>
          <ol>
            {
              Legende.map(item =>

                <li key={item.id}>{item.id}. {item.Beschreibung} [{item.Einheit}]</li>

              )
            }
          </ol>
        </div>
      </div>
    </>
  );
}
