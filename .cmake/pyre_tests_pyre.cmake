# -*- cmake -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2020 all rights reserved
#


#
# pyre/primitives
#
pyre_test_python_testcase(pyre/primitives/sanity.py)
pyre_test_python_testcase(pyre/primitives/path_arithmetic.py)
pyre_test_python_testcase(pyre/primitives/path_parts.py)
pyre_test_python_testcase(pyre/primitives/path_resolution.py)
pyre_test_python_testcase(pyre/primitives/path_tuple.py)

# the {path_resolution} test requires setup+cleanup
# the setup involves making a directory with a bunchof symbolic links
set(scratch_setup
  "rm -rf scratch; mkdir scratch; cd scratch; ln -s . here; ln -s .. up"
  "ln -s cycle cycle; ln -s $(pwd)/loop loop; ln -s $(pwd)/cycle ramp"
  "ln -s tic toc; ln -s toc tic"
  )
# to cleanup, just remove the scratch directory
set(scratch_cleanup
  "rm -rf scratch"
  )
pyre_test_testcase_shell_fixture(
  "${scratch_setup}" "${scratch_cleanup}"
  pyre/primitives/path_resolution.py
  )


#
# pyre/patterns
#
pyre_test_python_testcase(pyre/patterns/sanity.py)
pyre_test_python_testcase(pyre/patterns/powerset.py)
pyre_test_python_testcase(pyre/patterns/classifier.py)
pyre_test_python_testcase(pyre/patterns/extent.py)
pyre_test_python_testcase(pyre/patterns/named.py)
pyre_test_python_testcase(pyre/patterns/observable.py)
pyre_test_python_testcase(pyre/patterns/pathhash.py)
pyre_test_python_testcase(pyre/patterns/singleton.py)


#
# pyre/grid
#
pyre_test_python_testcase(pyre/grid/sanity.py)
pyre_test_python_testcase(pyre/grid/tile.py)
pyre_test_python_testcase(pyre/grid/grid.py)


#
# pyre/parsing
#
pyre_test_python_testcase(pyre/parsing/sanity.py)
pyre_test_python_testcase(pyre/parsing/exceptions.py)
pyre_test_python_testcase(pyre/parsing/scanner.py)
pyre_test_python_testcase(pyre/parsing/lexing.py)
pyre_test_python_testcase(pyre/parsing/lexing_tokenizationError.py)


#
# pyre/units
#
pyre_test_python_testcase(pyre/units/sanity.py)
pyre_test_python_testcase(pyre/units/exceptions.py)
pyre_test_python_testcase(pyre/units/one.py)
pyre_test_python_testcase(pyre/units/algebra.py)
pyre_test_python_testcase(pyre/units/parser.py)
pyre_test_python_testcase(pyre/units/formatting.py)


#
# pyre/filesystem
#
pyre_test_python_testcase(pyre/filesystem/sanity.py)
pyre_test_python_testcase(pyre/filesystem/exceptions.py)
pyre_test_python_testcase(pyre/filesystem/node.py)
pyre_test_python_testcase(pyre/filesystem/folder.py)
pyre_test_python_testcase(pyre/filesystem/filesystem.py)
pyre_test_python_testcase(pyre/filesystem/directory_walker.py)
pyre_test_python_testcase(pyre/filesystem/stat_recognizer.py)
pyre_test_python_testcase(pyre/filesystem/virtual.py)
pyre_test_python_testcase(pyre/filesystem/virtual_leaks.py)
pyre_test_python_testcase(pyre/filesystem/virtual_insert.py)
pyre_test_python_testcase(pyre/filesystem/virtual_insert_multiple.py)
pyre_test_python_testcase(pyre/filesystem/virtual_insert_badNode.py)
pyre_test_python_testcase(pyre/filesystem/virtual_find.py)
pyre_test_python_testcase(pyre/filesystem/virtual_subscripts.py)
pyre_test_python_testcase(pyre/filesystem/virtual_access.py)
pyre_test_python_testcase(pyre/filesystem/virtual_info.py)
pyre_test_python_testcase(pyre/filesystem/local.py)
pyre_test_python_testcase(pyre/filesystem/local_leaks.py)
pyre_test_python_testcase(pyre/filesystem/local_find.py)
pyre_test_python_testcase(pyre/filesystem/local_open.py)
pyre_test_python_testcase(pyre/filesystem/local_rootNonexistent.py)
pyre_test_python_testcase(pyre/filesystem/local_rootNotDirectory.py)
pyre_test_python_testcase(pyre/filesystem/local_make.py)
pyre_test_python_testcase(pyre/filesystem/zip.py)
pyre_test_python_testcase(pyre/filesystem/zip_open.py)
pyre_test_python_testcase(pyre/filesystem/zip_rootNonexistent.py)
pyre_test_python_testcase(pyre/filesystem/zip_rootNotZipfile.py)
pyre_test_python_testcase(pyre/filesystem/finder.py)
pyre_test_python_testcase(pyre/filesystem/finder_pattern.py)
pyre_test_python_testcase(pyre/filesystem/simple_explorer.py)
pyre_test_python_testcase(pyre/filesystem/tree_explorer.py)

