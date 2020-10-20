# Permit Data Folder

This folder is comprised of two different sheets from the 2018 Housing Element Annual Progress report that is submitted to HCD.


## **[CITY_NAME]_HousingDevApps_2018**  

This sheet comes from **Table A** in the Housing Element Annual Report. The table describes the **Housing Development Applications Submitted** which provides the location of the development, its unit category (ADU, SRO, MH), its submission date, how many units are affordable and the level of affordability, and if its deed restricted, how many units were approved and disapproved for the project, and whether the SB35 streamlining applies to the project.

Its function is to inform HCD and OPR of the housing units and developments in a given jurisdiction within the submission year.

### Variable Descriptions

If you have worked with housing datasets before many of these values may look familiar. If not, please ask for clarification if the descriptions below do not answer all of your questions.

* `Unnamed: 0` is the outcome of when Pandas reads in a .csv with an empty column name.

**Project Identifiers:** The following columns are ones that the HCD requires to help identify applications for a building permit

* `APN_old` and `APN` are assessor's parcel numbers (APN). `APN_old` is used when the APN for the project changed between its initial permitting date and when this file was uploaded to HCD.

* `address` is a pretty straight forward description. This column provides the physical address within a jurisdiction

* `project_name` whether the development has an official name given to it at the time of applying for the permit.

* `jurisdiction_id` originally the "Local Jurisdiction Tracking ID" but this is a code that each permit application can be associated to. This is an optional field in the file!

**Project Descriptors:**

* `date_submit` much like the name describes: When the application for the permit was submitted.

* `unit` describes the variety of unit types that a development project could have. They could be:
    * SFA - Single-family attached unit
    * SFD - Single-family detached unit
    * 2-4 - Two- to four-unit structures
    * 5+ - Five or more unit structure, multifamily
    * ADU - Accessory dwelling unit
    * MH  - Mobile home/manufactured home

* `tenure` variable that identifies whether the units within the development project are either proposed or planned at initial occupancy for either renters or owners. Options either `R` or `O`.

**Proposed Units:** Describes the proposed units in the project by affordability

* `vli_dr` is a variable for the number of Very Low-Income Deed Restricted units proposed
* `vli_ndr` is a variable for the number of Very Low-Income Non Deed Restricted units proposed
* `li_dr` is a variable for the number of Low-Income Deed Restricted units proposed
* `li_ndr` is a variable for the number of Low-Income Non Deed Restricted units proposed
* `mi_dr` is a variable for the number of Moderate-Income Deed Restricted units proposed
* `mi_ndr` is a variable for the number of Moderate-Income Non Deed Restricted units proposed
* `ami` is a variable for the number of Above Moderate-Income units proposed
* `proposed` is the total number of units proposed by a particular project


* `approved` is the total number of units approved by project
* `disapproved` is the total number of units disapproved by project


* `sb35` is whether or not the submitted application is pursuant to GC 65913.4(b), which is the SB 35 Streamlining clause.


* `notes` are notes regarding the project


## **[CITY_NAME]_ActivityReport_2018**

This sheet comes from **Table A2** in the Housing Element Annual Report. The table describes the **Annual Building Activity Report Summary - New Construction, Entitled, Permits and Completed Units** which details the number of entitlements and permits by a project's affordability level (including if the level of affordability is dictated by a deed restriction). It's a summary that provides the State with information regarding the activity of new housing construction within the jurisdiction.

The table requires information for very low, low, moderate and above moderate income housing affordability categories and for mixed-income projects. Jurisdictions are required to provide data on **net new housing units and developments** that have received any one of the following:
* An entitlement
* A building permit
* A certificate of occupancy or other form of readiness that was issued during the reporting year.

If you have worked with housing datasets before many of these values may look familiar. If not, please ask for clarification if the descriptions below do not answer all of your questions.

### Variable Descriptions:

* `Unnamed: 0` is the outcome of when Pandas reads in a .csv with an empty column name.

**Project Identifiers:** The following columns are ones that the HCD requires to help identify applications for a building permit

