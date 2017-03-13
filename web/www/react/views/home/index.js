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
import About from './about'
import Splash from './splash'

// declaration
const Home = () => (
    <div style={styles.home}>
        <Splash/>
        <main style={styles.main}>
            <About/>
        </main>
    </div>
)

//   publish
export default Home

// end of file
