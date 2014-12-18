# -*- coding: utf-8 -*-
from .. import models
from .generic import Manager


class NotesManager(Manager):

    def get_by_id(self, note_id):
        """
        Finds and returns note based on its id.
        """
        for obj in self.state['Notes']:
            if obj['id'] == note_id or obj.temp_id == str(note_id):
                return obj
        return None

    def add(self, item_id, content, **kwargs):
        """
        Adds a note to the local state, and appends the equivalent request to
        the queue.
        """
        obj = models.Note({'item_id': item_id, 'content': content}, self.api)
        ts = self.api.generate_timestamp()
        obj.temp_id = obj['id'] = '$' + ts
        obj.data.update(kwargs)
        self.state['Notes'].append(obj)
        item = {
            'type': 'note_add',
            'temp_id': obj.temp_id,
            'timestamp': ts,
            'args': obj.data,
        }
        self.queue.append(item)
        return obj