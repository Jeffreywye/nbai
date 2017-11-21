import datetime
from pymongo import MongoClient
from mongokit import Document
from database.connection import connection, DATABASE_NAME
from database.tables.fields import Fields as f
from database.tables.fields import Structure as s



def current_utctime():
    return unicode(datetime.datetime.utcnow())

@connection.register
class DatabaseRecord(Document):

    __database__ = DATABASE_NAME

    structure = {
        f.date_created : s.date_created,
        f.date_updated : s.date_updated,
    }

    required_fields = [
        f.date_created,
        f.date_updated,
    ]

    default_values = {
        f.date_created : current_utctime,
        f.date_updated : current_utctime,
    }

    ## Updates the 'date_updated' timestamp
    def save(self):
        return self.save_all([self])

    ## Updates the 'date_updated' timestamp
    def __update_timestamp(self):
        self[f.date_updated] = current_utctime()
        return

    ## Allows you to get fields directly,
    ## ex: Player.name instead of Player["name"]
    def __getattr__(self, field):
        if field in self.keys():
            return self[field]
        return Document.__getattr__(self, field)

    ## Allows you to set fields directly
    def __setattr__(self, field, value):
        if field in self.keys():
            self[field] = value
        Document.__setattr__(self, field, value)

    ## Returns a new Record with default values.
    ## Allows you to create a new record using
    ## FooRecord.new() instead of connection.FooRecord()
    @classmethod
    def new(cls, fields=None):
        instance = getattr(connection, cls.__name__)()
        if isinstance(fields, dict):
            for k, v in fields.items():
                instance[k] = v
        return instance

    ## Searches MongoDB for a specific Record.
    ## Returns None if not present,
    ## a Record if one exists,
    ## or throws an exception if more than one exist
    @classmethod
    def find_one(cls, query):
        not_an_instance = getattr(connection, cls.__name__)
        return not_an_instance.one(query)

    ## Searches MongoDB for a set of Records.
    ## Returns a Cursor object containing zero or more objects
    @classmethod
    def find_all(cls, query=None):
        if query is None:
            query = {}
        not_an_instance = getattr(connection, cls.__name__)
        return not_an_instance.find(query)

    ## Given a list of Records, saves all of them at once.
    ## This will also populate the objects with ObjectIds and updated timestamps
    @classmethod
    def save_all(cls, document_list, uuid=False, safe=True, *args, **kwargs):

        ## Returns a report
        def report(inserted, updated):
            return {"INSERTED" : inserted, "UPDATED" : updated}
        
        ## If there are no documents to save, exit.
        if not document_list:
            return report(0, 0)

        ## Otherwise, create lists of documents to insert and update
        insertable = []
        updatable = []

        ## For each document:
        for rec in document_list:

            ## Validate its type
            for doc in document_list:
                if not isinstance(rec, cls):
                    raise ValueError("save_all expected a {} but got a {}".format(cls, type(rec)))

            ## Validate its schema
            rec.validate(auto_migrate=False)
                
            ## If this is an old item, just update the original
            if '_id' in rec:
                updatable.append(rec)
                
            ## Otherwise, create a new one
            else:
                if uuid:
                    rec['_id'] = unicode("%s-%s" % (rec.__class__.__name__, uuid4()))
                insertable.append(rec)
                
            ## Additional function calls present in the save method
            rec._process_custom_type('bson', rec, rec.structure)
            rec._process_custom_type('python', rec, rec.structure)
        
        ## Create an object representing this table
        db = getattr(MongoClient(), DATABASE_NAME)
        table = getattr(db, cls.__collection__)
        
        ## Validate that the primary keys are still unique
        for primary_key in cls.indexes:
            
            ## If this key should be unique:
            if primary_key['unique']:
                
                ## Then for each unique field:
                for field in primary_key['fields']:
                    
                    ## Verify uniqueness among the records we're saving
                    if len(document_list) != len(set([getattr(doc, field) for doc in document_list])):
                        raise ValueError("Field {} should be unique".format(field))
                    
                    ## Make sure none of the new elements exist already
                    query = { field : { '$in' : [getattr(doc, field) for doc in insertable] } }
                    if table.find(query).count():
                        raise ValueError("Field {} should be unique".format(field))
        
        ## Update all the timestamps
        for doc in document_list:
            doc.__update_timestamp()

        ## Create a bulk operation to save everything at once
        bulk_op = table.initialize_ordered_bulk_op()
        for rec in insertable:
            bulk_op.insert(rec)
        for rec in updatable:
            bulk_op.find({'_id' : rec._id}).update({'$set' : rec})

        ## Save all the objects
        d = bulk_op.execute()
        return report(d['nInserted'], d['nModified'])

