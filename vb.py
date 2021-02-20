import sys
import random
import operator
from os import path
import json

config = {
    'lwin_size': 10,  # learning window size
    'lset_size': 100,  # learning set size
    'repeat_count': 3,  # repeat count to memorize
    'penalty_count': 4,  # repeat count when incorrect
    'debug': False,
}

study_flags = {
    'all': False,  # Studying the entire book
}

track_progress = {
    'pass': 0,  # today's pass count
    'fail': 0,  # today's fail count
    'memorized_count': 0,  # today's memorized count
}


def repeat_word(word, count=1):
    """
    Have user type the word for count times.

    Parameters:
    word (dict): Dictionary for a word
    count (int): How many times user must repeat
    """
    cnt = 0
    if word['sentence'] != '':
        print('    > ' + word['sentence'])
    print('    ' + word['meaning'] + ': ' + word['word'])
    while cnt < count:  # repeat count times
        w = input(str(cnt+1) + '/' + str(count) + ' ' + word['meaning'] + '? ')
        if w == word['word']:
            cnt += 1
        else:
            print('    *** Incorrect.  Try again.')


def fill_lwin(lset, lwin):
    """
    Create or fill the learning window (lwin) with words from 
    the learning set (lset).  lwin will have random words with
    the least score.

    Parameters:
    lset (list): The learning set
    lwin (list): The learning winow to be updated
    """
    lset_sorted = sorted(lset, key=operator.itemgetter('score', 'id'))
    for wd in lwin:
        # remove words already in lwin
        lset_sorted.remove(wd)
    while len(lwin) < config['lwin_size']:
        min_score = lset_sorted[0]['score']
        idx = 0
        if study_flags['all'] == True:
            min_score_cnt = sum(
                1 for dic in lset_sorted if dic['score'] == min_score)
            idx = random.randrange(min_score_cnt)
        lwin.append(lset_sorted.pop(idx))
        if len(lset_sorted) == 0:
            break


def load_book(book_path):
    """
    load word book and its save files, and create the learning book list.

    The word book format is either:
    - word + '\t' + meaning [+ '\t' + sentence] in a line; or
    - Two or three lines of word definition (word, meaning[, sentence])
      separated by the word separater line ('--').

    We use the words only appear in the word book file.  The save file is 
    to retrieve progress and study history info.  Word data that are not 
    in the word book file will be ignored.

    Parameters
    book_path (str): Path to the word book file to load
    """
    lbook = []
    idx = 0
    with open(book_path, 'rt') as fd:
        word = meaning = sentence = ''
        for line in fd:
            if line.startswith('--'):  # word separator
                if word != '':
                    lbook.append({'id': idx, 'word': word, 'meaning': meaning,
                                  'sentence': sentence, 'score': 0,
                                  'tmp_score': 0, 'total_pass': 0,
                                  'total_fail': 0})
                    idx += 1
                word = meaning = sentence = ''
            elif word == '':
                # For tab-separated word book format
                if '\t' in line:
                    worddef = line.strip().split('\t')
                    word = worddef[0].lower()
                    meaning = worddef[1]
                    if len(worddef) > 2:
                        sentence = worddef[2]
                    lbook.append({'id': idx, 'word': word, 'meaning': meaning,
                                  'sentence': sentence, 'score': 0,
                                  'tmp_score': 0, 'total_pass': 0,
                                  'total_fail': 0})
                    idx += 1
                    word = meaning = sentence = ''
                else:
                    word = line.rstrip().lower()
            elif meaning == '':
                meaning = line.rstrip()
            else:
                sentence = line.rstrip()

    # load the save file if exists
    json_path, _ = path.splitext(book_path)
    json_path = json_path + ".json"
    if path.exists(json_path):
        with open(json_path, 'r') as f:
            old_lbook = json.load(f)
        for old_word in old_lbook:
            new_word = next(
                (w for w in lbook if w['word'] == old_word['word']), None)
            if new_word != None:
                if old_word['total_pass'] != 0 or old_word['total_fail'] != 0:
                    new_word['total_pass'] = old_word['total_pass']
                    new_word['total_fail'] = old_word['total_fail']
                    new_word['score'] = old_word['score']
                    new_word['tmp_score'] = old_word['tmp_score']

    print(f"    {len(lbook)} words loaded.")
    return lbook


