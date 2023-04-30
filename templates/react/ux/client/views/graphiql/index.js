// -*- web -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// externals
import React from 'react'
import GraphiQL from 'graphiql'
import {{ createGraphiQLFetcher }} from '@graphiql/toolkit';


// render a {{graphiql}} view
export const GiQL = () => {{
    // make a fetcher
    const fetcher = createGraphiQLFetcher({{
        url: window.location.origin + '/graphql',
    }});

    // render
    return (
        <GraphiQL fetcher={{fetcher}} editorTheme={{'ambiance'}} />
    )
}}


// end of file
