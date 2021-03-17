// -*- web -*-
//
// {project.authors}
// (c) {project.span} all rights reserved


import 'regenerator-runtime'
// the component framework
import React, {{ Suspense }} from 'react'
import ReactDOM from 'react-dom'
// relay
import {{ RelayEnvironmentProvider }} from 'react-relay/hooks'
// routing
import {{ BrowserRouter as Router, Switch, Route }} from 'react-router-dom'
// generator support
import 'regenerator-runtime'


// locals
// styles
import styles from './styles'
// context
import {{ environment }} from '~/context'
// views
import {{
    // the main page
    Main,
    // boilerplate
    Loading, Stop,
    // layout
    Status,
}} from '~/views'


// the app layout
const {project.capname}App = () => {{
    // page layout and top-level, disrupting, navigation
    // the app renders a client area over a status bar; most urls render the normal ui, but
    // - /stop: the user clicked on the "kill the server" action; show a "close this window" page
    // - /loading: shown while the app is fetching itself from the server

    // render
    return (
        <div style={{styles.page}}>
            <Switch >
                {{/* the closing page */}}
                <Route path="/stop" component={{Stop}} />
                {{/* the page to render while waiting for data to arrive */}}
                <Route path="/loading" component={{Loading}} />

                {{/* show the app */}}
                <Route path="/" component={{Main}} />
            </Switch>
            <Status />
        </div>
    )
}}


// the outer component that sets up access to the {{relay}}, {{suspense}}, and {{router}} environments
const Root = () => (
    <RelayEnvironmentProvider environment={{environment}}>
        <Suspense fallback={{<Loading />}}>
            <Router>
                <{project.capname}App />
            </Router>
        </Suspense>
    </RelayEnvironmentProvider>
)


// render
ReactDOM.unstable_createRoot(document.getElementById('{project.name}')).render(<Root />)


// end of file
