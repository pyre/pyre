# -*- coding: utf-8 -*-
#
# {project.authors}
# (c) {project.span} all rights reserved


# externals
import graphene
import json
# support
import {project.name}


# the {{graphql}} request handler
class GraphQL:


    # interface
    def respond(self, plexus, server, request, **kwds):
        """
        Resolve the {{query}} and generate a response for the client
        """
        # parse the {{request}} payload
        payload = json.loads(b'\n'.join(request.payload))
        # get the query
        query = payload.get("query")
        # there are also other fields that we don't care about just yet
        # operation = payload.get("operation")
        # variables = payload.get("variables")

        # execute the query
        result = self.schema.execute(query, context=self.context)

        # assemble the resulting document
        doc = {{ "data": result.data }}
        # in addition, if something went wrong
        if result.errors:
            # inform the client
            doc["errors"] = [ {{"message": error.message}} for error in result.errors ]

        # encode it using JSON and serve it
        return server.documents.JSON(server=server, value=doc)


    # metamethods
    def __init__(self, panel, **kwds):
        # chain up
        super().__init__(**kwds)

        # load my schema
        from .schema import schema
        # and attach it
        self.schema = schema

        # get the package metadata
        meta = {project.name}.meta
        # build the version info
        version = {{
            "major": meta.major,
            "minor": meta.minor,
            "micro": meta.micro,
            "revid": meta.revision,
        }}

        # set up the execution context
        self.context = {{
            "nameserver": panel.pyre_nameserver,
            "version": version
        }}

        # all done
        return


# end of file
