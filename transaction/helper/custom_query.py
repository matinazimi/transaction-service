from bson import ObjectId

from zibal.mongo_configue import db


def custom_query(mode: str, merchantId: ObjectId = None) -> "mongo query object":
    """
    :param
        mode: day/week/month

    this api for Complicated query that ORM not support like group by on mongoDB
    we define custom pipe lines and base on mode use them
    """
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
    if mode == "week":
        Mode = week
    elif mode == "month":
        Mode = month
    else:
        Mode = day

    if merchantId:
        user = {'$match': {'merchantId': ObjectId(str(merchantId))}}
        Mode.insert(0, user)
    result = db.transaction_transaction.aggregate(Mode)

    return result