* `APN_old` and `APN` are assessor's parcel numbers (APN). `APN_old` is used when the APN for the project changed between its initial permitting date and when this file was uploaded to HCD.

* `address` is a pretty straight forward description. This column provides the physical address within a jurisdiction

* `project_name` whether the development has an official name given to it at the time of applying for the permit.

* `jurisdiction_id` originally the "Local Jurisdiction Tracking ID" but this is a code that each permit application can be associated to. This is an optional field in the file!

**Project Descriptors:**

* `date_submit` much like the name describes: When the application for the permit was submitted.

* `unit` describes the variety of unit types that a development project could have. They could be:
    * SFA - Single-family attached unit
    * SFD - Single-family detached unit
    * 2-4 - Two- to four-unit structures
    * 5+ - Five or more unit structure, multifamily
    * ADU - Accessory dwelling unit
    * MH  - Mobile home/manufactured home


* `tenure` variable that identifies whether the units within the development project are either proposed or planned at initial occupancy for either renters or owners. Options either `R` or `O`.

**Completed Entitlements:** Each development listed with the number of units that have been issued a completed entitlement during the reporting year by affordability level and whether the units are deed restricted or non-deed restricted.


* `vli_dr_entitle` is a variable for the number of Very Low-Income Deed Restricted units proposed with a completed entitlement. VLI are households from 0-50% AMI.

* `vli_ndr_entitle` is a variable for the number of Very Low-Income Non-Deed Restricted units proposed with a completed entitlement. VLI are households from 0-50% AMI

* `li_dr_entitle` is a variable for the number of Low-Income Deed Restricted units proposed with a completed entitlement. LI are households from 50-80% AMI.

* `li_ndr_entitle` is a variable for the number of Low-Income Non-Deed Restricted units proposed with a completed entitlement. LI are households from 50-80% AMI

* `mi_dr_entitle` is a variable for the number of Moderate-Income Deed Restricted units proposed with a completed entitlement. MI are households from 80-120% AMI.

* `mi_ndr_entitle` is a variable for the number of Moderate-Income Non-Deed Restricted units proposed with a completed entitlement. MI are households from 80-120% AMI.

* `ami_entitle` is a variable for the number of Above-Moderate Income units proposed with a completed entitlement. AMI are households above 120% AMI. This is not to be confused with the term AMI for `Area Median Income`.

* `date_entitle` is a variable for the reporting year that all required land use approvals or entitlements were issued by the jurisdiction.

* `units_entitle`'s field reflects the total number of units that were entitled for very-low, low, moderate, and above moderate income. It is the sum of all previously entitled units.

**Development Building Permits:** Each development listed by the number of units that have been issued a building permit during the reporting year by affordability level and whether the units are deed restricted or non-deed restricted.

* `vli_dr_permit` is a variable for the number of Very-Low Income Deed Restricted units proposed with issued building permits. VLI are households from 0-50% AMI.

* `vli_ndr_permit`is a variable for the number of Very-Low Income non-Deed Restricted units proposed with issued building permits. VLI are households from 0-50% AMI.

* `li_dr_permit` is a variable for the number of Low Income Deed Restricted units proposed with issued building permits. LI are households from 50-80% AMI.

* `li_ndr_permit` is a variable for the number of Low Income non-Deed Restricted units proposed with issued building permits. LI are households from 50-80% AMI.

* `mi_dr_permit` is a variable for the number of Moderate Income Deed Restricted units proposed with issued building permits. MI are households from 80-120% AMI.

* `mi_ndr_permit` is a variable for the number of Moderate Income non-Deed Restricted units proposed with issued building permits. MI are households from 80-120% AMI.

* `ami_permit` is a variable for the number of Above-Moderate Income non-Deed Restricted units proposed with issued building permits. AMI are households above 120% AMI. This is not to be confused with the term AMI for `Area Median Income`

* `date_permit` is  the date within the reporting year that the building permit was issued by the jurisdiction.

* `units_permit` is the sum of units that were permitted for very-low, low, moderate, and above moderate income as stated above.

