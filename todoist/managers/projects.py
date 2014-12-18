# -*- coding: utf-8 -*-
from .. import models
from .generic import Manager


class ProjectsManager(Manager):

    def all(self):
        return self.state['Projects']

    def get_by_id(self, project_id):
        """
        Finds and returns project based on its id.
        """
        for obj in self.state['Projects']:
            if obj['id'] == project_id or obj.temp_id == str(project_id):
                return obj
        return None

    def get_by_name(self, name):
        """
        Finds and returns project based on its name.
        """
        for obj in self.state['Projects']:
            if obj['name'] == name:
                return obj
        return None

    def add(self, name, **kwargs):
        """
        Adds a project to the local state, and appends the equivalent request
        to the queue.
        """
        obj = models.Project({'name': name}, self.api)
        ts = self.api.generate_timestamp()
        obj.temp_id = obj['id'] = '$' + ts
        obj.data.update(kwargs)
        self.state['Projects'].append(obj)
        item = {
            'type': 'project_add',
            'temp_id': obj.temp_id,
            'timestamp': ts,
            'args': obj.data,
        }
        self.queue.append(item)
        return obj

    def update_orders_indents(self, ids_to_orders_indents):
        """
        Updates in the local state the orders and indents of multiple projects,
        and appends the equivalent request to the queue.
        """
        for project_id in ids_to_orders_indents.keys():
            obj = self.get_by_id(project_id)
            if obj:
                obj['item_order'] = ids_to_orders_indents[project_id][0]
                obj['indent'] = ids_to_orders_indents[project_id][1]
        item = {
            'type': 'project_update_orders_indents',
            'timestamp': self.api.generate_timestamp(),
            'args': {
                'ids_to_orders_indents': ids_to_orders_indents,
            },
        }
        self.queue.append(item)