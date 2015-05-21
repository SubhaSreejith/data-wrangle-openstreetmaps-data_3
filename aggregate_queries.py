Top 1 Contributing user
db.bangalore_india.osm.aggregate([{
        "$group":{
            "_id":"$created.user",
            "count":{
                "$sum":1
            }
        }
    },{"$sort":{"count":-1}},
    {"$limit":1}])['result']
[{u'_id': u'docaneesh', u'count': 113770}

2 data that have palya


pipeline = [
            {'$match': {Palya:{'$exists':1}}},
            {'$limit' : 5}
]
result  = db.bengaluru_india.osm.aggregate(pipeline)['result']
pprint.pprint(result)

[{u'_id': u''Mariyappana Palya ', u'count': 1},
{u'_id': u''Papareddy Palya ', u'count': 1}
]

3. Restaurant and what food they serve

pipeline = [
            {'$match': {'amenity':'restaurant',
                        'name':{'$exists':1}}},
            {'$project':{'_id':'$name',
                         'cuisine':'$cuisine',
                         'contact':'$phone'}}
]
result  = db.bengaluru_india.osm.aggregate(pipeline)['result']
pprint.pprint(result)

[{u'_id': u'Adigas'},
 {u'_id': u'Taste of Rampur'},
 {u'_id': u'Pizza Corner'},
 {u'_id': u'KFC'},
 {u'_id': u"McDonald's"},
 {u'_id': u"Tashan"},
 {u'_id': u'Konark', u'cuisine': u'american'}
 ]
