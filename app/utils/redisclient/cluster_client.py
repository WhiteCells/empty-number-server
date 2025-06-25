from redis.cluster import ClusterNode, RedisCluster
import threading

_redis_cluster_client: RedisCluster = None
_lock = threading.Lock()

def get_redis_cluster_client() -> RedisCluster:
    global _redis_cluster_client
    if _redis_cluster_client is None: # 避免不必要的加锁
        with _lock:
            if _redis_cluster_client is None:
                _redis_cluster_client = RedisCluster(
                    startup_nodes=[
                        ClusterNode(
                            host="localhost", port=7000
                        ),
                        ClusterNode(
                            host="localhost", port=7001
                        ),
                        ClusterNode(
                            host="localhost", port=7002
                        ),
                        ClusterNode(
                            host="localhost", port=7003
                        ),
                        ClusterNode(
                            host="localhost", port=7004
                        ),
                        ClusterNode(
                            host="localhost", port=7005
                        ),
                    ],
                    password="10101",
                    decode_responses=True,
                )
    return _redis_cluster_client


if __name__ == "__main__":
    redis_cluster_client = get_redis_cluster_client()
    redis_cluster_client.set("key", "value")
    print(redis_cluster_client.get("key"))
