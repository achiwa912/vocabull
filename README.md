# vb.py - VocaBull

VocaBull is a small command line tool that helps your vocabulary building.

## How VocaBull can help you

With VocaBull, you can repeat typing words to memorize again and again, until you memorize them.  It tracks your progress and only challenges you with words which you have not memorized yet.

It goes like this:
* VocaBull gives you a quiz for a new word
* If you can't type the word, you are forced to type it for 4 times
* If you typed it correctly, you are still to type it for twice
* VocaBull gives you quizes from outstanding 10 words so that you can focus 10 words at a specific time
* If you typed a word correctly for several times, it deems that you have memorized theword
* In this case, it replaces the word with a new one.  This way, outstanding 10 words are continuously changing

# Prerequisites

* Python 3.6 or later (It uses f-strings)
* A word book file (see below)

# Usage
## How to run

```bash
python vb.py <WordBookFile>
```
You can use samples.txt (included in this repository) as a sample word book file which includes 10 words.  First, you will be greeted like this.  As you use samples.txt, it loads just 10 files.

```bash
% python vb.py samples.txt 
=== VocaBull - Help your vocabulary building ===
    10 words loaded.
```

## How to practice

Then practice starts.  You are now prompted to type a word to memorize.  You are asked what is the word for "exaggerated figure of speech" and you need to type the word.

```bash
    *** S: save, L: show learning set, Q: save and quit
    exaggerated figure of speech? 
```
As you can't guess the word, you typed as "aaa".

```bash
    exaggerated figure of speech? aaa        
    *** Incorrect.  Let's practice 4 times.
    > The rhetoric soared into lagrant hyperbole.
    exaggerated figure of speech: hyperbole
1/4 exaggerated figure of speech?
```
The answer was "hyperbole".  The line starts with '>' is the sample sentence if one is in the word book file.  You need to type the word for 4 times to proceed to the next quiz.

```bash
1/4 exaggerated figure of speech? hyperbole
2/4 exaggerated figure of speech? hyperbole
3/4 exaggerated figure of speech? hyperbole
4/4 exaggerated figure of speech? hyperbole
---
    *** S: save, L: show learning set, Q: save and quit
    generous?
```
Then, you are asked the next word.  What is one for "generous"?

## The learning window and the learning set

The tool tracks your progress.  If you typed a word correctly for several times, it thinks you've memorized the word for now.  Then it removes the word from the current "learning window" and a new word will be added to it.

The "learning window" consists of about 10 outstanding words.  The tool gives you quizes always from the learning window.  That is, you need to try memorizing 10 words at a specific time.  If you memorize a word or two in the learning window, they are replaced with new ones.

If the number of words in the word book are relatively big (100 or more), the tool will split the entire words into chapters/sets that each has 100 words (or less).  When you run the tool and if the word book is large, you'll be asked which set/chapter to study.  A set is also called a "learning set".

* Learning Window - 10 currently memorizing words.  As you memorize words, the learning window (kind of) moves within the learning set.
* Learning Set - A chapter/set of a word book and a learning set has 100 words.  The current learning set is the one you are studying now.
* Learning Book - The word book that can have as many words as you want.

## The commands

You can use commands when you see this "*** S: save..." message.
```bash
    *** S: save, L: show learning set, Q: save and quit
    exaggerated figure of speech? 
```
Instead of typing the word, you can type "S", "L" or "Q".

"S" is for save.  It will save your progress.  The saved data will be loaded automatically when you run the tool with the same word book.  The save file name is <wordfile>.pickle.

```
    *** S: save, L: show learning set, Q: save and quit
    high praise? S
Saved 10 words to samples.pickle
    *** S: save, L: show learning set, Q: save and quit
    high praise? 
```

"L" shows the "current learning set".  The current learning set is the set/chapter that you are currently studying.

```
    *** S: save, L: show learning set, Q: save and quit
    high praise? L
0 hyperbole - 0/0/0/1
1 munificent - 1/0/1/0
2 prevarication - 1/0/1/0
3 tyro - 1/0/1/0
<snip>
```

"Q" is for save&quit.  If you don't want to save your progress, you can use Ctrl-C to aboart the tool.

# Rationale

What is the single, most important thing to memorize new words?  I believe it's repetition.  It would be up to the individual or the difficulty of the word itself for how many times you need to repeat trying to memorize a word, but repetition is the key to memorize new words.

Traditional vocabulary books or flash cards are not very efficient for the repitition process in that they don't track your progress.

VocaBull is efficient in this regard.  That is, it tracks words you have memorized and word you have not yet.  And it gives you quizes only of words you have not memorized.


# Word book file format

vb.py supports two word book file format types.

The first one is "word" "meaning" "sentence" separated by tabs '\t'.  "sentence" is optional.  For example,

```
hyperbole	exaggerated figure of speech	The rhetoric soared into lagrant hyperbole.
```
The good thing about this format is that you can just copy and paste to create a word book file from various web sites such as: https://www.majortests.com/sat/wordlist.php  Note that sample sentences are optional.


The second format type is:
```
--
<word>
<meaning>
<sentence>
```
The "--" line is a word separator line.  The top and bottom lines need to be the separator lines.  "sentence" is also optional.  samples.txt included in the repository is of this format type.

# License info

VocaBull is under [MIT license](https://en.wikipedia.org/wiki/MIT_License).

VocaBull - Copyright (C) 2021 Kyosuke Achiwa