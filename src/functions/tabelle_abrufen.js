 export default async function tabelle_abrufen(tabelle_dateiname) {
    const res = await fetch('/tabelle_abrufen', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        tabelle: tabelle_dateiname,
      }),
    });
    const data = await res.json();
    return data.tabelle;
  }