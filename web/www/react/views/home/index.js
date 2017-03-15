// -*- jsx -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2017 all rights reserved
//

// externals
import React from 'react'

// locals
import styles from './styles'
import Splash from './splash'
import About from './about'
import Install from './install'

// declaration
const Home = () => (
    <div style={styles.home}>
        <Splash/>
        <main style={styles.main}>
            <About/>
            <Install/>
        </main>
    </div>
)

//   publish
export default Home

// end of file