**Certificates of Occupancy:** the number of units that issued certificates of occupancy or other form of readiness (e.g., final inspection, notice of completion) during the reporting year by affordability level and whether the units are deed restricted or non-deed restricted.

* `vli_dr_occcert` is a variable for the number of Very-Low Income Deed Restricted units proposed with Certificates of Occupancy. VLI are households from 0-50% AMI.

* `vli_ndr_occcert` is a variable for the number of Very-Low Income non-Deed Restricted units proposed with Certificates of Occupancy. VLI are households from 0-50% AMI.

* `li_dr_occcert` is a variable for the number of Low Income Deed Restricted units proposed with Certificates of Occupancy. LI are households from 50-80% AMI.

* `li_ndr_occcert` is a variable for the number of Low Income non-Deed Restricted units proposed with Certificates of Occupancy. LI are households from 50-80% AMI.

* `mi_dr_occcert` is a variable for the number of Moderate Income Deed Restricted units proposed with Certificates of Occupancy. MI are households from 80-120% AMI.

* `mi_ndr_occcert` is a variable for the number of Moderate Income non-Deed Restricted units proposed with Certificates of Occupancy. MI are households from 80-120% AMI.

* `ami_occcert` is a variable for the number of Above-Moderate Income non-Deed Restricted units proposed with Certificates of Occupancy. AMI are households above 120% AMI. This is not to be confused with the term AMI for `Area Median Income`

* `date_occcert` the date the certificate of occupancy or other form of readiness (e.g., final inspection, notice of completion) was issued for the project. For most jurisdictions, this is the final step before residents can occupy the unit.

* `units_occcert` is the number of Units Issued Certificates of Occupancy or other forms of Readiness. The sum of units that were issued a certificate of occupancy for very-low, low, moderate, and above moderate income,


**Other variables:**

* `ELI_units` an optional field for submitters. To gain a greater understanding of the level of building activity to meet the needs of extremely low-income households in the state, HCD ask they estimate, to the extent possible, the number of units affordable to extremely-low income households. This number is a subset of the number of units affordable to very low-income households.

* `sb35` is whether or not the APPLICATION SUBMITTED Pursuant to GC 65913.4(b)? Which is the SB 35 Streamlining clause

* `infill` is an optional field to gain a greater understanding of the level of infill housing activity in the state, HCD asks that they clarify if the housing units reported are infill by selecting “Yes” or “No.” See Definitions section for “infill housing units” definition.

* `asst_prog` if units received financial assistance from the city or county and/or other subsidy sources, this field will have affordability restrictions or covenants, and/or recapture of public funds upon resale. Refer to [2018 APR Instructions PDF](https://hcd.ca.gov/community-development/housing-element/docs/Housing-Element-Annual-Progress-Report-Instructions-2019.pdf) on page 12 for more information.

* `dr_type` if units in the project are considered affordable to very-low, low, and/or moderate income households due to a local program or policy, such as an inclusionary housing ordinance, regulatory agreement, or a density bonus.

    * “INC” if the units were approved pursuant to a local inclusionary housing ordinance.
    * “DB” if the units were approved using a density bonus.
    * “Other” for any other mechanism.

* `lcl_determ` Housing without Financial Assistance or Deed Restriction: If the units are affordable to very-low, low and moderate income households without financial assistance and/or deed restrictions

* `dr_afford_term` if units have committed financial assistance and/or are deed restricted,this gives the duration of affordability or deed restriction. If units are affordable in perpetuity, the entry will say 1000.

* `demoed_units` this section is to report if the project and associated APN, has a permit, entitlement or certificate of occupancy in the reporting year, and the APN previously had demolished or destroyed units. IT contains the number of units demolished.

* `demoed_type` means “demolished” if the units were torn down. Select “Destroyed” if the units were lost due to fire or other natural disaster.

* `demoed_tenure` - Demolished/Destroyed Units Owner or Renter: “R” for renter or “O” for owner

* `notes` are notes regarding the project


## **URL LOCATION FOR EACH JURISDICTION:**
* Oakland: https://www.oaklandca.gov/documents/2018-housing-element-annual-progress-report-1
* San Francisco: Not Publicly Available