# the {local_make} test requires setup+cleanup
# setup: zip the current directory
set(filesystem_local_make_setup
  "echo nothing to do"
  )
# cleanup: remove the zipfile
set(filesystem_local_make_cleanup
  "rm -rf local-make"
  )
pyre_test_testcase_shell_fixture(
  "${filesystem_local_make_setup}" "${filesystem_local_make_cleanup}"
  pyre/filesystem/local_make.py
  )

# the {zip} test requires setup+cleanup
# setup: zip the current directory
set(filesystem_zip_setup
  "zip -q sample.zip *"
  )
# cleanup: remove the zipfile
set(filesystem_zip_cleanup
  "rm sample.zip"
  )
pyre_test_testcase_shell_fixture(
  "${filesystem_zip_setup}" "${filesystem_zip_cleanup}"
  pyre/filesystem/zip.py
  )


#
# pyre/xml
#
pyre_test_python_testcase(pyre/xml/sanity.py)
pyre_test_python_testcase(pyre/xml/exceptions.py)
pyre_test_python_testcase(pyre/xml/reader.py)
pyre_test_python_testcase(pyre/xml/document.py)
pyre_test_python_testcase(pyre/xml/blank.py)
pyre_test_python_testcase(pyre/xml/empty.py)
pyre_test_python_testcase(pyre/xml/namespaces.py)
pyre_test_python_testcase(pyre/xml/schema.py)
pyre_test_python_testcase(pyre/xml/fs.py)
pyre_test_python_testcase(pyre/xml/fs_namespaces.py)
pyre_test_python_testcase(pyre/xml/fs_schema.py)
pyre_test_python_testcase(pyre/xml/fs_extra.py)


#
# pyre/schemata
#
pyre_test_python_testcase(pyre/schemata/sanity.py)
pyre_test_python_testcase(pyre/schemata/exceptions.py)
pyre_test_python_testcase(pyre/schemata/arrays.py)
pyre_test_python_testcase(pyre/schemata/booleans.py)
pyre_test_python_testcase(pyre/schemata/catalogs.py)
pyre_test_python_testcase(pyre/schemata/dates.py)
pyre_test_python_testcase(pyre/schemata/decimals.py)
pyre_test_python_testcase(pyre/schemata/dimensionals.py)
pyre_test_python_testcase(pyre/schemata/floats.py)
pyre_test_python_testcase(pyre/schemata/fractional.py)
pyre_test_python_testcase(pyre/schemata/inets.py)
pyre_test_python_testcase(pyre/schemata/integers.py)
pyre_test_python_testcase(pyre/schemata/istreams.py)
pyre_test_python_testcase(pyre/schemata/lists.py)
pyre_test_python_testcase(pyre/schemata/mappings.py)
pyre_test_python_testcase(pyre/schemata/ostreams.py)
pyre_test_python_testcase(pyre/schemata/paths.py)
pyre_test_python_testcase(pyre/schemata/sets.py)
pyre_test_python_testcase(pyre/schemata/strings.py)
pyre_test_python_testcase(pyre/schemata/times.py)
pyre_test_python_testcase(pyre/schemata/timestamps.py)
pyre_test_python_testcase(pyre/schemata/tuples.py)
pyre_test_python_testcase(pyre/schemata/uris.py)
pyre_test_python_testcase(pyre/schemata/typed.py)

# the {ostreams} test requires setup+cleanup
# setup: do nothing
set(schemata_ostreams_setup
  "echo nothing to do"
  )
# cleanup: remove the zipfile
set(schemata_ostreams_cleanup
  "rm output.cfg"
  )
pyre_test_testcase_shell_fixture(
  "${schemata_ostreams_setup}" "${schemata_ostreams_cleanup}"
  pyre/schemata/ostreams.py
  )


#
# pyre/constraints
#
pyre_test_python_testcase(pyre/constraints/sanity.py)
pyre_test_python_testcase(pyre/constraints/exceptions.py)
pyre_test_python_testcase(pyre/constraints/isBetween.py)
pyre_test_python_testcase(pyre/constraints/isEqual.py)
pyre_test_python_testcase(pyre/constraints/isGreater.py)
pyre_test_python_testcase(pyre/constraints/isGreaterEqual.py)
pyre_test_python_testcase(pyre/constraints/isLess.py)
pyre_test_python_testcase(pyre/constraints/isLessEqual.py)
pyre_test_python_testcase(pyre/constraints/isLike.py)
pyre_test_python_testcase(pyre/constraints/isMember.py)
pyre_test_python_testcase(pyre/constraints/isNegative.py)
pyre_test_python_testcase(pyre/constraints/isPositive.py)
pyre_test_python_testcase(pyre/constraints/isAll.py)
pyre_test_python_testcase(pyre/constraints/isAny.py)
pyre_test_python_testcase(pyre/constraints/isNot.py)
pyre_test_python_testcase(pyre/constraints/isSubset.py)
pyre_test_python_testcase(pyre/constraints/and.py)
pyre_test_python_testcase(pyre/constraints/or.py)


