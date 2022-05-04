export const increment = () => {
  return {
    type: 'INCREMENT',
  };
};

export const decrement = () => {
  return {
    type: 'DECREMENT',
  };
};

export const reset = () => {
  return {
    type: 'RESET',
  };
};

export const logIn = () => {
  return {
    type: 'LOG_IN',
  };
};

export const logOut = () => {
  return {
    type: 'LOG_OUT',
  };
};

//meine actions

export const zellformat_change = zellformat => {
  return {
    type: 'ZELLFORMAT_CHANGE',
    payload: zellformat,
  };
};

export const alle_zellen_laden = alleZellen => {
  return {
    type: 'ALLE_ZELLEN_LADEN',
    payload: alleZellen,
  };
};

export const gebaeude_state = newState => {
  return {
    type: 'GEBAEUDE_STATE',
    payload: newState,
  };
};

export const oekonomische_parameter_state = newState => {
  return {
    type: 'OEKONOMISCHE_PARAMETER_STATE',
    payload: newState,
  };
};

export const mitarbeiter_logistik_state = newState => {
  return {
    type: 'MITARBEITER_LOGISTIK_STATE',
    payload: newState,
  };
};

export const zellformat_name_state = newState => {
  return {
    type: 'ZELLFORMATNAME_CHANGE',
    payload: newState,
  };
};

export const zellchemie_state = newState => {
  return {
    type: 'ZELLCHEMIE_CHANGE',
    payload: newState,
  };
};

export const zellchemie_name_state = newState => {
  return {
    type: 'ZELLCHEMIENAME_CHANGE',
    payload: newState,
  };
};

export const materialien_state = newState => {
  return {
    type: 'MATERIALIEN_CHANGE',
    payload: newState,
  };
};

export const materialinfos_state = newState => {
  return {
    type: 'MATERIALINFOS_CHANGE',
    payload: newState,
  };
};

export const zellmaterialien_state = newState => {
  return {
    type: 'ZELLMATERIALIEN_STATE',
    payload: newState,
  };
};

export const empty_reducer = newState => {
  return {
    type: 'EMPTY_REDUCER',
    payload: newState,
  };
};

export const prozessroute_change = newState => {
  return {
    type: 'PROZESSROUTE_CHANGE',
    payload: newState,
  };
};

export const zellergebnisse_change = newState => {
  return {
    type: 'ZELLERGEBNISSE_CHANGE',
    payload: newState,
  };
};

export const GWh_Jahr_Ah_Zelle_change = newState => {
  return {
    type: 'GWH_JAHR_AH_ZELLE_STATE',
    payload: newState,
  };
};

export const Prozessdaten_change = newState => {
  return {
    type: 'PROZESS_DATEN_CHANGE',
    payload: newState,
  };
};

export const currentZellFormate_change = newState => {
  return {
    type: 'CURRENTZELLFORMATE_REDUCER',
    payload: newState,
  };
};

export const ergebnisTabelle_change = newState => {
  return {
    type: 'ERGEBNIS_TABELLE',
    payload: newState,
  };
};

export const quellen = newState => {
  return {
    type: 'QUELLEN',
    payload: newState,
  };
};

