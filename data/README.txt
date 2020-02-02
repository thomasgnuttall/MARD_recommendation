MARD: Multimodal Album Reviews Dataset

MARD contains texts and accompanying metadata originally obtained from a much larger dataset of Amazon customer reviews collected by Julian McAuley, and enriched with music metadata from MusicBrainz, and audio descriptors from AcousticBrainz. MARD amounts to a total of 65,566 albums and 263,525 customer reviews.


The dataset contains 2 files: 

mard_metadata.json: In this file there is an entry per album. Depending on the album, the following fields may be available or not. The list of possible fields per entry: 


Source: Amazon 

amazon-id: The Amazon product id. You can visualize the album page in amazon adding this id to the following url "www.amazon.com/dp/" 
artist: The artist name as it appears in Amazon 
title: The album title as it appears in Amazon 
related: 
    also bought: Other products bought by people who bought this album 
    buy_after_viewing: Other products bought by people after viewing this album 
price: The album price 
label: The record label of the album 
categories: The genre categories in Amazon 
sales_rank: Ranking in the Amazon music sales rank 
imUrl: Url of the album cover 
artist_url: The url of the artist page in amazon. You must add "www.amazon.com" at the beginning to access this page 
root-genre: The root genre category of the album, extracted from the categories field. 


Source: MusicBrainz 

artist-mbid: The MusicBrainz ID of the artist 
first-release-year: The year of first publication of the album 
release-group-mbid: The MusicBrainz ID of the release group mapped to this album title 
release-group: The MusicBrainz ID of the first release in the release-group of this album, used to extract the tracks info 
songs: List of tracks in the album 
    title: Title of the track 
    mbid: MusicBrainz recording ID of the track. Used to map with AcousticBrainz. 


acousticbrainz_descriptors/ This folder contains one file per album with the audio descriptors of its first track. In the folder, each filename has the format amazonid_mbid.json. Using the song mbid, it is possible to get all other album songs related acoustic descriptors from the AcousticBrainz web service. The number of songs with information in AcousticBrainz is constantly growing, so the numbers indicated in the Table represents the availability in the moment of the dataset creation. 


mard_reviews.json The file containing the reviews text with some metadata associated to each review. Each entry has the following fields: reviewerID, product-id, reviewerName, helpful, reviewText, overall, summary, unixReviewTime, reviewTime. 

Each line in these 2 files is a json dictionary. To load the file you must read a line and then eval the json expression. Python code example: 

fname = "mard_metadata.json" 
with open(fname, 'r') as f: 
    for line in f: 
        data = eval(line) 


Scientific References

For more details on how these files were generated, we refer to the following scientific publication. We would highly appreciate if scientific publications of works partly based on the MARD dataset quote the following publication:

Oramas, S., Espinosa-Anke L., Lawlor A., Serra X., & Saggion H. (2016). Exploring Customer Reviews for Music Genre Classification and Evolutionary Studies. 17th International Society for Music Information Retrieval Conference (ISMIR'16). 


Conditions of Use

Dataset compiled by Sergio Oramas based on a previous dataset by Julien McAuley. Copyright ©2016 Music Technology Group, Universitat Pompeu Fabra. All Rights Reserved.


Feedback

Problems, positive feedback, negative feedback... it is all welcome! Please help me improve MARD by sending your feedback to:
sergio.oramas@upf.edu AND mtg-datasets@llista.upf.edu

In case of a problem report please include as many details as possible.
