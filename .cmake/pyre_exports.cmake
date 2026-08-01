# -*- cmake -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# record an external package that one of our exported targets names in its link interface
# {package} is what to look for, {target} is the imported target the search must produce, and
# the remaining arguments are handed to {find_dependency} verbatim
function(pyre_exportRequirement package target)
  # find out whether the package configuration file has already been rendered
  get_property(sealed GLOBAL PROPERTY PYRE_EXPORT_SEALED)
  # if it has, this requirement would never reach the installed file
  if(sealed)
    # so complain loudly instead of shipping a package nobody can consume
    message(FATAL_ERROR
      "'${package}' joined an exported link interface after the {pyre} package configuration "
      "was rendered; move the {pyre_exportRequirement} call ahead of {pyre_exportRequirements}")
  endif()
  # flatten the search arguments into a single blank separated string so the entry survives
  # the trip through the property as one piece
  string(REPLACE ";" " " arguments "${ARGN}")
  # and stash it
  set_property(GLOBAL APPEND PROPERTY PYRE_EXPORT_REQUIREMENTS "${package} ${target} ${arguments}")
  # all done
endfunction(pyre_exportRequirement)


# verify that every external package our exported targets name has been recorded, render the
# recorded requirements as cmake code, and hand the text back through {variable}
function(pyre_exportRequirements variable)
  # retrieve what the build recorded
  get_property(requirements GLOBAL PROPERTY PYRE_EXPORT_REQUIREMENTS)

  # the imported targets we know how to resolve, and the code that resolves them
  set(known "")
  set(text "")
  # go through the requirements in the order they were recorded
  foreach(requirement IN LISTS requirements)
    # take the entry apart
    string(REPLACE " " ";" fields "${requirement}")
    # the first two fields name the package and the imported target it must produce
    list(POP_FRONT fields package target)
    # and whatever is left is the argument list for the search
    list(JOIN fields " " arguments)
    # remember the target so the audit below can account for it
    list(APPEND known ${target})
    # emit the search itself
    string(APPEND text "find_dependency(${package} ${arguments})\n")
    # a successful search is not proof that the imported target exists: a consumer running with
    # {CMAKE_FIND_PACKAGE_PREFER_CONFIG} can resolve the package's own configuration file, which
    # may well publish the target under a different name; catch that here, while we can still
    # say something useful, rather than at the consumer's generate step
    string(APPEND text "if(NOT TARGET ${target})\n")
    string(APPEND text "  set(pyre_FOUND FALSE)\n")
    string(APPEND text "  set(pyre_NOT_FOUND_MESSAGE\n")
    string(APPEND text
      "      \"{pyre} was built against ${package}, but locating it did not define the imported "
      "target '${target}' that the {pyre} targets name; check whether "
      "CMAKE_FIND_PACKAGE_PREFER_CONFIG is steering the search towards a different "
      "${package} package\")\n")
    string(APPEND text "  return()\n")
    string(APPEND text "endif()\n")
  endforeach()

  # now audit the exported targets: anything they name that we cannot resolve is a target the
  # consumer will be asked to supply, and the whole point of the exercise is that it shouldn't
  foreach(exported pyre journal)
    # collect the link interface
    get_target_property(interface ${exported} INTERFACE_LINK_LIBRARIES)
    # an empty interface has nothing to answer for
    if(NOT interface)
      continue()
    endif()
    # otherwise, look at each entry
    foreach(dependency IN LISTS interface)
      # a private link on a static library rides along wrapped, and would still have to be
      # resolved by the consumer; unwrap it so it gets the same scrutiny as the rest
      string(REGEX REPLACE "^\\$<LINK_ONLY:(.*)>$" "\\1" dependency "${dependency}")
      # only namespaced imported targets place a burden on the consumer
      if(NOT dependency MATCHES "^([A-Za-z0-9_+.-]+)::")
        continue()
      endif()
      # and our own are resolved by the targets file itself
      if(CMAKE_MATCH_1 STREQUAL "pyre")
        continue()
      endif()
      # everything else must have been recorded at the point of the link
      if(NOT dependency IN_LIST known)
        message(FATAL_ERROR
          "the exported target '${exported}' names the imported target '${dependency}', but "
          "nothing taught the {pyre} package configuration how to find it; add a matching "
          "{pyre_exportRequirement} call next to the {target_link_libraries} that introduced it")
      endif()
    endforeach()
  endforeach()

  # refuse any further recording, so a link established after this point cannot slip past the
  # file we are about to render
  set_property(GLOBAL PROPERTY PYRE_EXPORT_SEALED TRUE)
  # publish the rendered text
  set(${variable} "${text}" PARENT_SCOPE)
  # all done
endfunction(pyre_exportRequirements)


# end of file
