import gc
import dask
from dask.distributed import Client, LocalCluster


def force_gc():
    gc.collect()

if __name__ == '__main__':
    # Adjust config settings programmatically
    dask.config.set({
        # Increase heartbeat timeout tolerance for heavy workloads
        "distributed.comm.timeouts.connect": "30s",
        "distributed.comm.timeouts.tcp": "60s",
        "distributed.deploy.lost-worker-timeout": "30s",
        
        # Increase unmanaged memory tolerance before pausing
        "distributed.worker.memory.target": 0.60,   # Target 60% memory usage
        "distributed.worker.memory.spill": 0.70,    # Spill to disk at 70%
        "distributed.worker.memory.pause": 0.85,    # Pause receiving tasks at 85%
        "distributed.worker.memory.terminate": 0.95  # Restart worker gracefully at 95%
    })

    # Automatically creates a local scheduler and workers based on your CPU cores
    cluster = LocalCluster(n_workers=4, threads_per_worker=2, memory_limit='4GB', processes=False)
    client = Client(cluster)

    print(f"Dashboard URL: {client.dashboard_link}")


    # Run garbage collection directly on all worker processes
    client.run(force_gc)