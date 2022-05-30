import { Button, ComposedModal, FormGroup, ModalBody, ModalHeader, TextInput } from "carbon-components-react";
import React, { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { login, login_admin } from './../../actions'

export default function LoginModal(props) {

    const [nutzername, setNutzername] = useState(null)
    const [passwort, setPasswort] = useState(null)

    const [nutzerdaten, setNutzerdaten] = useState(null)
    const dispatch = useDispatch();
    const logged = useSelector(state => state.loggedIn)
    const loggedAdmin = useSelector(state => state.loggedInAdmin)

    async function CheckLog() {
        const res = await fetch('/user_check', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                Nutzer: nutzername,
                Passwort: passwort
            }),
        });
        const data = await res.json();
        return data;
    }

    function Login() {
        CheckLog().then(result => setNutzerdaten(result))
    }

    useEffect(() => {
        nutzerdaten !== null &&
            nutzerdaten.StartzeitMS - Date.now() < 0 &&
            nutzerdaten.EndzeitMS + 86400000 - Date.now() > 0 &&
            dispatch(login(true)) &&
            nutzerdaten.Berechtigung === "Admin" &&
            dispatch(login_admin(true))

    }, [nutzerdaten])


    return (

        <ComposedModal open={props.open} onClose={props.close} >
            <ModalHeader title="Login" />
            <ModalBody >
                <p style={{ marginBottom: '1rem' }}>
                    Falls Sie keine Zugangsdaten haben oder Ihre Zugangsdaten abgelaufen sind, wenden Sie sich bitte an das Institut für Partikeltechnik (den Ersteller des Programms: k.bendzuck@tu-braunschweig.de).
                </p>
                <FormGroup legendText="Login" style={{ maxWidth: '400px' }}>
                    <TextInput
                        id="one"
                        labelText="Nutzername"
                        value={nutzername !== null ? nutzername : ""}
                        onChange={(event) => setNutzername(event.target.value)}
                    />
                    <TextInput
                        id="two"
                        labelText="Passwort"
                        type="password"
                        value={passwort !== null ? passwort : ""}
                        onChange={(event) => setPasswort(event.target.value)}
                    />
                    <Button style={{ marginTop: "20px" }} onClick={() => Login()}>
                        Login
                    </Button>
                    {logged === true && <h3>Erfolgreich eingeloggt!</h3>}
                </FormGroup>
            </ModalBody>
        </ComposedModal>
    )
}