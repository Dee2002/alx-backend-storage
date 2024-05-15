#!/usr/bin/env python3

from pymongo import MongoClient


def log_stats():
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs
    nginx_collection = db.nginx

    # Log stats
    log_count = nginx_collection.count_documents({})
    print(f"{log_count} logs")
    print("Methods:")
    for method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
        count = nginx_collection.count_documents({"method": method})
        print(f"\tmethod {method}: {count}")
    status_check = nginx_collection.count_documents(
        {"method": "GET", "path": "/status"})
    print(f"{status_check} status check")

    # Top 10 IPs
    print("IPs:")
    pipeline = [
        {
            "$group": {
                "_id": "$ip",
                "count": {"$sum": 1}
            }
        },
        {
            "$sort": {"count": -1}
        },
        {
            "$limit": 10
        }
    ]
    top_ips = nginx_collection.aggregate(pipeline)
    for ip in top_ips:
        print(f"\t{ip['_id']}: {ip['count']}")


if __name__ == "__main__":
    log_stats()