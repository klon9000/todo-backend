import os
import json

class Entry:
    def __init__(self, title, entries=None, parent=None):
        if entries == None:
            entries = []
        self.title = title
        self.entries = entries
        self.parent = parent

    def __str__(self):
        return self.title

    def add_entry(self, entry):
        self.entries.append(entry)
        entry.parent = self

    def print_entries(self, indent=0):
        print_with_indent(self.title, indent)
        indent += 1
        for entry in self.entries:
            entry.print_entries(indent)

    def json(self):
        entry_dict = {
            'title': self.title,
            'entries': [entry.json() for entry in self.entries]
        }
        return entry_dict

    @classmethod
    def from_json(cls, value):
        new_entry = cls(value['title'])
        for entry in value.get('entries', []):
            new_entry.add_entry(cls.from_json(entry))
        return new_entry

    def save(self, path):
        fname = os.path.join(path, f"{self.title}.json")
        with open(fname, 'w', encoding='utf-8') as f:
            json.dump(self.json(), f)

    @classmethod
    def load(cls, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return cls.from_json(json.load(f))


class EntryManager:
    def __init__(self, data_path):
        self.data_path = data_path
        self.entries = list()

    def save(self):
        for item in self.entries:
            item.save(self.data_path)

    def load(self):
        for filename in os.listdir(self.data_path):
            if filename.endswith('.json'):
                file = os.path.join(self.data_path, filename)
                entry = Entry.load(file)
                self.entries.append(entry)

    def add_entry(self, title: str):
        self.entries.append(Entry(title))

def print_with_indent(value, indent=0):
    prefix = '\t' * indent
    print(f"{prefix}{value}")