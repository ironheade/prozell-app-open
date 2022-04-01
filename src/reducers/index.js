import authReducer from './authReducer';
import zellformatReducer from './zellformatReducer';
import alleZellenReducer from './alleZellenReducer';
import oekonomischeParameterReducer from './oekonomischeParameterReducer';
import mitarbeiterLogistikReducer from './mitarbeiterLogistikReducer';
//import gebaeudeReducer from './gebaeudeReducer';
import zellformatNameReducer from './zellformatNameReducer';
//import zellchemieReducer from './zellchemieReducer';
import zellchemieNameReducer from './zellchemieNameReducer';
import materialInfosReducer from './materialInfosReducer';
import zellmaterialienReducer from './zellmaterialienReducer';
import emptyReducer from './emptyReducer';
import prozessRouteReducer from './prozessRouteReducer'
import zellergebnisseReducer from './zellergebnisseReducer'
import GWH_Jahr_AH_ZelleReducer from './GWH_Jahr_AH_ZelleReducer'
import prozessschrittDatenReducer from './prozessschrittDatenReducer'
import currentZellformateReducer from'./currentZellformateReducer'
import * as reducer from './reducers.js'
import { combineReducers } from 'redux';



const rootreducer = combineReducers({
  auth: authReducer,
  zellformat: zellformatReducer,
  alleZellen: alleZellenReducer,
  oekonomischeParameter: oekonomischeParameterReducer,
  mitarbeiterLogistik: mitarbeiterLogistikReducer,
  gebaeude: reducer.gebaeudeReducer,
  zellformatName: zellformatNameReducer,
  zellchemie: reducer.zellchemieReducer,
  zellchemieName: zellchemieNameReducer,
  zellergebnisse: zellergebnisseReducer,
  materialInfos: materialInfosReducer,
  zellmaterialien: zellmaterialienReducer,
  empty: emptyReducer,
  prozessRoute: prozessRouteReducer,
  GWH_Jahr_AH_Zelle: GWH_Jahr_AH_ZelleReducer,
  prozessschrittDaten: prozessschrittDatenReducer,
  currentZellformate: currentZellformateReducer
});

export default rootreducer;
