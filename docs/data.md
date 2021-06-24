## Litbank
Link: [https://github.com/dbamman/litbank](https://github.com/dbamman/litbank)

Last commit: a371cd678701fc98371355b328a1a6c4b58508a3

Issues:
* The entites in the novels are analysed on different levels, which means that the files do not have the same structure (num of columns).
* The entity annotation layer of LitBank covers six of the ACE 2005 categories in text: People (PER), Facilities (FAC), Geo-political entities (GPE), Locations (LOC), Vehicles (VEH), Organizations (ORG)
* Litbank treats words containing a hyphen as one entity (e.g. WAISTCOAT-POCKET). We split those for consistency. 

## Dekker et al. 
Link: [https://github.com/Niels-Dekker/Out-with-the-Old-and-in-with-the-Novel](https://github.com/Niels-Dekker/Out-with-the-Old-and-in-with-the-Novel)

Last commit: ad31ce1fa515dceabb8febbaa7aa235f3de47ebd

Only annotates people (I-PERSON) and does not differenciate between first token of entity and rest (i.e. no B-PERSON used)