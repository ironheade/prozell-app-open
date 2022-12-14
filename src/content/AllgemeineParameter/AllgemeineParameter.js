import React from 'react';
import { Breadcrumb, BreadcrumbItem } from 'carbon-components-react';
import AllgParameterTable from './components/allg_parameter_table';
import { useSelector, useDispatch } from 'react-redux';
import {
  gebaeude_state,
  oekonomische_parameter_state,
  mitarbeiter_logistik_state,
  rueckgewinnung_state,
} from './../../actions';

export default function AllgemeineParameter() {
  const dispatch = useDispatch();

  const oekonomischeParameter = useSelector(state => state.oekonomischeParameter);
  const mitarbeiterLogistik = useSelector(state => state.mitarbeiterLogistik);
  const gebaeude = useSelector(state => state.gebaeude);
  const rueckgewinnung = useSelector(state => state.rueckgewinnung)

  function onChange_oekonomisch(Beschreibung, neuerWert) {
    var prevIndex = JSON.parse(oekonomischeParameter).findIndex(
      item => item.Beschreibung === Beschreibung
    ); //index im State für das zu Ändernde Object
    let newState = [...JSON.parse(oekonomischeParameter)]; //shallow copy of old state
    let newObject = { ...newState[prevIndex] }; //shallow copy of specific Object
    newObject.Wert = neuerWert; //Prozentzahl anpassen
    newState[prevIndex] = newObject; //unter dem gleichen Index im neuen State überschreiben
    dispatch(oekonomische_parameter_state(JSON.stringify(newState)));
  }

  function onChange_mitarbeiter(Beschreibung, neuerWert) {
    var prevIndex = JSON.parse(mitarbeiterLogistik).findIndex(
      item => item.Beschreibung === Beschreibung
    ); //index im State für das zu Ändernde Object
    let newState = [...JSON.parse(mitarbeiterLogistik)]; //shallow copy of old state
    let newObject = { ...newState[prevIndex] }; //shallow copy of specific Object
    newObject.Wert = neuerWert; //Prozentzahl anpassen
    newState[prevIndex] = newObject; //unter dem gleichen Index im neuen State überschreiben
    dispatch(mitarbeiter_logistik_state(JSON.stringify(newState)));
  }

  function onChange_gebaeude(Beschreibung, neuerWert) {
    var prevIndex = JSON.parse(gebaeude).findIndex(
      item => item.Beschreibung === Beschreibung
    ); //index im State für das zu Ändernde Object
    let newState = [...JSON.parse(gebaeude)]; //shallow copy of old state
    let newObject = { ...newState[prevIndex] }; //shallow copy of specific Object
    newObject.Wert = neuerWert; //Prozentzahl anpassen
    newState[prevIndex] = newObject; //unter dem gleichen Index im neuen State überschreiben
    dispatch(gebaeude_state(JSON.stringify(newState)));
  }

  function onChange_rueckgewinnung(Beschreibung, neuerWert) {
    var prevIndex = JSON.parse(rueckgewinnung).findIndex(
      item => item.Beschreibung === Beschreibung
    ); //index im State für das zu Ändernde Object
    let newState = [...JSON.parse(rueckgewinnung)]; //shallow copy of old state
    let newObject = { ...newState[prevIndex] }; //shallow copy of specific Object
    newObject.Wert = neuerWert; //Prozentzahl anpassen
    newState[prevIndex] = newObject; //unter dem gleichen Index im neuen State überschreiben
    dispatch(rueckgewinnung_state(JSON.stringify(newState)));
  }

  return (
    <div className="bx--grid bx--grid--full-width allgemeine-parameter">
      <div className="bx--row __banner">
        <div className="bx--col-lg-16">
          <Breadcrumb noTrailingSlash aria-label="Page navigation">
            <BreadcrumbItem>
              <a href="/">Startseite</a>
            </BreadcrumbItem>
            <BreadcrumbItem>
              <a href="/#/AllgemeineParameter">Allgemeine Parameter</a>
            </BreadcrumbItem>
          </Breadcrumb>
          <h1 className="__heading">Allgemeine Parameter</h1>
        </div>
      </div>

      <div className="bx--row landing-page__r2">
        <div className="bx--col bx--no-gutter">
          <div className="bx--row">
            <div className="bx--col" style={{ marginTop: '50px' }}>
              <h1>Ökonomische Parameter</h1>
              <AllgParameterTable
                content={oekonomischeParameter}
                onChange={onChange_oekonomisch}
              />
            </div>
            <div className="bx--col" style={{ marginTop: '50px' }}>
              <h1>Mitarbeiter &amp; Logistik</h1>
              <AllgParameterTable
                content={mitarbeiterLogistik}
                onChange={onChange_mitarbeiter}
              />
            </div>
            <div className="bx--col" style={{ marginTop: '50px' }}>
              <h1>Gebäude</h1>
              <AllgParameterTable
                content={gebaeude}
                onChange={onChange_gebaeude}
              />
            </div>
            <div className="bx--col" style={{ marginTop: '50px' }}>
              <h1>Rückgewinnung</h1>
              <AllgParameterTable
                content={rueckgewinnung}
                onChange={onChange_rueckgewinnung}
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
