// -*- web -*-
//
// {project.authors}
// (c) {project.span} all rights reserved


// the component framework
import React, {{ Suspense }} from 'react'
import ReactDOM from 'react-dom'
// relay
import {{ RelayEnvironmentProvider }} from 'react-relay/hooks'
// routing
import {{ BrowserRouter as Router, Routes, Route }} from 'react-router-dom'
// generator support
import 'regenerator-runtime'


// locals
// styles
import styles from './styles'
// context
import {{ environment }} from '~/context'
// views
import {{
    // graphiql
    GiQL,
    // the main page
    Main,
    // boilerplate
    Loading, NYI, Stop,
}} from '~/views'


// the app layout
const {project.capname}App = () => {{
    // page layout and top-level, disrupting, navigation
    // the app renders a client area over a status bar; most urls render the normal ui, but
    // - /stop: the user clicked on the "kill the server" action; show a "close this window" page
    // - /loading: shown while the app is fetching itself from the server

    // render
    return (
        <Routes >
            {{/* the app */ }}
            <Route path="/" element={{<Main />}} >
                {{/* specific activities */ }}
                <Route path="experiment" element={{<NYI />}} />
                <Route path="help" element={{<NYI />}} />
                <Route path="about" element={{<NYI />}} />

                {{/* the default page */ }}
                <Route index element={{<NYI />}} />
            </Route>

            {{/* meta navigation */ }}
            {{/* the closing page */ }}
            <Route path="/stop" element={{<Stop />}} />
            {{/* the page to render while waiting for data to arrive */ }}
            <Route path="/loading" element={{<Loading />}} />


            {{/* the graphiql sandbox */ }}
            <Route path="/graphiql" element={{<GiQL />}} />
        </Routes>
    )
}}


// the outer component that sets up access to the {{relay}}, {{suspense}},
// and {{router}} environments
const Root = () => (
    <RelayEnvironmentProvider environment={{ environment }}>
        <Suspense fallback={{< Loading />}}>
            <Router>
                <{project.capname}App />
            </Router>
    </Suspense>
    </RelayEnvironmentProvider >
)


// render
ReactDOM.render(<Root />, document.getElementById('{project.name}'))


// end of file
