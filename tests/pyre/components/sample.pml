<?xml version="1.0" encoding="utf-8"?>
<!--
!
! michael a.g. aïvázis
! california institute of technology
! (c) 1998-2010  all rights reserved
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

  <component name="d1" family="sample.derived">
    <!-- some bindings -->
    <bind property="extra">d1 - extra</bind>
    <bind property="middle">d1 - middle</bind>
    <bind property="common">d1 - common</bind>
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