#
# pyre/algebraic
#
pyre_test_python_testcase(pyre/algebraic/sanity.py)
pyre_test_python_testcase(pyre/algebraic/exceptions.py)
pyre_test_python_testcase(pyre/algebraic/layout.py)
pyre_test_python_testcase(pyre/algebraic/arithmetic.py)
pyre_test_python_testcase(pyre/algebraic/ordering.py)
pyre_test_python_testcase(pyre/algebraic/boolean.py)
pyre_test_python_testcase(pyre/algebraic/dependencies.py)
pyre_test_python_testcase(pyre/algebraic/patch.py)


#
# pyre/calc
#
pyre_test_python_testcase(pyre/calc/sanity.py)
pyre_test_python_testcase(pyre/calc/exceptions.py)
pyre_test_python_testcase(pyre/calc/node_class.py)
pyre_test_python_testcase(pyre/calc/node_instance.py)
pyre_test_python_testcase(pyre/calc/node.py)
pyre_test_python_testcase(pyre/calc/substitute.py)
pyre_test_python_testcase(pyre/calc/replace.py)
pyre_test_python_testcase(pyre/calc/replace_probe.py)
pyre_test_python_testcase(pyre/calc/patch.py)
pyre_test_python_testcase(pyre/calc/explicit.py)
pyre_test_python_testcase(pyre/calc/probe.py)
pyre_test_python_testcase(pyre/calc/containers.py)
pyre_test_python_testcase(pyre/calc/reference.py)
pyre_test_python_testcase(pyre/calc/sum.py)
pyre_test_python_testcase(pyre/calc/aggregators.py)
pyre_test_python_testcase(pyre/calc/reductors.py)
pyre_test_python_testcase(pyre/calc/operations.py)
pyre_test_python_testcase(pyre/calc/algebra.py)
pyre_test_python_testcase(pyre/calc/expression.py)
pyre_test_python_testcase(pyre/calc/expression_escaped.py)
pyre_test_python_testcase(pyre/calc/expression_resolution.py)
pyre_test_python_testcase(pyre/calc/expression_circular.py)
pyre_test_python_testcase(pyre/calc/expression_syntaxerror.py)
pyre_test_python_testcase(pyre/calc/expression_typeerror.py)
pyre_test_python_testcase(pyre/calc/interpolation.py)
pyre_test_python_testcase(pyre/calc/interpolation_escaped.py)
pyre_test_python_testcase(pyre/calc/interpolation_circular.py)
pyre_test_python_testcase(pyre/calc/memo.py)
pyre_test_python_testcase(pyre/calc/memo_model.py)
pyre_test_python_testcase(pyre/calc/memo_expression.py)
pyre_test_python_testcase(pyre/calc/memo_interpolation.py)
pyre_test_python_testcase(pyre/calc/hierarchical.py)
pyre_test_python_testcase(pyre/calc/hierarchical_patch.py)
pyre_test_python_testcase(pyre/calc/hierarchical_alias.py)
pyre_test_python_testcase(pyre/calc/hierarchical_group.py)
pyre_test_python_testcase(pyre/calc/hierarchical_contains.py)
pyre_test_python_testcase(pyre/calc/model.py)


#
# pyre/descriptors
#
pyre_test_python_testcase(pyre/descriptors/sanity.py)
pyre_test_python_testcase(pyre/descriptors/booleans.py)
pyre_test_python_testcase(pyre/descriptors/decimals.py)
pyre_test_python_testcase(pyre/descriptors/floats.py)
pyre_test_python_testcase(pyre/descriptors/inets.py)
pyre_test_python_testcase(pyre/descriptors/integers.py)
pyre_test_python_testcase(pyre/descriptors/strings.py)
pyre_test_python_testcase(pyre/descriptors/dates.py)
pyre_test_python_testcase(pyre/descriptors/dimensionals.py)
pyre_test_python_testcase(pyre/descriptors/paths.py)
pyre_test_python_testcase(pyre/descriptors/times.py)
pyre_test_python_testcase(pyre/descriptors/timestamps.py)
pyre_test_python_testcase(pyre/descriptors/uris.py)
pyre_test_python_testcase(pyre/descriptors/arrays.py)
pyre_test_python_testcase(pyre/descriptors/tuples.py)
pyre_test_python_testcase(pyre/descriptors/lists.py)
pyre_test_python_testcase(pyre/descriptors/sets.py)
pyre_test_python_testcase(pyre/descriptors/istreams.py)
pyre_test_python_testcase(pyre/descriptors/ostreams.py)
pyre_test_python_testcase(pyre/descriptors/harvesting.py)
pyre_test_python_testcase(pyre/descriptors/defaults.py)
pyre_test_python_testcase(pyre/descriptors/inheritance.py)
pyre_test_python_testcase(pyre/descriptors/filtering.py)
pyre_test_python_testcase(pyre/descriptors/converters.py)

# the {ostreams} test requires setup+cleanup
# setup: do nothing
set(descriptors_ostreams_setup
  "echo nothing to do"
  )
