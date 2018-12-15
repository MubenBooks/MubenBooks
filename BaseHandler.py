# Base Handler
import tornado.web
import logging
import json

class BaseHandler(tornado.web.RequestHandler):
    """
        Base Handler
    """
    def row_to_obj(self, row, cur):
        """Convert a SQL row to an object supporting dict and attribute access"""
        obj = tornado.util.ObjectDict()
        for val, desc in zip(row, cur.description):
            obj[desc.name] = val
        return obj

    async def execute(self, stmt, *args):
        """Execute a SQL statement.
    
        Must be called with ''await self.execute(...)''
        """
        with (await self.application.db.cursor()) as cur:
            await cur.execute(stmt, args)

    async def query(self, stmt, *args):
        """Query for a list of results.
        
        Typical usage::

            results = await self.query(...)

        Od::
            
            for row in await self.query()
        """

        with (await self.application.db.cursor()) as cur:
            await cur.execute(stmt, args)
            return [self.row_to_obj(row, cur) for row in await cur.fetchall()]

    async def queryone(self, stmt, *args):
        """Query for exactly one result.
        
        Raises NoResultError if there are no results, or ValueError if
        there are more than on.
        """
        results = await self.query(stmt, *args)
        if len(results) == 0:
            raise NoResultError()
        elif len(results) > 1:
            raise ValueError("Expected 1 result, got %d" % len(results))
        return results[0]

    async def any_user_exists(self, *args):
        """Query for any user exists.
            
        Return True if there alreay exists one user, else return False
        """
        return bool(await self.query("SELECT * FROM users WHERE username=%s LIMIT 1", *args))


def ReturnCode(status, arg=None):
    data = {'code': status}

    if not arg:
        return json.dumps(data)

    data['msg'] = arg
    return json.dumps(data)

