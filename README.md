# Rate Limiter
Implemented a decorator that limits the number of requests for the specific endpoint.

### How to use
1. Create a simple route function.
```python
@app.route('/some-route')
def some_route():
    return "Hello World"
```
2. Add a decorator `limit_rate_request` to the function.
```python
@limit_rate_request()
@app.route('/some-route')
def some_route():
    return "Hello World"
```
3. Specify rate_limit (by default is 100).
```python
@limit_rate_request(rate_limit=135)
@app.route('/some-route')
def some_route():
    return "Hello World"
```

### How to run a test application
1. Install docker to your machine 'https://www.docker.com/products/docker-desktop'.
2. Install docker-compose 'https://docs.docker.com/compose/install/'.
3. Run command `docker-compose up -d --build` to build image and run it.

**The app will run on 5000 port. There are two endpoints for testing.**
1. 'http://localhost:5000/' with 100 allowed requests per hour.
2. 'http://localhost:5000/second' with 50 allowed requests per hour.