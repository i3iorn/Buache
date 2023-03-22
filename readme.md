# ***___Buache___***

=============================================================================

## 1. Vision

An API for address verification and lookup based on aggregated data from many sources.

## 2. Etymologi

From the cartographer Phillipe Buache.
https://en.wikipedia.org/wiki/Philippe_Buache

## 3. Concepts
___

### 3.1 Resource

Any instantiated class that refers to a external party to the api.

### 3.2 Declarations

Json formatted documents that keeps all information that is unique to the resource declared. Declarations are stored 
in Buache/declarations. The naming convention is <resource_name>_declaration.json and each file contains a list of all 
resources of that type.

### 3.3 Source

Sources are exactly what it sounds like. Different places where you can find address data. All sources are instantiated 
by the Source class. The Source class contains all the necessary methods for establishing communication with a source 
so that the source_declaration

### 3.4 Augmentors

External tools that can be used to enrich or refine address data. Is instantiated by the Augmentor class.

### 3.5 Adapter

Different ways of communicating with a resource. The primary ones will be API and File. Sub adapters of API are 
Authenticated and Unauthenticated. Sub adapters for File would be FTP, local, or HTTP.

All adapters have common methods for accessing them and extract data that are generic as to which source is used.
Any necessary processing is handled internally.

### 3.6 Address

A globally unique humanreadable text that identifies one specific location on earth. The Address class contains 
methods for manipulating and/or querying the address.

#### 3.6.1 Address Components
An address component carries just a few simple methods. 

* Validation
* Formatting

#### 3.6.2 Hierarchy

Defines the linkage between address components.

1. Continent
2. Country
3. Region
4. Sub-region / Administrative Region
5. Municipality / County
6. City
7. Borough / Zip
8. Street
9. Street number
10. Entrance
11. Apartment number

### 3.6.3 Related data

* Time zone
* Languages
* Cultures
* Religions
* Address type