# cleanup: remove the zipfile
set(descriptors_ostreams_cleanup
  "rm output.cfg"
  )
pyre_test_testcase_shell_fixture(
  "${descriptors_ostreams_setup}" "${descriptors_ostreams_cleanup}"
  pyre/descriptors/ostreams.py
  )


#
# pyre/records
#
pyre_test_python_testcase(pyre/records/sanity.py)
pyre_test_python_testcase(pyre/records/simple.py)
pyre_test_python_testcase(pyre/records/simple_layout.py)
pyre_test_python_testcase(pyre/records/simple_inheritance.py)
pyre_test_python_testcase(pyre/records/simple_inheritance_multi.py)
pyre_test_python_testcase(pyre/records/simple_immutable_data.py)
pyre_test_python_testcase(pyre/records/simple_immutable_kwds.py)
pyre_test_python_testcase(pyre/records/simple_immutable_conversions.py)
pyre_test_python_testcase(pyre/records/simple_immutable_validations.py)
pyre_test_python_testcase(pyre/records/simple_mutable_data.py)
pyre_test_python_testcase(pyre/records/simple_mutable_kwds.py)
pyre_test_python_testcase(pyre/records/simple_mutable_conversions.py)
pyre_test_python_testcase(pyre/records/simple_mutable_validations.py)
pyre_test_python_testcase(pyre/records/complex_layout.py)
pyre_test_python_testcase(pyre/records/complex_inheritance.py)
pyre_test_python_testcase(pyre/records/complex_inheritance_multi.py)
pyre_test_python_testcase(pyre/records/complex_immutable_data.py)
pyre_test_python_testcase(pyre/records/complex_immutable_kwds.py)
pyre_test_python_testcase(pyre/records/complex_immutable_conversions.py)
pyre_test_python_testcase(pyre/records/complex_immutable_validations.py)
pyre_test_python_testcase(pyre/records/complex_mutable_data.py)
pyre_test_python_testcase(pyre/records/complex_mutable_kwds.py)
pyre_test_python_testcase(pyre/records/complex_mutable_conversions.py)
pyre_test_python_testcase(pyre/records/complex_mutable_validations.py)
pyre_test_python_testcase(pyre/records/csv_instance.py)
pyre_test_python_testcase(pyre/records/csv_read_simple.py)
pyre_test_python_testcase(pyre/records/csv_read_partial.py)
pyre_test_python_testcase(pyre/records/csv_read_mutable.py)
pyre_test_python_testcase(pyre/records/csv_read_complex.py)
pyre_test_python_testcase(pyre/records/csv_bad_source.py)


#
# pyre/tabular
#
pyre_test_python_testcase(pyre/tabular/sanity.py)
pyre_test_python_testcase(pyre/tabular/sheet.py)
pyre_test_python_testcase(pyre/tabular/sheet_class_layout.py)
pyre_test_python_testcase(pyre/tabular/sheet_class_inheritance.py)
pyre_test_python_testcase(pyre/tabular/sheet_class_inheritance_multi.py)
pyre_test_python_testcase(pyre/tabular/sheet_class_record.py)
pyre_test_python_testcase(pyre/tabular/sheet_class_inheritance_record.py)
pyre_test_python_testcase(pyre/tabular/sheet_instance.py)
pyre_test_python_testcase(pyre/tabular/sheet_populate.py)
pyre_test_python_testcase(pyre/tabular/sheet_columns.py)
pyre_test_python_testcase(pyre/tabular/sheet_index.py)
pyre_test_python_testcase(pyre/tabular/sheet_updates.py)
pyre_test_python_testcase(pyre/tabular/view.py)
pyre_test_python_testcase(pyre/tabular/chart.py)
pyre_test_python_testcase(pyre/tabular/chart_class_layout.py)
pyre_test_python_testcase(pyre/tabular/chart_class_inheritance.py)
pyre_test_python_testcase(pyre/tabular/chart_instance.py)
pyre_test_python_testcase(pyre/tabular/chart_inferred.py)
pyre_test_python_testcase(pyre/tabular/chart_interval_config.py)
pyre_test_python_testcase(pyre/tabular/chart_interval.py)
pyre_test_python_testcase(pyre/tabular/chart_filter.py)
pyre_test_python_testcase(pyre/tabular/chart_sales.py)
pyre_test_python_testcase(pyre/tabular/pivot.py)
pyre_test_python_testcase(pyre/tabular/csv_instance.py)
pyre_test_python_testcase(pyre/tabular/csv_read.py)


#
# pyre/tracking
#
pyre_test_python_testcase(pyre/tracking/sanity.py)
pyre_test_python_testcase(pyre/tracking/simple.py)
pyre_test_python_testcase(pyre/tracking/lookup.py)
pyre_test_python_testcase(pyre/tracking/command.py)
pyre_test_python_testcase(pyre/tracking/file.py)
pyre_test_python_testcase(pyre/tracking/fileregion.py)
pyre_test_python_testcase(pyre/tracking/script.py)
pyre_test_python_testcase(pyre/tracking/chain.py)


