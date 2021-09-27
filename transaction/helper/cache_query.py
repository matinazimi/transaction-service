from bson import ObjectId

from transaction.models import TransactionCache
from zibal.mongo_configue import db


def cache_insert_query():
    """
    This function use when save calculate data on new collection
    This collection have 2 type data :
        1)data when calculate for all user group by their mode (day/week/month)
        2)data when calculate per user whit (merchantId) group by their mode (day/week/month)
    """
    print('>>>>>>>>>>>>>>>>>>>>>>>> CACHE - START >>>>>>>>>>>>>>>>>>>>>>')
    db.transaction_transactioncache.remove({})
    day = [{'$group': {'_id': {'$dayOfYear': "$createdAt"},
                       'createdAt': {'$first': '$createdAt'},
                       'totalAmount': {'$sum': '$amount'},
                       'Count': {'$sum': 1}}},
           {"$sort": {"_id": 1}}
           ]

    week = [
        {
            '$group': {
                '_id': {'$week': '$createdAt'},
                'createdAt': {'$first': '$createdAt'},
                'totalAmount': {'$sum': '$amount'},
                'Count': {'$sum': 1},
            }
        },
        {"$sort": {"_id": 1}}
    ]

    month = [
        {
            '$group': {
                '_id': {'$month': '$createdAt'},
                'createdAt': {'$first': '$createdAt'},
                'totalAmount': {'$sum': '$amount'},
                'Count': {'$sum': 1},
            }
        },
        {"$sort": {"_id": 1}}
    ]
    result_day = db.transaction_transaction.aggregate(day)
    result_week = db.transaction_transaction.aggregate(week)
    result_month = db.transaction_transaction.aggregate(month)
    for result_d in result_day:
        TransactionCache.objects.create(mode='day', type='All',
                                        data={
                                            'createdAt': result_d.get('createdAt'),
                                            'totalAmount': result_d.get('totalAmount'),
                                            'Count': result_d.get('Count'),
                                        })
    for result_w in result_week:
        TransactionCache.objects.create(mode='week', type='All',
                                        data={
                                            'createdAt': result_w.get('createdAt'),
                                            'totalAmount': result_w.get('totalAmount'),
                                            'Count': result_w.get('Count'),
                                        })
    for result_m in result_month:
        TransactionCache.objects.create(mode='month', type='All',
                                        data={
                                            'createdAt': result_m.get('createdAt'),
                                            'totalAmount': result_m.get('totalAmount'),
                                            'Count': result_m.get('Count'),
                                        })

    merchantId = [{'$group': {'_id': '$merchantId'}}]
    users = db.transaction_transaction.aggregate(merchantId)
    for user in users:
        day = [{'$match': {'merchantId': ObjectId(user.get("_id"))}},
               {'$group': {'_id': {'$dayOfYear': "$createdAt"},
                           'createdAt': {'$first': '$createdAt'},
                           'totalAmount': {'$sum': '$amount'},
                           'Count': {'$sum': 1}}},
               {"$sort": {"_id": 1}}
               ]
        week = [{'$match': {'merchantId': ObjectId(user.get("_id"))}},
                {'$group': {'_id': {'$week': "$createdAt"},
                            'createdAt': {'$first': '$createdAt'},
                            'totalAmount': {'$sum': '$amount'},
                            'Count': {'$sum': 1}}},
                {"$sort": {"_id": 1}}
                ]
        month = [{'$match': {'merchantId': ObjectId(user.get("_id"))}},
                 {'$group': {'_id': {'$month': "$createdAt"},
                             'createdAt': {'$first': '$createdAt'},
                             'totalAmount': {'$sum': '$amount'},
                             'Count': {'$sum': 1}}},
                 {"$sort": {"_id": 1}}
                 ]
        result_day = db.transaction_transaction.aggregate(day)
        result_week = db.transaction_transaction.aggregate(week)
        result_month = db.transaction_transaction.aggregate(month)
        for i in result_day:
            TransactionCache.objects.create(mode='day', merchantId=str(ObjectId(str(user.get("_id")))),
                                            data={
                                                'createdAt': i.get('createdAt'),
                                                'totalAmount': i.get('totalAmount'),
                                                'Count': i.get('Count'),
                                            })
        for z in result_week:
            TransactionCache.objects.create(mode='week', merchantId=ObjectId(str(user.get("_id"))),
                                            data={
                                                'createdAt': z.get('createdAt'),
                                                'totalAmount': z.get('totalAmount'),
                                                'Count': z.get('Count'),
                                            })
        for j in result_month:
            TransactionCache.objects.create(mode='month', merchantId=ObjectId(str(user.get("_id"))),
                                            data={
                                                'createdAt': j.get('createdAt'),
                                                'totalAmount': j.get('totalAmount'),
                                                'Count': j.get('Count'),
                                            })
    print('>>>>>>>>>>>>>>>>>>>>>>>> CACHE - FINISH >>>>>>>>>>>>>>>>>>>>>>')
