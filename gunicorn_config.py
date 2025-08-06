# Gunicorn configuration file for Obesity Prediction Application

# Server socket
bind = "0.0.0.0:5000"
backlog = 2048

# Worker processes
workers = 2
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# Restart workers after this many requests, to help prevent memory leaks
max_requests = 1000
max_requests_jitter = 50

# Logging
accesslog = "/opt/obesity-prediction/logs/access.log"
errorlog = "/opt/obesity-prediction/logs/error.log"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = "obesity-prediction"

# Server mechanics
daemon = False
pidfile = "/opt/obesity-prediction/gunicorn.pid"
user = "ec2-user"
group = "ec2-user"
tmp_upload_dir = None

# SSL (uncomment if using SSL)
# keyfile = "/path/to/keyfile"
# certfile = "/path/to/certfile"

# Server hooks
def on_starting(server):
    server.log.info("Starting Obesity Prediction Application")

def on_reload(server):
    server.log.info("Reloading Obesity Prediction Application")

def worker_int(worker):
    worker.log.info("worker received INT or QUIT signal")

def pre_fork(server, worker):
    server.log.info("Worker spawned (pid: %s)", worker.pid)

def post_fork(server, worker):
    server.log.info("Worker spawned (pid: %s)", worker.pid)

def post_worker_init(worker):
    worker.log.info("Worker initialized (pid: %s)", worker.pid)

def worker_abort(worker):
    worker.log.info("Worker aborted (pid: %s)", worker.pid) 