import logging
import json
from datetime import datetime, timezone
import os

class StructuredLogger:
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)

        handler.setFormatter(self.JsonFormatter())
        self.logger.addHandler(handler)

    class JsonFormatter(logging.Formatter):
        def format(self, record):
            log_entry = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "level": record.levelname,
                "message": record.getMessage(),
                "module": record.module,
            }
            if hasattr(record, "extra"):
                log_entry.update(record.extra)
            return json.dumps(log_entry)
        
    def info(self, message:str, **kwargs):
        self.logger.info(message, extra={"extra": kwargs})
    
    def warning(self, message:str, **kwargs):
        self.logger.warning(message, extra={"extra": kwargs})

    def error(self, message:str, **kwargs):
        self.logger.error(message, extra={"extra": kwargs})

logger = StructuredLogger("robinhood")
              