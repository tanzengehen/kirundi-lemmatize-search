Feature: kirundi lemmatizer
    As a Linguist
    I want to lemmatize a rundi text
    to use the data in search and analyse tools

Feature: kirundi lemma search
    As a Linguist
    I want to search for words and word combinations in rundi texts based on lemmatization

Feature: contribute to the dictionary
    As a Linguist
    I want to check words that are unknown to the dictionary
    to put them into the database 
    or to mark them as Named Entities 
    or to mark them as spelling mistakes

Background:
    Given the following lemmata:
    | id | ... |

    Given the following text:
    "Abantu bose barashaka gukunda umuntu mwiza. Mu majoro yose hari umwijima."

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Kirundi-NLP" in the title
    And I should not see "404 Not Found"

Scenario: Lemmatize a rundi text
    When I visit the "Home Page"
    And I set "textfile" to "path/to/filename.txt"
    And I press the "Lemmatize" button
    Then I should see the message "Success"
    And I should see "Numbers of Characters"
    And I should see "Numbers of Tokens"
    And I should see "Numbers of Types (unknown)"
    And I should see "Numbers of Lemmata"
    And I should see "Numbers of Named Entities"
    And I should see "Numbers of Foreign Words"
    And I should see "Numbers of Singletons"
    And I should see "frequency distribution" filename
    And I should see "tagged" filename
    And I should see "lemma soup" filename
    And I should see "lemma soup without stopwords" filename
    And the button "download frequency distribution" should be active
    And the button "download tagged file" should be active
    And the button "download lemma soup" should be active
    And the button "download lemma soup without stopwords" should be active
    When I press the button "download frequency distribution"
    Then the dialog "Save" should open
    When I press the button "download tagged file"
    Then the dialog "Save" should open
    When I press the button "download lemma soups"
    Then the dialog "Save" should open
    When I press the button "lemma soup without stopwords"
    Then the dialog "Save" should open

Scenario: Search in a text by lemmata
    When I visit the "Home Page"
    And I write a "word" in the searchfield
    Then a row named "word" should be added in the searchtable at "word position"

    When I write a "[PoS]" in the searchfield
    And "[PoS]" is in PoS-List
    Then in row "[PoS]" the radiobutton "PoS" should be selected
    And in row "[PoS]" the checkbox NOT should be selectable
    And in row "[PoS]" the radiobutton "Token" should be inactive
    And in row "[PoS]" the radiobutton "Lemma" should be inactive
    And in row "[PoS]" the radiobutton "Wildcard" should be inactive
    And I should not see the message "Specify your search"

    When I press "[PoS]" in PoS-List
    Then the word "[PoS]" should be added in the searchfield at actual cursor position 
    And a row named "[PoS]" should be added in the searchtable at "word position"
    And I should not see the message "Specify your search"

    When I write " * " in the searchfield
    Then a row named "*" should be added in the searchtable at "word position"
    And in row "*" I should not see the message "Specify your search"
    And in row "*" the radiobutton "Lemma" should be inactive
    And in row "*" the radiobutton "PoS" should be inactive
    And in row "*" the checkbox NOT should be inactive

    When I check the ckeckbox NOT in row "word"
    Then the name of the row should be "¬word"

    When I uncheck the ckeckbox NOT in row "¬word"
    Then the name of the row should be reset to "word"

    When the searchfield is empty
    And I press button "Search"
    Then I should see the message "Specify your search"

    When in row "word" the radiobutton "Type" is not selected
    And in row "word" the radiobutton "Lemma" is not selected
    And in row "word" the radiobutton "PoS" is not selected
    And in row "word" the radiobutton "Wildcard" is not selected
    And I press button "Search"
    Then I should see the message "Specify your search"

    When "searchfile" is empty
    And I press button "Search"
    Then I should see the message "Select a json file for your search"
    And the dialog "Open" should open
    But only json and txt files are valid to load

    When I press button "Load File"
    Then the dialog "Open" should open
    But only json and txt files are valid to load


    When I set "searchfield" to "gushaka [VERB]"
    Then I should see a row named "gushaka" in the searchtable
    And in row "gushaka" the radiobutton "Token" should be selectable
    And in row "gushaka" the radiobutton "Lemma" should be selectable
    And in row "gushaka" the radiobutton "PoS" should not be selectable
    And in row "gushaka" the radiobutton "Wildcard" should not be selectable
    And in row "gushaka" the checkbox NOT should be selectable
    And I should see a row named "[VERB]" in the searchtable
    And in row "[VERB]" the radiobutton "Token" should be inactive
    And in row "[VERB]" the radiobutton "Lemma" should be inactive
    And in row "[VERB]" the radiobutton "PoS" should be selected
    And in row "[VERB]" the radiobutton "Wildcard" should not be selectable
    And in row "[VERB]" the checkbox NOT should be selectable

    When I set "searchfile" to "path/to/filename.json"
    And I set "searchfield" to "gushaka [VERB]"
    And I select radiobutton "Lemma" in row "gushaka"
    And I check the checkbox NOT in row "[VERB]"
    Then I should see a row named "gushaka" in the searchtable
    And in row "gushaka" the radiobutton "Token" should not be selected
    And in row "gushaka" the radiobutton "PoS" should not be selectable
    And in row "gushaka" the checkbox NOT should be un-selectable
    And I should see a row named "¬[VERB]" in the searchtable
    
    When I set "searchfile" to "path/to/filename.json"
    And I set "searchfield" to "gushaka VERB"
    And I select radiobutton "Lemma" in row "gushaka"
    And I press button "Search"
    Then I should see the message "Success"
    And I should see "showing first 20 of 1 results"
    And I should see "barashaka gukunda"
    And I should see "search result" filename
    And the button "download search result" should be active
    When I press the button "download search result"
    Then the dialog "Save" should open
    
    
