import asyncio
import logging
import os
import platform
import shlex
import subprocess
import sys
from pathlib import Path
from subprocess import Popen
from typing import Optional

import psutil
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.timeouts import Timeouts
from webdriver_manager.chrome import ChromeDriverManager

from lib.configuration import Configuration
from lib.exception import POpenError, InvalidArgument, UnsupportedOS, NotInitialized, ClientError
from lib.driver import SpectronDriver
import lib.helper as helper

logger = logging.getLogger(__name__)


class Application:

    def __init__(self, app_path: str, chromedriver_version: str, config=None):
        """
        Creates a new instance of Application.

        :Args:
         - app_path : Path to the Electron application
         - chromedriver_version : Specify the exact chromedriver version. https://chromedriver.chromium.org/downloads
         - config : List of optional configurations for webdriver, chromedriver, and electron. Refer to Configuration class for details.
         """

        if config is None:
            config = {}

        config.update({'chromedriver_version': chromedriver_version})
        config.update({'app_path': app_path})
        self.config = Configuration(**config)

        self.os = platform.system()
        self._client: Optional[SpectronDriver] = None
        self.return_code = None
        self.app: Optional[Popen] = None
        self.running = False
        self.results = None

    @property
    def client(self) -> SpectronDriver:
        if self._client is None:
            msg = "Client not started yet."
            logger.error(msg)
            raise ClientError(msg)

        return self._client

    def start(self) -> None:
        """Start App and Client."""
        self.start_app()

        asyncio.run(self.start_client())

        wait_time = helper.to_seconds(self.config.wait_timeout)
        self.client.update_wait(wait_time)

        self.running = True

    def stop(self) -> None:
        """Close App and Client using Webdriver (client) functions."""
        if not self.is_running():
            return

        if self.app.stdout:
            logger.info(f'Closing any log file.')
            self.app.stdout.close()
            self.app.stderr.close()

        self.switch_to_main_window()
        self.client.close()
        self.client.quit()
        self._cleanup()

    def terminate(self) -> None:
        """Close Electron process tree using OS-specific functions."""
        if not self.app:
            return

        timeout_seconds = to_seconds(self.config.stop_timeout)
        process = psutil.Process(self.app.pid)
        child_processes = process.children(recursive=True)

        try:
            def on_terminate(proc):
                logger.info(f"process {proc} terminated.")

            process.terminate()

            gone, alive = psutil.wait_procs(
                [process] + child_processes,
                timeout=timeout_seconds,
                callback=on_terminate
            )

            for p in alive:
                p.kill()

        except psutil.NoSuchProcess as e:
            logger.warning(f"Process [{process}] already closed.")
            logger.warning(e, exc_info=True)

        self._cleanup()

    def restart(self) -> None:
        self.stop()
        self.start()

    async def start_client(self) -> WebDriver:
        if self.is_running():
            return self.client

        # Options
        client_options = self._build_chrome_options()

        # Service
        chrome_service = self._build_chrome_service()

        # Chromedriver has an unconfigurable default timeout of 60 seconds.
        # We add a configurable timeout to it via asyncio.
        def start_webdriver(wb_args):
            return SpectronDriver(wb_args)

        webdriver_args = self.config.webdriver_options
        kwargs = {
                     'options': client_options,
                     'service': chrome_service
                 } | webdriver_args

        timeout_seconds = helper.to_seconds(self.config.start_timeout)
        try:
            self._client: WebDriver = await asyncio.wait_for(
                asyncio.to_thread(start_webdriver, kwargs),
                timeout=timeout_seconds
            )
        except asyncio.TimeoutError:
            logger.error(f"Took longer than {timeout_seconds} seconds to start.")
            raise
        finally:
            logger.info("WebDriver started.")
            logger.info(f"Application Electron version: {self._electron_version()}")

        return self.client

    def start_app(self) -> Popen:
        """Open Electron app."""
        if self.is_running():
            return self.app

        if self.os == "Darwin":
            cmd = shlex.split(f'{self.config.app_path} --args')
        elif self.os == "Windows":
            raise NotImplementedError
        elif self.os == "Linux":
            raise NotImplementedError
        else:
            raise UnsupportedOS(f"Unsupported OS - {self.os}")

        if type(self.config.electron_args) is not list:
            raise InvalidArgument("Electron_args is not a list")

        debugger_arg = f'--remote-debugging-port={self.config.app_port}'
        args = self.config.electron_args.copy() + [debugger_arg]

        if self.config.electron_log_path:
            file_name = self.config.electron_log_path
            stdout = open(file_name, "w")
            stderr = subprocess.STDOUT
        else:
            stdout = subprocess.DEVNULL
            stderr = subprocess.STDOUT

        kwargs = {
            'stdout': stdout,
            'stderr': stderr,
            'universal_newlines': True,
            'cwd': self.config.working_directory
        }

        try:
            logger.info(f'Running command: {cmd + args}')
            self.app = Popen(cmd + args, **kwargs)
            self.return_code = self.app.returncode
        except OSError as e:
            logger.exception(f"Error opening App! {e}")
            raise POpenError

        logger.info("Application started.")

        return self.app

    def wait_until_window_loaded(self):
        raise NotImplementedError

    def is_running(self) -> bool:
        return self.running

    def get_settings(self) -> Configuration:
        return self.config

    def switch_to_main_window(self) -> None:
        self.client.switch_to.window(self.client.window_handles[0])

    def take_screenshot(self, filename=None, folder=None) -> None:
        if self.is_running() is False:
            return

        file_path = []

        if folder:
            file_path.append(folder)

        if filename is None:
            filename = 'screenshot.png'

        file_path.append(filename)

        logger.info(f'Saving screenshot to "{"/".join(file_path)}"')
        self.client.save_screenshot("/".join(file_path))

    # private

    def _chrome_version(self) -> str:
        if not self.client:
            raise NotInitialized("Client not initialized yet")

        return self.client.capabilities['browserVersion']

    def _debugger_address(self) -> str:
        return f"localhost:{self.config.app_port}"

    def _cleanup(self) -> None:
        self.running = False
        self.app = None
        self._client = None

    def _electron_version(self) -> str:
        return self.client.execute_script("return process.versions.electron;")

    def _build_chrome_service(self) -> ChromeService:
        if self.config.chromedriver_path:
            self.config.chromedriver_path = os.path.join(Path.cwd(), self.config.chromedriver_path)
        else:
            version = self.config.chromedriver_version
            self.config.chromedriver_path = ChromeDriverManager(
                version,
                cache_valid_range=self.config.chromedriver_cache
            ).install()

        args = []
        if self.config.chromedriver_verbose:
            args.append('--verbose')

        return ChromeService(
            self.config.chromedriver_path,
            log_path=self.config.chromedriver_log_path,
            service_args=args
        )

    def _build_chrome_options(self) -> Options:
        options = Options()
        options.debugger_address = self._debugger_address()
        args = self.config.chrome_driver_args

        while args:
            options.add_argument(args.pop())

        return options
