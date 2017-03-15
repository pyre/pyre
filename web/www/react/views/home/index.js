// -*- jsx -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2017 all rights reserved
//

// externals
import React from 'react'
import { Switch, Route } from 'react-router-dom'

// locals
import styles from './styles'
import Splash from './splash'
import About from './about'
import Install from './install'


// assemble the default view
const Default = () => (
    <div>
        <Splash/>
        <About/>
    </div>
)

// declaration
const Home = () => (
    <main style={styles.main}>
        <Switch>
            <Route exact path="/" component={Default}/>
            <Route path="/about" component={About}/>
            <Route path="/install" component={Install}/>
            <Route component={Default}/>
        </Switch>
    </main>
)

//   publish
export default Home

// end of file
