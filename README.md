## XXE Introduction
XML External Entity (XXE) Injection is a vulnerability that allows an attacker to manipulate the processing of XML data.  Similar to other injection techniques, this allows the attacker access to data and services within the vulnerable system.  The XXE vulnerability is ranked at #4 on OWASP's Top 10 Web Application Security Risk.  

## XML Background
eXtensible Markup Language (XML): a language simitlar to HTML that was designed to store and transport data.  The document is stored in plaintext, so it is human readable.  An example of XML and its syntax is shown below: 
```
<item>
    <elem1>Element One</elem1>
    <elem2>Element Two</elem2>
</item>
```

Document Type Definition (DTD): an agreed upon structure of what is expected in an XML document.  This document can be defined internally or externally. (We will see later why allowing external definitions of the DTD can lead to the XXE vulnerability).  

## Testing the App
Clone the repo to your local directory.
```
git clone https://github.com/Meltanki/xxe-lesson.git
```
Install the necessary requirements to fun the application.  
```
pip install -r requirements.txt
```
Run the application.
```
python app.py
```
Navigate to ```http://localhost:5000``` to access the application.  

The application is very simple.  The bottom section displays the "Items" that are in the database.  The top section allows us to upload an xml file from our local system.  If the XML file is formatted correctly, then the Item will be added to the list and we should see that Item display in the list in the bottom section.  

Click on 'Choose File' and select 'sample.xml' from the repo.  After clicking 'Process XML', you should see the data from sample.xml show up in the lower list.  Try editing the text within 'sample.xml' and uploading the new xml file to verify that your new input is displaying in the "Items" list.  

## Exploiting the App
Review the contents of the 'attack.xml' file and notice the following lines:
```
<!DOCTYPE newdoc
[
	<!ENTITY xxe SYSTEM "file:///secrets.txt" >
]>
```
These lines introduce a new ```DOCTYPE``` element that defines an external entity (```xxe```) containing a path to a file (```secrets.txt```).  We then use the defined external entity within the xml document as shown in the line below.  
```
<title>&xxe;</title>
```
In the running application, upload the 'attack.xml' file and click the 'Process XML' button.  You should see the contents of the 'secrets.txt' file show in the list in the bottom of the screen. The 'secrets.txt' file is an example filled with dummy data.  This example is meant to show that the contents of any file on they system can be dumped to the screen. 

## Mitigation
In order to help mitigate XXE injection the XML processor should be configured to use a local static DTD and disallow any declared DTD in the XML document.  In our specific application, we use the ```lxml``` library to parse XML.  This library allows the addition of external entities, but other libraries (such as ```etree``` or ```minidom```) will raise a ParseException with external entities.  Please review the the Python official documentation for further information on XML Processing Modules (https://docs.python.org/3/library/xml.html#the-defusedxml-and-defusedexpat-packages)