def save_lbook(lbook, book_path):
    """
    Save the progress of the learning book.  The save file is the
    same book file name + ".json" extension.

    Parameters:
    lbook (dict): The learning book dictionary to save
    book_path (str): The path to the word book file
    """
    json_path, _ = path.splitext(book_path)
    json_path = json_path + ".json"
    with open(json_path, 'w') as f:
        json.dump(lbook, f)
    print(f"    *** Saved {len(lbook)} words to {json_path}")
    print(
        f"        Passed/total: {track_progress['pass']}/{track_progress['pass']+track_progress['fail']}, memorized {track_progress['memorized_count']} word(s) today.")


def create_lset(lbook):
    """
    Create the (current) learning set (lset) from the learning book 
    (lbook).

    User will specify which set/chapter to study If lbook is larger
    than the lset size.

    Parameters:
    lbook (dict): the learning book dictionary

    Return:
    lset (dict): Created learning set
    """
    lset = []
    if len(lbook) > config['lset_size']:
        while True:
            setnum = len(lbook) // config['lset_size']
            if len(lbook) % config['lset_size'] != 0:
                setnum += 1
            i = input(f"    Which learning set to use (1-{setnum}; all)? ")
            if i.startswith('all'):
                lset = lbook[:]
                study_flags['all'] = True
                break
            else:
                study_flags['all'] = False
                try:
                    i = int(i)
                except:
                    continue
                if i <= setnum and i > 0:
                    idx = (i-1) * config['lset_size']
                    for _ in range(config['lset_size']):
                        lset.append(lbook[idx])
                        idx += 1
                        if idx >= len(lbook):
                            break
                    break
    else:
        lset = lbook[:]
    return lset


def command(command, lset, lbook, book_path):
    """
    run a command

    Parameters
    command (str): A command character
    lset (dict): Learning set
    lbook (dict): Learning book
    book_path: The path to the word book file
    """
    exittool = False  # continue
    if command == 'S':
        save_lbook(lbook, book_path)
    elif command == 'Q':
        save_lbook(lbook, book_path)
        exittool = True  # exit program
    elif command == 'L':
        for w in lset:
            print(
                f"{w['id']} {w['word']} - {w['score']}"
                f"/{w['total_fail']}/{w['total_pass']+w['total_fail']}")
    elif command == 'W' and config['debug'] == True:
        # Show learning window (debug mode only)
        for w in lwin:
            print(
                f"{w['id']} {w['word']} - {w['tmp_score']}/{w['score']}"
                f"/{w['total_pass']}/{w['total_fail']}")
    else:
        print("    *** what?")
    return exittool


def study(lbook, lset, lwin, book_path):
    """
    Study main loop

    Parameters
    command (str): A command character
    lset (dict): Learning set
    lbook (dict): Learning book
    book_path: The path to the word book file
    """
    fill_lwin(lset, lwin)
    #idx = random.randrange(len(lwin))
    idx = 0
    while True:
        print("    *** S: save, L: show learning set, Q: save and quit")
        word = lwin[idx]
        inword = input(f"    {word['meaning']}? ").rstrip()
        if len(inword) == 1:  # command
            if command(inword, lset, lbook, book_path):
                return
            continue
        elif word['word'] == inword:
            print("    *** Correct.  Practice a little more.")
            repeat_word(word, 2)
            word['total_pass'] += 1
            word['tmp_score'] += 1
            track_progress['pass'] += 1
            if word['tmp_score'] >= config['repeat_count']:
                word['tmp_score'] = 0
                word['score'] += 1
                track_progress['memorized_count'] += 1
                print(
                    f"    *** You've memorized the word.  {track_progress['memorized_count']} word(s) memorized today.")
                lwin.pop(idx)
                fill_lwin(lset, lwin)
                if idx > 0:
                    idx -= 1  # ++++++++
        else:
            print(f"    *** Incorrect.  Let's practice " +
                  str(config['penalty_count']) + " times.")
            if word['tmp_score'] > 0:
                word['tmp_score'] -= 1
            word['total_fail'] += 1
            track_progress['fail'] += 1
            repeat_word(word, config['penalty_count'])
        print('---')
        idx += 1
        if idx >= len(lwin):
            idx = 0


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <wordfile>")
        sys.exit()
    print("    *** VocaBull - Help your vocabulary building ***")
    book_path = sys.argv[1]
    lbook = load_book(book_path)
    lset = create_lset(lbook)
    lwin = []
    study(lbook, lset, lwin, book_path)
