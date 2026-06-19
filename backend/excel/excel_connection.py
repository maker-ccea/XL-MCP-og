
import xlwings as xw

from typing import Optional

import logging


logger = logging.getLogger("excel_connection")
logging.basicConfig(level=logging.INFO)

class ExcelConnectionManager:
    """
    A singleton connection manager class to handle startup, shutdown,
    and state tracking of the Microsoft Excel desktop application.
    """

    _instance: Optional["ExcelConnectionManager"] = None

    _app: Optional[xw.App] = None

    def __new__(cls) -> "ExcelConnectionManager":

        if cls._instance is None:

            cls._instance = super(ExcelConnectionManager, cls).__new__(cls)

        return cls._instance

    def connect_excel(self) -> xw.App:
        """
        Connects to a running Excel instance or launches a new one.
        Returns the xlwings App object.
        """

        if self._app is not None:
            try:

                _ = self._app.pid
                logger.debug("Reusing existing connection to Microsoft Excel.")

                return self._app
            except Exception:

                logger.warning("Cached Excel connection was lost. Cleaning up.")

                self._app = None


        if len(xw.apps) > 0:
            try:

                self._app = xw.apps[0]
                logger.info("Successfully connected to a running Microsoft Excel instance.")
                return self._app
            except Exception as e:

                logger.error(f"Failed to bind to existing Excel app: {e}")


        logger.info("Starting a new Microsoft Excel instance.")

        self._app = xw.App(visible=True, add_book=False)

        return self._app

    def disconnect_excel(self) -> None:
        """
        Safely disconnects from Microsoft Excel, closing the app reference.
        """

        if self._app is not None:
            try:

                self._app.quit()
                logger.info("Disconnected and closed Microsoft Excel instance.")
            except Exception as e:

                logger.error(f"Error while quitting Excel: {e}")
            finally:

                self._app = None

    def is_excel_running(self) -> bool:
        """
        Checks if Microsoft Excel is currently running on the system.
        """

        if self._app is None:

            return len(xw.apps) > 0
        try:

            _ = self._app.pid

            return True
        except Exception:

            return False

    def get_excel_app(self) -> xw.App:
        """
        Exposes the active Excel App instance. Connects automatically if not running.
        """

        return self.connect_excel()


excel_conn = ExcelConnectionManager()