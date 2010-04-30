<?xml version="1.0" encoding="utf-8"?>
<!--
!
! michael a.g. aïvázis
! california institute of technology
! (c) 1998-2009  all rights reserved
!
-->

<config>

  <!-- data for component_configuration -->
  <component family="sample.configuration">
    <!-- some bindings -->
    <bind property="p1">sample - p1</bind>
    <bind property="p2">sample - p2</bind>
  </component>

  <!-- data for component_configuration_inheritance -->
  <component family="sample.base">
    <!-- some bindings -->
    <bind property="common">base - common</bind>
  </component>

  <component family="sample.derived">
    <!-- some bindings -->
    <bind property="extra">derived - extra</bind>
    <bind property="common">derived - common</bind>
  </component>

</config>


<!-- end of file -->