#
#  pyre/codecs
#
pyre_test_python_testcase(pyre/codecs/sanity.py)
pyre_test_python_testcase(pyre/codecs/exceptions.py)
pyre_test_python_testcase(pyre/codecs/manager.py)
pyre_test_python_testcase(pyre/codecs/pml.py)
pyre_test_python_testcase(pyre/codecs/pml_empty.py)
pyre_test_python_testcase(pyre/codecs/pml_badRoot.py)
pyre_test_python_testcase(pyre/codecs/pml_unknownNode.py)
pyre_test_python_testcase(pyre/codecs/pml_badNode.py)
pyre_test_python_testcase(pyre/codecs/pml_badAttribute.py)
pyre_test_python_testcase(pyre/codecs/pml_package.py)
pyre_test_python_testcase(pyre/codecs/pml_packageNested.py)
pyre_test_python_testcase(pyre/codecs/pml_componentFamily.py)
pyre_test_python_testcase(pyre/codecs/pml_componentName.py)
pyre_test_python_testcase(pyre/codecs/pml_componentConditional.py)
pyre_test_python_testcase(pyre/codecs/pml_componentConditionalNested.py)
pyre_test_python_testcase(pyre/codecs/pml_sample.py)
pyre_test_python_testcase(pyre/codecs/cfg.py)
pyre_test_python_testcase(pyre/codecs/cfg_empty.py)
pyre_test_python_testcase(pyre/codecs/cfg_badToken.py)
pyre_test_python_testcase(pyre/codecs/cfg_marker.py)
pyre_test_python_testcase(pyre/codecs/cfg_open.py)
pyre_test_python_testcase(pyre/codecs/cfg_close.py)
pyre_test_python_testcase(pyre/codecs/pfg.py)
pyre_test_python_testcase(pyre/codecs/pfg_empty.py)
pyre_test_python_testcase(pyre/codecs/pfg_package.py)
pyre_test_python_testcase(pyre/codecs/pfg_packageNested.py)
pyre_test_python_testcase(pyre/codecs/pfg_componentFamily.py)
pyre_test_python_testcase(pyre/codecs/pfg_componentName.py)
pyre_test_python_testcase(pyre/codecs/pfg_componentConditional.py)
pyre_test_python_testcase(pyre/codecs/pfg_componentConditionalNested.py)
pyre_test_python_testcase(pyre/codecs/pfg_sample.py)


#
# pyre/config
#
pyre_test_python_testcase(pyre/config/sanity.py)
pyre_test_python_testcase(pyre/config/exceptions.py)
pyre_test_python_testcase(pyre/config/events.py)
pyre_test_python_testcase(pyre/config/events_assignments.py)
pyre_test_python_testcase(pyre/config/configurator.py)
pyre_test_python_testcase(pyre/config/configurator_assignments.py)
pyre_test_python_testcase(pyre/config/configurator_load_pml.py)
pyre_test_python_testcase(pyre/config/configurator_load_cfg.py)
pyre_test_python_testcase(pyre/config/configurator_load_pfg.py)
pyre_test_python_testcase(pyre/config/command.py)
pyre_test_python_testcase(pyre/config/command_argv.py)
pyre_test_python_testcase(pyre/config/command_config.py)


#
# pyre/framework
#
pyre_test_python_testcase(pyre/framework/sanity.py)
pyre_test_python_testcase(pyre/framework/exceptions.py)
pyre_test_python_testcase(pyre/framework/slot.py)
pyre_test_python_testcase(pyre/framework/slot_instance.py)
pyre_test_python_testcase(pyre/framework/slot_algebra.py)
pyre_test_python_testcase(pyre/framework/slot_update.py)
pyre_test_python_testcase(pyre/framework/nameserver.py)
pyre_test_python_testcase(pyre/framework/nameserver_access.py)
pyre_test_python_testcase(pyre/framework/nameserver_aliases.py)
pyre_test_python_testcase(pyre/framework/fileserver.py)
pyre_test_python_testcase(pyre/framework/fileserver_uri.py)
pyre_test_python_testcase(pyre/framework/fileserver_mount.py)
pyre_test_python_testcase(pyre/framework/registrar.py)
pyre_test_python_testcase(pyre/framework/linker.py)
pyre_test_python_testcase(pyre/framework/linker_codecs.py)
pyre_test_python_testcase(pyre/framework/linker_shelves.py)
pyre_test_python_testcase(pyre/framework/externals.py)
pyre_test_python_testcase(pyre/framework/executive.py)
pyre_test_python_testcase(pyre/framework/executive_configuration.py)
pyre_test_python_testcase(pyre/framework/executive_resolve.py)
pyre_test_python_testcase(pyre/framework/executive_resolve_duplicate.py)
pyre_test_python_testcase(pyre/framework/executive_resolve_badImport.py)
pyre_test_python_testcase(pyre/framework/executive_resolve_syntaxError.py)


