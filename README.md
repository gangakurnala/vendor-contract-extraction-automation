# vendor-contract-extraction-automation

## Problem
We have 500+ vendor contracts in PDF and Word format. We need to:
- Extract services offered by each vendor
- Extract rates with terms mentioned in the contract
- Create SAP purchase information records (packing info records)

## Goal
Build an automation using Claude AI to:
1. Process all contracts automatically
2. Extract information from structured / unstructured  data (vendor name, services, rates, payment terms, etc.)
3. Output data in format ready for SAP

## Current Status
- Identifying sample contracts
- Defining SAP field requirements
- Planning Claude integration approach

## Sample Contracts
See `sample-contracts/` folder for examples

## Fields Needed for SAP
See `sap-fields-needed.md` for complete requirements
