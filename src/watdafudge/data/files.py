from . import DocsLoader as Base

class DocsDirLoader(Base):

    @classmethod
    def Default(cls, src_dir='.', fname_pat=r'.+\.txt', encoding='utf-8'):
        return cls(src_dir, fname_pat, encoding)

    def __init__(self, src_dir, fname_pat, encoding):
        self.src_dir = src_dir
        self.fname_pat = fname_pat
        self.encoding = encoding

    def __iter__(self):
        from os import path, listdir
        from io import open

        if self.fname_pat:
            from re import compile
            fname_match = compile(self.fname_pat).match
        else:
            fname_match = lambda f: f
        
        src_dir = path.abspath(self.src_dir)
        
        enc = self.encoding

        for fname in listdir(src_dir):
            m = fname_match(fname)
            if not m:
                continue

            fpath = path.join(src_dir, fname)
            with open(fpath, encoding=enc) as f:
                yield {
                    'name': fname,
                    'dir': src_dir,
                    'text': f.read()
                }


class DocsFileLoader(Base):

    @classmethod
    def Default(cls, src_path, encoding='utf-8'):
        return cls(src_path, encoding)

    def __init__(self, src_path, encoding):
        self.src_path = src_path
        self.encoding = encoding

    def __iter__(self):
        from os import path
        from io import open

        src_path = path.abspath(self.src_path)

        with open(src_path, encoding=self.encoding) as f:
            yield {
                'name': path.basename(src_path),
                'dir': path.dirname(src_path),
                'text': f.read()
            }


class PhrasesDirLoader(Base):

    @classmethod
    def Default(cls, src_dir='.', fname_pat=r'.+\.txt', encoding='utf-8', sep=u'|', weight=1.0):
        return cls(src_dir, fname_pat, encoding, sep, weight)

    def __init__(self, src_dir, fname_pat, encoding, sep, weight):
        self.src_dir = src_dir
        self.fname_pat = fname_pat
        self.encoding = encoding
        self.sep = sep
        self.weight = weight

    def __iter__(self):
        from os import path, listdir
        from io import open
        
        if self.fname_pat:
            from re import compile
            fname_match = compile(self.fname_pat).match
        else:
            fname_match = lambda f: f
        
        src_dir = path.abspath(self.src_dir)
        
        enc = self.encoding
        sep = self.sep
        weight = self.weight

        for fname in listdir(src_dir):
            m = fname_match(fname)
            if not m:
                continue

            fpath = path.join(src_dir, fname)
            with open(fpath, encoding=enc) as f:
                for l in f:
                    cols = l.split(sep)
                    if len(cols) == 1:
                        name = cols[0].strip()
                        content = cols[0].strip()

                    elif len(cols >= 2):
                        name = cols[0].strip()
                        content = cols[1].strip()

                yield {
                    'name': name,
                    'content': content,
                    'weight': weight
                }


class PhrasesFileLoader(Base):

    @classmethod
    def Default(cls, src_path, encoding='utf-8', sep=u'|', weight=1.0):
        return cls(src_path, encoding, sep, weight)

    def __init__(self, src_path, encoding, sep, weight):
        self.src_path = src_path
        self.encoding = encoding
        self.sep = sep
        self.weight = weight

    def __iter__(self):
        from io import open
        
        sep = self.sep
        weight = self.weight

        with open(self.src_path, encoding=self.encoding) as f:
            for l in f:
                cols = l.split(sep)
                if len(cols) == 1:
                    name = cols[0].strip()
                    content = cols[0].strip()

                elif len(cols >= 2):
                    name = cols[0].strip()
                    content = cols[1].strip()

                yield {
                    'name': name,
                    'content': content,
                    'weight': weight
                }
