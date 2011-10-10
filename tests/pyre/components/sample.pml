<?xml version="1.0" encoding="utf-8"?>
<!--
!
! michael a.g. aïvázis
! california institute of technology
! (c) 1998-2011 all rights reserved
!
-->

<config>

  <!-- global settings -->
  <bind property="sample.file">sample.pml</bind>

  <!-- data for component_class_configuration -->
  <component family="sample.configuration">
    <!-- some bindings -->
    <bind property="p1">sample - p1</bind>
    <bind property="p2">sample - p2</bind>
  </component>

  <!-- data for component_class_configuration_inheritance -->
  <component family="sample.base">
    <!-- some bindings -->
    <bind property="common">base - common</bind>
  </component>

  <component family="sample.derived">
    <!-- some bindings -->
    <bind property="extra">derived - extra</bind>
    <bind property="common">derived - common</bind>
  </component>

  <!-- data for component_class_inventory -->
  <component family="sample.inventory.base">
    <!-- some bindings -->
    <bind property="bprop">1</bind>
  </component>

  <component family="sample.inventory.derived">
    <!-- some bindings -->
    <bind property="bprop">2</bind>
    <bind property="dprop">Hello world!</bind>
  </component>

  <!-- data for component_instance_configuration -->
  <component name="c" family="sample.configuration">
    <!-- some bindings -->
    <bind property="p1">p1 - instance</bind>
    <bind property="p2">p2 - instance</bind>
  </component>

  <!-- data for component_instance_configuration_inheritance -->
  <component name="d" family="sample.derived">
    <!-- some bindings -->
    <bind property="extra">d - extra</bind>
    <bind property="middle">d - middle</bind>
    <bind property="common">d - common</bind>
  </component>

  <!-- data for component_instance_binding_configuration -->
  <component name="c" family="sample.manager">
    <bind property="jobs">10</bind>
  </component>
  <component name="w" family="sample.worker">
    <bind property="host">pyre.caltech.edu</bind>
  </component>
  <component name="c.gopher" family="sample.worker">
    <bind property="host">foxtrot.caltech.edu</bind>
  </component>

  <!-- data for component_aliases -->
  <component family="sample.functor">
    <bind property="mean">mean</bind>
    <bind property="μ">μ</bind>
    <bind property="spread">spread</bind>
    <bind property="σ">σ</bind>
  </component>

</config>


<!-- end of file -->
