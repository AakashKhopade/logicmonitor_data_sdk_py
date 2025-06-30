Here is the updated code:

```
import logging
from typing import Dict, Any

import os
import psutil
import time

from logicmonitor_data_sdk import (
    Configuration,
    ResponseInterface,
    Resource,
    DataSource,
    DataPoint,
    DataSourceInstance,
)
from logicmonitor_data_sdk.api.metrics import Metrics

logging.basicConfig(level=logging.INFO)

configuration = Configuration(debug=False)

class MyResponse(ResponseInterface):
    def success_callback(self, request: Any, response: Any, status: int, request_id: str) -> None:
        logging.info("%s: %s: %s", response, status, request_id)

    def error_callback(self, request: Any, response: Any, status: int, request_id: str, reason: str) -> None:
        logging.error("%s: %s: %s %s", response, status, reason, request_id)


def metric_request(device_name: str = None) -> None:
    if not device_name:
        logger.warning("Device name is required")
        return

    resource = Resource(ids={"system.displayname": device_name}, name=device_name, create=True)
    datasource = DataSource(name="CPU")
    instance = DataSourceInstance(name='cpu-1')
    datapoint = DataPoint(name="cpu_utilization")

    metric_api = Metrics(batch=True, interval=10, response_callback=MyResponse())
    while True:
        values: Dict[str, str] = {str(int(time.time())): str(psutil.cpu_percent())}

        try:
            metric_api.send_metrics(
                resource=resource,
                datasource=datasource,
                instance=instance,
                datapoint=datapoint,
                values=values
            )
        except Exception as e:
            logger.error("Error sending metrics: %s", e)

        time.sleep(10)


if __name__ == "__main__":
    metric_request()
```