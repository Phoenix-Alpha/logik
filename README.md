# LogiK

LogiK is a platform specialized in logistic.

Here are the different users of the solution :

- Integrators : They have access to the Integrator Center and manage environments, modules, front-end for end-users, store etc.. They have access to all the features of the Integrator Center
- End-users : They have access to the front-end developped by the integrator. It's a combination of modules installed in a environment. The purpose is to allow them to manage their warehouses
- Warehouse users : They have access to a little-front (Developed by the integrator with the UI Manager) end with a special phone allowing them to scan article in a warehouse, prepare shipments etc..

The Integrator centor is a combination of features. The purpose is to give the opportunity to the users to create modules, deploy them, sell them..
Modules are composed of :

- Documents (Document manager)
- Widgets (Widget manager)
- Functions (Function manager) : For example, create a label automatically when you shipped a parcel
- Flows (Flow manager) : a series of functions
- Dictionary Manager : CMS containing all the data (tables / fields) of a module
- UI Manager

## Documents Manager

List of documents linked to an environment.
Each document is linked to a module. Every user can create document in this section (For example, a label for a parcel)

## Dictionary Manager

The dictionary manager is a CMS like allowing a user to create tables with specific fields and links between tables. Like a database.
All the tables created are attached to a module and allows to have all the fields / tables for a module

## Flows Manager

Flow manager allows user to combine a series of functions with a start and an end. Functions will be written in Python and used in the Function Manager

## Functions Manager

In this section, user can create function using an IDE and Python

## UI Manager

This is an IDE allowing the integrator to develop the front-end interface for end customers. This is where the integrator defines all access to the modules and the final UI

## Store

The store is the place where you find all the modules. The ones created by all the integrators.
You can find the modules created by the current integrator (The one who is connected) in a dedicated tab.
A module can be installed / deleted in a environment

## Rights management

The integrator can add collaborators each having different roles. Each role provides access to a number of features of the Integrator Center

## Spaces management

The integrator can manage all the spaces for these customers. A space has a URL to access the end user's front-end application

## Front-end App

Front-end application for end-users. All the front is built by the integrator with the UI Manager and allowed end-users to manager their warehouse thanks to the module developed by the integrator

## Mobile App

It is a mobile application allowing warehouse users to be able to carry out actions specific to a warehouse such as scanning articles etc.

## LogiK Admin

It is a web page that allows administrators to manage the submission of modules on the store, the invoicing part with integrators, etc.