#
# pyre/components
#
pyre_test_python_testcase(pyre/components/sanity.py)
pyre_test_python_testcase(pyre/components/exceptions.py)
pyre_test_python_testcase(pyre/components/requirement.py)
pyre_test_python_testcase(pyre/components/role.py)
pyre_test_python_testcase(pyre/components/actor.py)
pyre_test_python_testcase(pyre/components/protocol.py)
pyre_test_python_testcase(pyre/components/protocol_family.py)
pyre_test_python_testcase(pyre/components/protocol_behavior.py)
pyre_test_python_testcase(pyre/components/protocol_property.py)
pyre_test_python_testcase(pyre/components/protocol_inheritance.py)
pyre_test_python_testcase(pyre/components/protocol_shadow.py)
pyre_test_python_testcase(pyre/components/protocol_inheritance_multi.py)
pyre_test_python_testcase(pyre/components/protocol_compatibility.py)
pyre_test_python_testcase(pyre/components/protocol_compatibility_reports.py)
pyre_test_python_testcase(pyre/components/protocol_instantiation.py)
pyre_test_python_testcase(pyre/components/component.py)
pyre_test_python_testcase(pyre/components/component_family.py)
pyre_test_python_testcase(pyre/components/component_behavior.py)
pyre_test_python_testcase(pyre/components/component_property.py)
pyre_test_python_testcase(pyre/components/component_facility.py)
pyre_test_python_testcase(pyre/components/component_inheritance.py)
pyre_test_python_testcase(pyre/components/component_shadow.py)
pyre_test_python_testcase(pyre/components/component_inheritance_multi.py)
pyre_test_python_testcase(pyre/components/component_compatibility.py)
pyre_test_python_testcase(pyre/components/component_compatibility_reports.py)
pyre_test_python_testcase(pyre/components/component_implements.py)
pyre_test_python_testcase(pyre/components/component_bad_implementations.py)
pyre_test_python_testcase(pyre/components/component_class_registration.py)
pyre_test_python_testcase(pyre/components/component_class_registration_inventory.py)
pyre_test_python_testcase(pyre/components/component_class_registration_model.py)
pyre_test_python_testcase(pyre/components/component_class_configuration.py)
pyre_test_python_testcase(pyre/components/component_class_configuration_inheritance.py)
pyre_test_python_testcase(pyre/components/component_class_configuration_inheritance_multi.py)
pyre_test_python_testcase(pyre/components/component_class_binding.py)
pyre_test_python_testcase(pyre/components/component_class_binding_import.py)
pyre_test_python_testcase(pyre/components/component_class_binding_vfs.py)
pyre_test_python_testcase(pyre/components/component_class_binding_conversions.py)
pyre_test_python_testcase(pyre/components/component_class_validation.py)
pyre_test_python_testcase(pyre/components/component_class_trait_matrix.py)
pyre_test_python_testcase(pyre/components/component_class_private_locators.py)
pyre_test_python_testcase(pyre/components/component_class_public_locators.py)
pyre_test_python_testcase(pyre/components/component_class_inventory.py)
pyre_test_python_testcase(pyre/components/component_defaults.py)
pyre_test_python_testcase(pyre/components/component_instantiation.py)
pyre_test_python_testcase(pyre/components/component_invocation.py)
pyre_test_python_testcase(pyre/components/component_instance_registration.py)
pyre_test_python_testcase(pyre/components/component_instance_configuration.py)
pyre_test_python_testcase(pyre/components/component_instance_configuration_constructor.py)
pyre_test_python_testcase(pyre/components/component_instance_configuration_inheritance.py)
pyre_test_python_testcase(pyre/components/component_instance_configuration_inheritance_multi.py)
pyre_test_python_testcase(pyre/components/component_instance_binding.py)
pyre_test_python_testcase(pyre/components/component_instance_binding_implicit.py)
pyre_test_python_testcase(pyre/components/component_instance_binding_configuration.py)
pyre_test_python_testcase(pyre/components/component_instance_binding_existing.py)
pyre_test_python_testcase(pyre/components/component_instance_binding_deferred.py)
pyre_test_python_testcase(pyre/components/component_instance_validation.py)
pyre_test_python_testcase(pyre/components/component_instance_private_locators.py)
pyre_test_python_testcase(pyre/components/component_instance_public_locators.py)
pyre_test_python_testcase(pyre/components/component_aliases.py --functor.μ=0.10 --gaussian.σ=0.10)
pyre_test_python_testcase(pyre/components/component_slots.py)
pyre_test_python_testcase(pyre/components/component_list.py)
pyre_test_python_testcase(pyre/components/component_dict.py)
pyre_test_python_testcase(pyre/components/quad.py)
pyre_test_python_testcase(pyre/components/monitor.py)
pyre_test_python_testcase(pyre/components/tracker.py)


#
# pyre/timers
#
pyre_test_python_testcase(pyre/timers/sanity.py)
pyre_test_python_testcase(pyre/timers/python_timer.py)
pyre_test_python_testcase(pyre/timers/python_timer_errors.py)
pyre_test_python_testcase(pyre/timers/native_timer.py)
pyre_test_python_testcase(pyre/timers/pyre_timer.py)


