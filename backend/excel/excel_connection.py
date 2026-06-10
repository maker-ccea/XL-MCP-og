# Import xlwings library for Microsoft Excel automation
import xlwings as xw
# Import Optional type hint from typing module
from typing import Optional
# Import python standard logging to log connection events
import logging

# Set up logging configuration for console output
logger = logging.getLogger("excel_connection")
logging.basicConfig(level=logging.INFO)

class ExcelConnectionManager:
    """
    A singleton connection manager class to handle startup, shutdown,
    and state tracking of the Microsoft Excel desktop application.
    """
    # Class-level private variable to hold the single instance of the manager
    _instance: Optional["ExcelConnectionManager"] = None
    # Private variable to store the xlwings App object
    _app: Optional[xw.App] = None

    def __new__(cls) -> "ExcelConnectionManager":
        # Check if an instance of this class already exists
        if cls._instance is None:
            # If not, create the instance using superclass constructor
            cls._instance = super(ExcelConnectionManager, cls).__new__(cls)
        # Return the singleton instance
        return cls._instance

    def connect_excel(self) -> xw.App:
        """
        Connects to a running Excel instance or launches a new one.
        Returns the xlwings App object.
        """
        # If we already have a reference to an app, let's verify if it's still alive
        if self._app is not None:
            try:
                # Try accessing app properties to check if connection is active
                _ = self._app.pid
                logger.debug("Reusing existing connection to Microsoft Excel.")
                # Return the cached app instance
                return self._app
            except Exception:
                # If an exception is raised, the connection has gone stale
                logger.warning("Cached Excel connection was lost. Cleaning up.")
                # Clear the reference so we can establish a new one
                self._app = None

        # Check if there are already running xlwings App instances
        if len(xw.apps) > 0:
            try:
                # Reuse the first active app in the collection
                self._app = xw.apps[0]
                logger.info("Successfully connected to a running Microsoft Excel instance.")
                return self._app
            except Exception as e:
                # Log any failure when attempting to connect to the active app
                logger.error(f"Failed to bind to existing Excel app: {e}")

        # If no active app is found or could be bound, start a new Excel process
        logger.info("Starting a new Microsoft Excel instance.")
        # Create a new app instance; visible=True shows the window, add_book=False prevents creating a blank sheet on start
        self._app = xw.App(visible=True, add_book=False)
        # Return the newly created app reference
        return self._app

    def disconnect_excel(self) -> None:
        """
        Safely disconnects from Microsoft Excel, closing the app reference.
        """
        # Check if we have an active app reference
        if self._app is not None:
            try:
                # Attempt to quit/close the Excel application process
                self._app.quit()
                logger.info("Disconnected and closed Microsoft Excel instance.")
            except Exception as e:
                # Log any errors during disconnection/close
                logger.error(f"Error while quitting Excel: {e}")
            finally:
                # Set the app reference back to None
                self._app = None

    def is_excel_running(self) -> bool:
        """
        Checks if Microsoft Excel is currently running on the system.
        """
        # If we don't have a cached app reference
        if self._app is None:
            # Return True if the list of xlwings apps is not empty
            return len(xw.apps) > 0
        try:
            # Query the PID of the cached app to check if it's active
            _ = self._app.pid
            # If successful, Excel is active
            return True
        except Exception:
            # If we get an exception, the Excel process is not running or unreachable
            return False

    def get_excel_app(self) -> xw.App:
        """
        Exposes the active Excel App instance. Connects automatically if not running.
        """
        # Delegate to connect_excel to ensure we return a valid App instance
        return self.connect_excel()

# Export a single global instance of the connection manager
excel_conn = ExcelConnectionManager()