Scenario: Contribute to Dictionary
    When I visit the "Home Page"
    And the button "download frequency distribution" is active
    And the "Numbers of Types (unknown)" is set
    Then the button "contribute" should be active
    When I press button "contribute"
    Then I should see the message "Success"
    And a table should open with 20 most frequently unknown Types
    And I should see the check box "Can we contact you, if we might have a question?"
    And the button "next twenty" should be active
    And I should see the button "Send to check"
    And I should see a column "Lemma"
    And I should see a column "prefix"
    And I should see a column "stem"
    And I should see a column "pronounciation"
    And I should see a column "alternative spellings for Lemma"
    And I should see a column "PoS" with dropdown menu
    And I should see a column "Class Singular"
    And I should see a column "Class Plural"
    And I should see a column "Perfective"
    And I should see a column "Source Language"
    And I should see a column "stem with common Suffixes (ingobotozo)"
    And I should see a column "remarks"
    When I select "NOUN" in PoS
    Then in this row column "Class Singular" with dropdown menu should be active
    And in this row column "Class Plural" with dropdown menu should be active
    And in this row column "Perfective" should be inactive
    And in this row column "common Suffixes (ingobotozo)" should be inactive
    When I select "VERB" in PoS
    Then in this row column "Perfective" should be active
    And in this row column "common Suffixes (ingobotozo)" should be active
    And in this row column "Class Singular" with dropdown menu should be inactive
    And in this row column "Class Plural" with dropdown menu should be inactive
    When I select "ADV" in PoS
    Then in this row column "Perfective" should be inactive
    And in this row column "common Suffixes (ingobotozo)" should be inactive
    And in this row column "Class Singular" with dropdown menu should be inactive
    And in this row column "Class Plural" with dropdown menu should be inactive
    When I select "ADJ" in PoS
    Then in this row column "Perfective" should be inactive
    And in this row column "common Suffixes (ingobotozo)" should be inactive
    And in this row column "Class Singular" with dropdown menu should be inactive
    And in this row column "Class Plural" with dropdown menu should be inactive
    When I select "CONJ" in PoS
    Then in this row column "Perfective" should be inactive
    And in this row column "common Suffixes (ingobotozo)" should be inactive
    And in this row column "Class Singular" with dropdown menu should be inactive
    And in this row column "Class Plural" with dropdown menu should be inactive
    When I select "INTJ" in PoS
    Then in this row column "Perfective" should be inactive
    And in this row column "common Suffixes (ingobotozo)" should be inactive
    And in this row column "Class Singular" with dropdown menu should be inactive
    And in this row column "Class Plural" with dropdown menu should be inactive
    When I select "PROPN" in PoS
    Then in this row column "Perfective" should be active
    And in this row column "common Suffixes (ingobotozo)" should be active
    And in this row column "Class Singular" with dropdown menu should be active
    And in this row column "Class Plural" with dropdown menu should be active
    When I select "FOREIGN WORD" in PoS
    Then in this row column "Language" should be active
    When I press the button "next twenty"
    Then the table should add 20 more rows
    When I press the button "Send to check"
    Then the table should be send
    And I should see the message "Success"
    And I should see the message "Thanks"