#
# pyre/weaver
#
pyre_test_python_testcase(pyre/weaver/sanity.py)
pyre_test_python_testcase(pyre/weaver/weaver_raw.py)
pyre_test_python_testcase(pyre/weaver/document_c.py)
pyre_test_python_testcase(pyre/weaver/document_csh.py)
pyre_test_python_testcase(pyre/weaver/document_cxx.py)
pyre_test_python_testcase(pyre/weaver/document_f77.py)
pyre_test_python_testcase(pyre/weaver/document_f90.py)
pyre_test_python_testcase(pyre/weaver/document_html.py)
pyre_test_python_testcase(pyre/weaver/document_latex.py)
pyre_test_python_testcase(pyre/weaver/document_make.py)
pyre_test_python_testcase(pyre/weaver/document_pfg.py)
pyre_test_python_testcase(pyre/weaver/document_perl.py)
pyre_test_python_testcase(pyre/weaver/document_python.py)
pyre_test_python_testcase(pyre/weaver/document_sh.py)
pyre_test_python_testcase(pyre/weaver/document_sql.py)
pyre_test_python_testcase(pyre/weaver/document_svg.py)
pyre_test_python_testcase(pyre/weaver/document_tex.py)
pyre_test_python_testcase(pyre/weaver/document_xml.py)
pyre_test_python_testcase(pyre/weaver/expressions_c.py)
pyre_test_python_testcase(pyre/weaver/expressions_cxx.py)
pyre_test_python_testcase(pyre/weaver/expressions_python.py)
pyre_test_python_testcase(pyre/weaver/expressions_sql.py)


#
# pyre/db
#
pyre_test_python_testcase(pyre/db/sanity.py)
pyre_test_python_testcase(pyre/db/table_declaration.py)
pyre_test_python_testcase(pyre/db/table_inheritance.py)
pyre_test_python_testcase(pyre/db/table_create.py)
pyre_test_python_testcase(pyre/db/table_references.py)
pyre_test_python_testcase(pyre/db/table_annotations.py)
pyre_test_python_testcase(pyre/db/table_delete.py)
pyre_test_python_testcase(pyre/db/table_instantiation.py)
pyre_test_python_testcase(pyre/db/table_insert.py)
pyre_test_python_testcase(pyre/db/table_update.py)
pyre_test_python_testcase(pyre/db/query_star.py)
pyre_test_python_testcase(pyre/db/query_projection.py)
pyre_test_python_testcase(pyre/db/query_projection_expressions.py)
pyre_test_python_testcase(pyre/db/query_projection_multitable.py)
pyre_test_python_testcase(pyre/db/query_restriction.py)
pyre_test_python_testcase(pyre/db/query_collation.py)
pyre_test_python_testcase(pyre/db/query_collation_explicit.py)
pyre_test_python_testcase(pyre/db/query_collation_expression.py)
pyre_test_python_testcase(pyre/db/query_inheritance.py)
pyre_test_python_testcase(pyre/db/persistent_declaration.py)


#
# pyre/ipc
#
pyre_test_python_testcase(pyre/ipc/sanity.py)
pyre_test_python_testcase(pyre/ipc/pickler.py)
pyre_test_python_testcase(pyre/ipc/pipe.py)
pyre_test_python_testcase(pyre/ipc/tcp.py)
pyre_test_python_testcase(pyre/ipc/pickler_over_pipe.py)
pyre_test_python_testcase(pyre/ipc/pickler_over_tcp.py)
pyre_test_python_testcase(pyre/ipc/scheduler.py)
pyre_test_python_testcase(pyre/ipc/scheduler_instantiation.py)
pyre_test_python_testcase(pyre/ipc/scheduler_alarms.py)
pyre_test_python_testcase(pyre/ipc/selector.py)
pyre_test_python_testcase(pyre/ipc/selector_instantiation.py)
pyre_test_python_testcase(pyre/ipc/selector_alarms.py)
pyre_test_python_testcase(pyre/ipc/selector_signals.py)
pyre_test_python_testcase(pyre/ipc/selector_pickler_over_pipe.py)
pyre_test_python_testcase(pyre/ipc/selector_pickler_over_tcp.py)


#
# pyre/nexus
#
pyre_test_python_testcase(pyre/nexus/sanity.py)
pyre_test_python_testcase(pyre/nexus/node.py)
pyre_test_python_testcase(pyre/nexus/node_instantiation.py)
pyre_test_python_testcase(pyre/nexus/node_signals.py)
pyre_test_python_testcase(pyre/nexus/pool.py)
pyre_test_python_testcase(pyre/nexus/pool.py --tasks=4 --team.size=2)


#
# pyre/platforms
#
pyre_test_python_testcase(pyre/platforms/sanity.py)
pyre_test_python_testcase(pyre/platforms/host.py)


