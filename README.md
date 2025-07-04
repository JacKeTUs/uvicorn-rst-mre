# MRE for observing Unicorn closing connections prematurely

## Steps to reproduce:

1. Clone repo 
2. Install venv, install requirements from requirements.txt
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Launch app with `gunicorn -k uvicorn_worker.UvicornWorker mre-app:app --max-requests 1`.
Here we set `max-requests` as 1 for best reproducibility, it happens with any other number, and happens with Uvicorn and Hypercorn as well. Worker count is also irrelevant, happens with multiple workers as well. `timeout_graceful_shutdown` has no effect, it's by default set at 30s in Gunicorn. Worker loop setting (asyncio, uvloop) or http setting (h11, httptools) also doesn't matter.
4. Launch `mre.py`.


### Expected result:
MRE should last indefinitely without any errors. All sent requests should return valid response (http 200 in this case).

### Observed result:
MRE exits with exception `104: Connection reset by peer` after couple of seconds. In traffic dump ACK flag sent out by service after receiving HTTP request, and RST ACK flag is sent by service shortly after. Task is not processed, no valid response sent in this session.

```
$ time python3 ./mre.py
Traceback (most recent call last):
  File "mre.py", line 8, in <module>
    s.recv(255)
    ~~~~~~^^^^^
ConnectionResetError: [Errno 104] Connection reset by peer

real    0m3,089s
user    0m0,059s
sys     0m0,187s
```

