import logging
import json
from datetime import datetime
from typing import Any, Dict
import uuid

class CustomFormatter(logging.Formatter):
    """Custom formatter that includes transaction ID and structured metadata."""
    
    def format(self, record: logging.LogRecord) -> str:
        # Add ISO format timestamp
        record.created_iso = datetime.fromtimestamp(record.created).isoformat()
        
        # Ensure transaction_id exists
        if not hasattr(record, 'transaction_id'):
            record.transaction_id = getattr(record, 'transaction_id', str(uuid.uuid4()))
            
        # Format metadata if it exists
        if hasattr(record, 'metadata') and record.metadata:
            metadata_str = ' | '.join(f"{k}: {v}" for k, v in record.metadata.items() if v is not None)
            record.message = f"{record.getMessage()} | {metadata_str}"
        else:
            record.message = record.getMessage()
            
        # Basic format
        log_entry = (
            f"{record.created_iso} - {record.name} - {record.levelname} - "
            f"[Transaction ID: {record.transaction_id}] {record.message}"
        )
        
        # Add exception info if present
        if record.exc_info:
            log_entry += f"\n{self.formatException(record.exc_info)}"
            
        return log_entry

def setup_logging():
    """Configure logging with custom formatter."""
    # Create custom formatter
    formatter = CustomFormatter()
    
    # Create console handler and set formatter
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    
    # Remove existing handlers and add our custom handler
    root_logger.handlers = []
    root_logger.addHandler(console_handler)

class CustomLogger(logging.Logger):
    """Custom logger with additional methods for structured logging."""
    
    def __init__(self, name: str):
        super().__init__(name)
        self.transaction_id = str(uuid.uuid4())
    
    def log_with_metadata(self, level: int, msg: str, metadata: Dict[str, Any] = None, **kwargs):
        """Log a message with associated metadata."""
        if metadata is None:
            metadata = {}
        
        # Create a new record
        record = logging.LogRecord(
            name=self.name,
            level=level,
            pathname='',
            lineno=0,
            msg=msg,
            args=(),
            exc_info=None
        )
        
        # Add metadata and transaction_id
        record.metadata = metadata
        record.transaction_id = self.transaction_id
        
        # Add any additional kwargs
        for key, value in kwargs.items():
            setattr(record, key, value)
        
        # Process the record
        self.handle(record)

# Register custom logger class
logging.setLoggerClass(CustomLogger) 