# Text Editor

## The Problem

Designing a Text Editor with focus on the performance of Cut, Copy and Paste Operations.

## My approach

After going through the problem and existing implementation, I couldn't think of any way to enhance the performance, especially when using strings. Only logical thing seemed to be to try and come up with another datastructure to store strings that might make the performance faster. After going through all data structures I know and researching on the internet, I learned about Ropes Data Structure. According to various sources Ropes is used by various text editing softwares to make operations more efficient. I found a rough overview on Wikipedia but couldn't find any proper implemetation anywhere so I had to come up with my own.

## How to Run

To run the code using terminal or command prompt use the following command:
	
	python editor.py

Also to run you might have to change the path for dictionary file depending on whether you are using Mac/linux or Windows OS.

## Design/ Tradeoffs

After implementing ropes and testing performance for given testcase, I realized it was even slower than original implementation. I tried for even larger string but still same. Finally I decided to test it for extremely large document, and I saw significant increase in performance of cut-copy-paste operations. But it wasn't without tradeoffs. While cut, copy and paste operations were significantly faster with ropes, retreiving whole document in case of larger documents was significantly slower. And since to check for spellings I need to retreive the document first, then split it into words and compare with dictionary, misspellings functions performance suffered even more.

> Note: If document size is large and cut copy paste operations are performed frequently with few document retrievals, Ropes is desirable. If document size is small or there are more frequent document retreival operations Ropes might not be best choice.

## Future Scope

I have undo and redo functionality using stacks. Default number of undo/redo are 100 although that can be changed by passing a value to constructor. I have also added load and save functionalities to save and load document from a txt file. Given more time I would have like to functionalities like Find and Replace.



> Note: My ropes implementation is combination of wikipedia definition, partial pseudocode or implementation found on internet and my own understanding. It is entirely possible my implementation might not be 100% accurate or have more than few bugs but working with a completly new data structure I did the best I could do. 

## Testing

I have included a file "pride.txt" that I used to test my performance. Please note that performance for operations like get_text, misspellings and save would be much worse for very large document like "pride.txt", so I would suggest to use a smaller size document to test those functionalities.



