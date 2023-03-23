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
3. Administrative Region Large
4. Municipality
5. City
6. Administrative Region Medium 
7. Zip
8. Street
9. Street number
10. Entrance
11. Apartment number

#### 3.6.3 Related data

* Time zone
* Languages
* Cultures
* Religions
* Address type

### 3.7 Address Parsing

#### 3.7.1 Address breakdown

#### 3.7.1.1 ___String parts using sliding window___

Starting with 1 character we break up the address string into pieces of increasing length up til len(Address) / 2 
or 12 whichever is larger.
Example for 1-3 characters using "Daggränd 17 186 66 Hedeby":

1 Character

|0| 1   | 2   | 3   | 4   | 5   | 6   | 7   | 8   | 9   | 
|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| D   | a   | g   | g   | r   | ä   | n   | d   |     | 1   |
| 7   |     | 1   | 8   | 6   |     | 6   | 6   |     | H   |
| e   | d   | e   | b   | y   |     |     |     |     |     |

2 Characters

| 0   | 1   | 2   | 3   | 4 | 5   | 6   | 7   | 8   | 9   | 
|-----|-----|-----|-----|---|-----|-----|-----|-----|-----|
| Da  | ag  | gg  | gr  | rä | än  | nd  | d   | 1   | 17  |
| 7   | 1   | 18  | 86  | 6 | 66  | 6   | H   | he  | ed  |
| de  | de  | eb  | by  |   |     |     |     |     |     |

3 Characters

| 0   | 1   | 2   | 3   | 4   | 5   | 6   | 7   | 8   | 9   | 
|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| Dag | agg | ggr | grä | rän | änd | nd  | d 1 | 17  | 17  |
| 7 1 | 18  | 186 | 86  | 6 6 | 66  | 66  | 6 H | He  | Hed |
| ede | deb | eby |     |     |     |     |     |     |     |

#### 3.7.1.2 ___Create a map___

All strings are trimmed and strings that have a space inside them are ignored. Parts are placed into a dictionary 
where the string parts are the keys. Example:

```
{
   agg: {
        street_number: None,
        street_name: None,
        ...
   },
   66: {
        street_number: None,
        street_name: None,
        ...
   }
}
```

#### 3.7.1.3 ___Apply rules___

Next we go through all the strings and apply all rules starting with the longest strings. 