The overlapping books in the two annotated dataset collections are the following:
* Alice's Adventures in Wonderland
* David Coperfield
* Dracula
* Emma
* Frankenstein
* Adventures of Huckleberry Finn
* Moby Dick
* Oliver Twist
* Pride and Prejudice
* The Call of the Wild
* Ulysses
* Vanity Fair

Certain manual changes have been done to the individual books:
* Alice in Wonderland: *Maâ€™am* -> *Ma'am*
* David Copperfield: *oâ€™clock* -> *o’clock* 
* Dracula: none
* Emma: none
* Frankenstein: none
* Adventures of Huckleberry Finn: *sumf â€™n* -> *sumf'n*; *more â€™n* -> *more'n*
* Moby Dick:
    * additional entity
    ```
        Loomings O
        . O         <- removed from Dekker et al., does not exist in LitBank
        Call O    
    ```
    ```
    alleys	B-FAC
    ,	O
    streets	B-FAC
    and	O
    avenues	B-FAC
    ,	O           <- extra comma removed from LitBank, does not exist in Dekker et al.
    --	O
    north	O
    ```
    ```
    ?	O
    --	O
    Water	O           <- missing -- after this row in LitBank. Removed from Dekker et al.
    there	O
    is	O
    not	O
    a	O
    drop	O
    ```
    ```
    their	B-FAC
    huge	I-FAC
    bakehouses	I-FAC       <- bake - houses in Dekker et al. - collapsed 
    the	I-FAC
    pyramids	I-FAC
    ```
    ```
    into O
    the O
    fore-castle	O       <- one word in Dekker et al. - split
    , O
    ```
    * Different sentenses (As the extra two tokens in Litbank are not marked as an entity, we remove those.)
        ```
        Litbank:
            Some	O
            leaning	O
            against	O
            the	O
            spiles	O
            ;	O
            some	O
            seated	O
            upon	O
            the	O
            pier	O
            -	O
            heads	O
            ;	O
            some	O
            looking	O
            over	O
            the	O
            bulwarks	O
            glasses	O       <-
            !	O           <-
            of	O
            ships	O
            from	O
            China	B-GPE
        Dekker et al.:
            Some O
            leaning O
            against O
            the O
            spiles O
            ; O
            some O
            seated O
            upon O
            the O
            pier O
            - O
            heads O
            ; O
            some O
            looking O
            over O
            the O
            bulwarks O
            of O
            ships O
            from O
            China O
            ; O
        ```
* Oliver Twist: none
* Pride and Prejudice: none
* The Call of the Wild: *deliver \` m* -> *deliver'm*, *choke \` m* -> *choke'm*, *cure \` m* -> *cure'm*, *takin ` m* -> *takin'm* (Dekker et al.)
Adapted (all three) Dekker et al. to Litbank in order to not add anything, but only remove non marked entities.
```
    Dekker:
    you O
    deliver O
    ` O
    m O
    
    Litbank:
    you	O
    deliver	O
    'm	O
```
*'m. O* was split into *'m O* and *. O* (Dekker et al.)

```
    I	O
    'm	O
    takin	O
    '	O       -> extra token ' removed
    'm	O
    up	O
    for	O
    the	B-PER
    boss	I-PER
```
* Ulysses: 
```
    you	O
    ...	O
    .	O           <- LitBank extra . removed
    He	O
    broke	O
```
```
    says	O
    you	O
    have	O
    g.	O
    p.	O
    i.	O           <- i. split in two tokens in Dekker et al. -> collapsed
```
* Vanity Fair: none