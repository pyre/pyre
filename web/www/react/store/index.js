// -*- jsx -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2017 all rights reserved
//

// externals
import { createStore as createReduxStore, combineReducers, compose } from 'redux'
import { responsiveStoreEnhancer, calculateResponsiveState } from 'redux-responsive'

// locals
import browser from './browser'

// assemble my reducers
const reducer = combineReducers({
    browser,
})

// my store factory
const createStore = () => createReduxStore(
    reducer,
    compose(
        responsiveStoreEnhancer,
    )
)

// my store
const store = createStore()

// make sure we track the window as it changes size
window.addEventListener('resize', () =>
    // update the redux store
    store.dispatch(calculateResponsiveState(window))
)

// publish
export default store

// end of file
