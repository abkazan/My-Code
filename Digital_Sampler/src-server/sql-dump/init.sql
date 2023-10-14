CREATE TABLE sample (

    /* Essential data */
    primary_key     INT             NOT NULL AUTO_INCREMENT,
    upload_date     DATETIME        NOT NULL, 

    file_data   MEDIUMBLOB            NOT NULL,
    file_name   VARCHAR(255)    NOT NULL,
    file_ext    VARCHAR(5)      NOT NULL, /* Can be calculated @upload */
    duration    INT             NOT NULL, /* Can be calculated @upload */

    /* Non-essential data */
    title       VARCHAR(255)    NULL,
    artist      VARCHAR(255)    NULL,
    album       VARCHAR(255)    NULL,
    genre       VARCHAR(255)    NULL,
    instrument  VARCHAR(255)    NULL,
    album_art   BLOB            NULL,
    album_art_ext VARCHAR(5)    NULL,
    
    bpm             INT             NULL,
    key_signature   VARCHAR(15)     NULL,
    
    PRIMARY KEY (primary_key)
);