#
# pyre/shells
#
pyre_test_python_testcase(pyre/shells/sanity.py)
pyre_test_python_testcase(pyre/shells/application_sanity.py)
pyre_test_python_testcase(pyre/shells/application_instantiation.py)
pyre_test_python_testcase(pyre/shells/application_inheritance.py)
pyre_test_python_testcase(pyre/shells/application_namespace.py)
pyre_test_python_testcase(pyre/shells/script_sanity.py)
pyre_test_python_testcase(pyre/shells/script_instantiation.py)
pyre_test_python_testcase(pyre/shells/fork_sanity.py)
pyre_test_python_testcase(pyre/shells/fork_instantiation.py)
pyre_test_python_testcase(pyre/shells/daemon_sanity.py)
pyre_test_python_testcase(pyre/shells/daemon_instantiation.py)
pyre_test_python_testcase(pyre/shells/colors256.py)
pyre_test_python_testcase(pyre/shells/colors24bit.py)
pyre_test_python_testcase(pyre/shells/script_launching.py)
pyre_test_python_testcase(pyre/shells/fork_launching.py)
pyre_test_python_testcase(pyre/shells/daemon_launching.py)


#
# pyre/externals
#
pyre_test_python_testcase(pyre/externals/sanity.py)
pyre_test_python_testcase(pyre/externals/locate.py)
pyre_test_python_testcase(pyre/externals/blas.py)
pyre_test_python_testcase(pyre/externals/blas.py --blas=gslcblas)
pyre_test_python_testcase(pyre/externals/blas.py --blas=atlas)
pyre_test_python_testcase(pyre/externals/blas.py --blas=openblas)
#pyre_test_python_testcase(pyre/externals/blas.py --blas=gslcblas\\\#mga)
#pyre_test_python_testcase(pyre/externals/blas.py --blas=atlas\#mga)
#pyre_test_python_testcase(pyre/externals/blas.py --blas=openblas\#mga)
pyre_test_python_testcase(pyre/externals/cython.py)
pyre_test_python_testcase(pyre/externals/cython.py --cython=cython2)
pyre_test_python_testcase(pyre/externals/cython.py --cython=cython3)
#pyre_test_python_testcase(pyre/externals/cython.py --cython=cython2\#mga)
#pyre_test_python_testcase(pyre/externals/cython.py --cython=cython3\#mga)
pyre_test_python_testcase(pyre/externals/gcc.py)
pyre_test_python_testcase(pyre/externals/gcc.py --gcc=gcc5)
#pyre_test_python_testcase(pyre/externals/gcc.py --gcc=gcc5\#mga)
pyre_test_python_testcase(pyre/externals/gsl.py)
pyre_test_python_testcase(pyre/externals/gsl.py --gsl=default)
#pyre_test_python_testcase(pyre/externals/gsl.py --gsl=default\#mga)
pyre_test_python_testcase(pyre/externals/hdf5.py)
pyre_test_python_testcase(pyre/externals/hdf5.py --hdf5=default)
#pyre_test_python_testcase(pyre/externals/hdf5.py --hdf5=default\#mga)
pyre_test_python_testcase(pyre/externals/mpi.py)
pyre_test_python_testcase(pyre/externals/mpi.py --mpi=mpich)
pyre_test_python_testcase(pyre/externals/mpi.py --mpi=openmpi)
#pyre_test_python_testcase(pyre/externals/mpi.py --mpi=mpich\#mga)
#pyre_test_python_testcase(pyre/externals/mpi.py --mpi=openmpi\#mga)
pyre_test_python_testcase(pyre/externals/postgres.py)
pyre_test_python_testcase(pyre/externals/postgres.py --postgres=default)
#pyre_test_python_testcase(pyre/externals/postgres.py --postgres=default\#mga)
pyre_test_python_testcase(pyre/externals/python.py)
pyre_test_python_testcase(pyre/externals/python.py --python=python3)
pyre_test_python_testcase(pyre/externals/python.py --python=python2)
#pyre_test_python_testcase(pyre/externals/python.py --python=python3\#python35)
#pyre_test_python_testcase(pyre/externals/python.py --python=python2\#python27)
#pyre_test_python_testcase(pyre/externals/python.py --python=python3\#mga)
#pyre_test_python_testcase(pyre/externals/python.py --python=python2\#mga)
pyre_test_python_testcase(pyre/externals/vtk.py)
pyre_test_python_testcase(pyre/externals/vtk.py --vtk=vtk5)
pyre_test_python_testcase(pyre/externals/vtk.py --vtk=vtk6)
#pyre_test_python_testcase(pyre/externals/vtk.py --vtk=vtk6\#mga)


#
# pyre/flow
#
pyre_test_python_testcase(pyre/flow/sanity.py)


#
# pyre/pyre
#
pyre_test_python_testcase(pyre/pyre/sanity.py)
pyre_test_python_testcase(pyre/pyre/loadConfiguration.py)
pyre_test_python_testcase(pyre/pyre/resolve.py)
pyre_test_python_testcase(pyre/pyre/spaces.py)
pyre_test_python_testcase(pyre/pyre/defaults.py)
pyre_test_python_testcase(pyre/pyre/play.py)
pyre_test_python_testcase(pyre/pyre/headers.py)


# end of file
