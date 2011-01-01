<?xml version="1.0" encoding="utf-8"?>
<!--
!
! michael a.g. aïvázis
! california institute of technology
! (c) 1998-2011  all rights reserved
!
-->

<config>

  <!-- application settings -->
  <component name="gauss">
    <bind property="domain">import://gauss.shapes.circle</bind>
    <bind property="integrand">import://gauss.functors.one</bind>
    <bind property="integrator">import://gauss.integrators.montecarlo</bind>
  </component>


  <!-- sample configurations -->

  <!-- when the integrator is montecarlo -->
  <component name="gauss.integrator" family="gauss.integrators.montecarlo">
    <bind property="samples">1e7</bind>
  </component>

  <!-- when the domain is a circle -->
  <component name="gauss.domain" family="gauss.shapes.circle">
    <bind property="radius">1.0</bind>
    <bind property="center">(0.0, 0.0)</bind>
  </component>

  <!-- when the integrand is a gaussian -->
  <component name="gauss.integrand" family="gauss.functors.gaussian">
    <bind property="μ">(0.0,0.0)</bind>
    <bind property="σ">1.0</bind>
  </component>

</config>


<!-- end of file -->
