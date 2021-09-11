import nltk
import sys
import os
import math
import string

FILE_MATCHES = 2
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    d={}
    for (dirpath, dirnames, filenames) in os.walk(directory):
        for file in filenames:
            with open(os.path.join(dirpath,file), 'rb') as f:
                d[str(file[:-4])]=str(f.read()).replace('\\n', '\n')
    # print(d)
    return d


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    l=[]
    for w in nltk.word_tokenize(document):
        if (w.lower() not in string.punctuation) and (w.lower() not in nltk.corpus.stopwords.words("english")):
            l+=[w.lower()]
    return l


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    idfs={}
    for doc in documents:
        # print(documents[doc])
        words=[]
        for word in documents[doc]:
            if word in words:
                continue
            words+=[word]
            if word in idfs:
                idfs[word]+=1
            else:
                idfs[word]=1
    # print(idfs["what"])
    for word in idfs:
        idfs[word]=math.log(len(documents)/idfs[word])
    return idfs


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    tf={}
    for file in files:
        tf[file]={}
        for word in files[file]:
            if word in query:
                if word in tf[file]:
                    tf[file][word]+=1
                else:
                    tf[file][word]=1
    d={}
    for file in tf:
        d[file]=0
        for word in tf[file]:
            d[file]+=tf[file][word]*idfs[word]
    # print(tf)
    # print(idfs["what"], idfs["neural"], idfs["network"])
    # print({k: v for k, v in sorted(d.items(), key=lambda item: item[1], reverse=True)})
    l=list(({k: v for k, v in sorted(d.items(), key=lambda item: item[1], reverse=True)}).keys())
    # print(l)
    return l[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    d={}
    for sentence in sentences:
        d[sentence]=0
        for word in query:
            if word in sentences[sentence]:
                # print(sentence, sentences[sentence])
                d[sentence]+=idfs[word]
    # print({k: v for k, v in sorted(d.items(), key=lambda item: item[1], reverse=True)})
    l=list({k: v for k, v in sorted(d.items(), key=lambda item: item[1], reverse=True)}.keys())
    # print(l)
    # print(l[:n])
    for j in range(len(l)):
        oldScore=-1
        oldDensity=0
        for i in range(len(l)):
            # print(l[i], "score is", d[l[i]])
            newDensity=0
            for word in query:
                if word in sentences[l[i]]:
                    newDensity+=1.0
            newDensity/=len(sentences[l[i]])
            # print(newDensity)
            if d[l[i]]==oldScore and newDensity>oldDensity:
                t=l[i]
                l[i]=l[i-1]
                l[i-1]=t
            oldDensity=newDensity
            oldScore=d[l[i]]
    # print(l[:n])
    return l[:n]



if __name__ == "__main__":
    main()
