
import bild from '../../resources/process_icons/assemblieren.png'
import Oberfläche from '../../resources/Anleitung_icons/interface.svg'
import searching from '../../resources/Anleitung_icons/searching.svg'
import services from '../../resources/Anleitung_icons/services.svg'
import sharing from '../../resources/Anleitung_icons/sharing.svg'

export default function Anleitung() {

    function Spacer() {
        return (<div style={{ height: 400 }}></div>)
    }

    function Img(props) {
        return (<img src={props.source} style={{ height: 200, marginTop: 35 }} />)
    }

    return (
        <>
            <div className="bx--col-lg-16"></div>
            <div className="bx--col-lg-9">
                <h3>Einleitung</h3>
                <p className='anleitungstext'>
                    Das vorliegende Programm vereinfacht die Kostenbetrachtung in der Batteriezellproduktion im großen Maßstab. Es ermöglicht die Gestaltung einer Lithium-Ionen Batterie aus einer der vorgegeben Zellbautypen, die anschließende Auslegung der Produktionsroute und nach einem letzten Blick auf allgemeine Parameter die Betrachtung der Ergebnisse. Dabei ist es nicht notwendig, die entsprechenden Punkte in der Kopfzeile von links nach Rechts zu bearbeiten. Im Folgenden werden die wichtigsten Auswahlmöglichkeiten des Programms erläutert.
                </p>
            </div>
            <div className="bx--col-lg-5 centerbox" >
                <Img source={Oberfläche} />
            </div>
            <Spacer />

            <div className="bx--col-lg-5 centerbox" >
                <Img source={searching} />
            </div>

            <div className="bx--col-lg-9">
                <h3>Zellauslegung</h3>
                <p className='anleitungstext'>
                    Die Zellauslegung beginnt mit der Auswahl des Zelltyps mittels eines Dropdown Fensters auf der linken Seite. Zur Auswahl stehen dabei <span style={{fontWeight: 'bold'}}>Pouchzellen, Hardcase Zellen Rundzellen</span> und <span style={{fontWeight: 'bold'}}>Prismatische Zellen</span>. Anschließend kann eine der vorgefertigten Zellen ausgewählt und angepasst werden.  Als nächstes wird die Größe der Jahresproduktion in GWH/Jahr und, für Pouchzellen, die Ladung in Ah/Zelle angegeben. <br/> Auf der rechten Seite werden die Zusammensetzung und Chemie der Zelle festgelegt. Zunächst wird aus dem entsprechenden Dropdown Fenster eine der vorgefertigten Zellchemien ausgewählt. Im ersten Abschnitt
                </p>
            </div>

            <Spacer />

            <div className="bx--col-lg-9">
                <h3>Prozessauslegung</h3>
                <p className='anleitungstext'>
                    Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.
                </p>
            </div>
            <div className="bx--col-lg-5 centerbox" >
                <Img source={services} />
            </div>
            <Spacer />

            <div className="bx--col-lg-5 centerbox" >
                <Img source={sharing} />
            </div>

            <div className="bx--col-lg-9">
                <h3>Allgemeine Parameter</h3>
                <p className='anleitungstext'>
                    Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.
                </p>
            </div>

        </>
    )
}