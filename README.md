# Wikiexporter - a tool to export a github wiki to an html file

A very simple github wiki exporter … really minimal right now
( ** Works only for markdown! ** )


 Usage:
 
 	python wikiexporter.py path_to_your_root_document output_file.html [--bootstrap] [--include-children]
 	
 	
Dependencies are in requirements.txt
 	
Switches: 
* --include-children: The root doc and all documents linked will be included in html
   and all links will be transformed to local anchors. Otherwise only the root document
   will be converted
   
* --bootstrap: includes css from twitter bootstrap. the css is inlined in the output html

#TODOS

*  Support for other markup elements (images, ecc)
*  Export to pdf 
*  Support other markup formats  
*  Options for parsing doc (recursive or not)
*  Style options
*  better CSS and Js inclusions … (theme - like)
*  Package it