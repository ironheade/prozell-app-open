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
    return <img src={props.source} alt={props.alt} style={{ height: 200, marginTop: 35 }} />;
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
    <div className="bx--col-lg-14">

      <h3>Einleitung</h3>
      <p className="anleitungstext">Das vorliegende Programm ermöglicht die ökonomische Betrachtung einer Lithium-Ionen Batterie Produktion in großem Maßstab. Es führt den Nutzer über die Modellierung der Batterie, die Gestaltung der Produktionslinie, die Festlegung wichtiger Rahmenparameter hin zu den Ergebnissen. Im folgenden wird die Handhabung des Programms Schritt für Schritt erläutert.<br/><strong>Hinweis:</strong> Das Programm ist im Rahmen des eKoZell Projektes entstanden, gefördert durch das Bundesministerium für Bildung und Forschung. Eine Druckversion der Anleitung kann <a target="_blank" href='https://www.google.com/'>hier</a> heruntergeladen werden. Der Login um die Möglichkeiten des Programms nutzen zu können erfolgt über das Symbol oben rechts in der Ecke. Für Zugangsdaten wenden Sie sich an das Institut für Partikeltechnik (siehe Impressum).</p><br/>

      <h3>Zellauslegung</h3>
      <p className="anleitungstext">Die zu produzierende Zelle wird unter dem Reiter <strong>Zellauslegung</strong> modelliert. Die Modellierung ist grob unterteilt in äußere Parameter (Zelltyp, Abmaße der Zelle, Größe der Produktion) auf der linken Seite und die Wahl der Materialkomposition auf der rechten Seite.<br/><br/> Auf der linken Seite wird zunächst der Zellformat gewählt. Es stehen vier Zellformate zur Auswahl, zwei Arten gewickelte Zellen (Rundwickel und prismatischer Wickel) und zwei Arten gestapelter Zellen (mit fester Hülle und mit Pouchhülle), siehe <strong>Zellformate</strong>. Zunächst wird die Jahresproduktion in GWh angeben, bei gestapelten Pouchzellen wird noch die Ladung einer einzelnen Zelle in Ah festgelegt. Bei den anderen Zellformaten errechnet sich die Ladung mittels der festen Zellgröße und der Zellchemie. Nach der Wahl des Zellformats kann aus einer der vorgefertigten Varianten gewählt werden, z.B. der 18650 Zelle bei Rundzellen. Die zugehörigen Maßer können alle eingestellt werden, eine Erläuterung der verschiedenen Parameter befindet sich unter <strong>Zellformate</strong>.<br/><br/>
      Auf der rechten Seite wird zunächst eine vorgefertigte Zellchemie ausgewählt. Diese beschreibt, welche Materialien zu welchem Umfang in der zelle verwendet werden. Über das rote Minus Symbol können Materialien aus der Zelle entfernt werden, über die Dropdown Fenster können neue Materialien aus der Datenbank hinzugefügt werden. Die Mengen müssen sich zu 100% aufsummieren. Die Parameter zu den gewählten Materialien (z.B. Dicke des Separators oder spezifische Kapazität des Aktivmaterials) können weiter unten unter <strong>Materialdetails</strong> ausgewählt werden. Alle weiteren Parameter, die weder zu den Zellmaßen noch zu den Materialien zugeordnet werden können (z.B. Zellspannung) werden auf der rechten Seite unter <strong>weitere Parameter</strong> eingestellt. <br/><br/> Nachdem die Zelle ausgelegt ist, wird oben rechts ein Knopf mit der Aufschrift "Ergebnisse" freigeschaltet. Mit diesem Knopf wird die Zelle berechnet und das Programm springt direkt zu den Ergebnissen. Dort werden alle Ergebnisse auf der linken Seite in Tabellenform festgehalten. Auf der rechten Seite wird mit Hilfe von Donut-Diagrammen die Mengen- und Kostenverteilung innerhalb einer Zelle dargestellt. Die Kostenverteilung weicht dabei leicht ab von der Verteilung der für die Jahresproduktion verwendeten Materialien, da für unterschiedliche Materialien unterschiedliche Verluste auftreten (z.B. unterliegt die Suspension allen Verlusten, da sie früh in der Produktion hinzugefügt wird, das Elektrolyt weniger Verlusten, da es später hinzugefügt wird). 
      </p><br/>

      <h3>Zellformate</h3>
      <div className="bx--row">

        <div className="bx--col-lg-8">
          <img alt="wickel_hardcase" src={wickel_hardcase} style={{ height: 500, marginTop: 35 }} />
          <figcaption><h4>Hardcase gewickelt</h4></figcaption>
        </div>

        <div className="bx--col-lg-8">
          <img alt="rundzelle" src={rundzelle} style={{ height: 500, marginTop: 35 }} />
          <figcaption><h4>Rundzelle</h4></figcaption>
        </div>

        <div className="bx--col-lg-8">
          <img alt="stapel_hardcase" src={stapel_hardcase} style={{ height: 400, marginTop: 35 }} />
          <figcaption><h4>Hardcase gestapelt</h4></figcaption>
        </div>

        <div className="bx--col-lg-8">
          <img alt="stapel_pouch" src={stapel_pouch} style={{ height: 300, marginTop: 35 }} />
          <figcaption><h4>Pouchzelle gestapelt</h4></figcaption>
        </div>

      </div><br/>

      <h3>Prozessauslegung</h3>
      <p className="anleitungstext">
      Die Prozesskette wird unter dem Reiter <strong>Prozessauslegung</strong> festgelegt. Auf der linken Seite befindet sich die aktuelle Prozesskette, aufgeteilt in verschiedene Abschnitte der Produktion. Eingefügte Prozessschritte können über das rote Minus entfernt werden. In der Mitte befinden sich alle zur Verfügung stehenden Prozessschritte, welche mit dem blauen Plus zur aktuellen Prozesskette hinzugefügt werden können. Dopplungen sind nicht möglich. Alternativ kann auch eine vorgefertigte Prozessroute über das Dropdown Menü oben rechts im Fenster ausgewählt werden. Nachdem ein Prozessschritt hinzugefügt wurde, erscheint er auf der rechten Seite und kann ausgeklappt werden, um alle Parameter des Prozessschrittes einstellen zu können. Diese umfassen Produktionsparameter, wie den Durchsatz, den Stromverbrauch oder die Flächennutzung.
      </p><br/>

      <h3>Allgemeine Paramter</h3>
      <p className="anleitungstext">
      Weitere Parameter zur Produktion, die weder zur Zelle noch zu den Prozessschritten zugeordnet werden können, werden unter dem Reiter <strong>Allgemeine Paramter</strong> eingestellt. Diese sind unterteilt in vier Abschnitte:
      <ul style={{listStyleType:"square",marginLeft:"20px"}}>
        <li><strong>Ökonomische Parameter: </strong>Allgemeine ökonomische Parameter</li>
        <li><strong>Mitarbeiter & Logistik: </strong>Parameter zu Mitarbeiter und Logistik, wie z.B. die Arbeitszeiten oder die Mitarbeiterkosten</li>
        <li><strong>Gebäude: </strong>Flächenkosten und Aufschläge für Zusatzflächen</li>
        <li><strong>Rückgewinnung: </strong>Prozentsatz des Materials, das vom Verlustmaterial über die Produktion wieder zurückgewonnen werden kann</li>
      </ul>
      </p><br/>

      <h3>Ergebnisse</h3>
      <p className="anleitungstext">Nachdem alle die Zellmodellierung und Prozessauslegung abgeschlossen sind, erscheint unter dem Reiter <strong>Ergebnisse</strong> ein Knopf mit der Aufschrift "Ergebnisse". Mit diesem werden die Ergebnisse errechnet und dargestellt. Es erscheinen zunächst zwei Balkendiagramme. </p><br/>
      </div> 
    <Spacer />

      <div className="bx--col-lg-16">

        <h3>Maße auf Coil</h3>

        <div className="bx--row">

          <div className="bx--col-lg-8">
            <img alt="coil_stapel" src={coil_stapel} style={{ height: 300, marginTop: 35 }} />
            <figcaption><h4>Coil Wickelzelle</h4></figcaption>
          </div>

          <div className="bx--col-lg-8">
            <img alt="coil_wickel" src={coil_wickel} style={{ height: 260, marginTop: 35 }} />
            <figcaption><h4>Coil Stapelzelle</h4></figcaption>
          </div>

        </div>

        <br />
        <h3>Wiederholeinheit</h3>

        <div className="bx--row">

          <div className="bx--col-lg-8">
            <img alt="whe" src={whe} style={{ height: 260, marginTop: 35 }} />
            <figcaption><h4>Wiederholeinheit</h4></figcaption>
          </div>

          <div className="bx--col-lg-8">
            <img alt="abstand" src={abstand} style={{ height: 300, marginTop: 35 }} />
            <figcaption><h4>Abstände Wiederholeinheit</h4></figcaption>
          </div>

        </div>

        <br />
        <h3>Einzelsheet</h3>

        <div className="bx--row">

          <div className="bx--col-lg-6">
            <img alt="sheet_stapel" src={sheet_stapel} style={{ height: 300, marginTop: 35 }} />
            <figcaption><h4>Blatt Stapelzelle</h4></figcaption>
          </div>

          <div className="bx--col-lg-8">
            <img alt="sheet_wickel" src={sheet_wickel} style={{ height: 190, marginTop: 35 }} />
            <figcaption><h4>Blatt Wickelzelle</h4></figcaption>
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
