## Planbox API Python Library

### About

This library acts as a synchronous wrapper for the Planbox api (http://www.planbox.com/api)
Endpoints are defined in the planbox/planbox.yaml file

### Usage

```python
    from planbox import PlanboxAPI
    api = PlanboxAPI()
    api.login(email='<your-email>',password='<your-password>')
    # call endpoints
    api.logout()
```

### License

This software is released under the MIT License, as detailed in the LICENSE file