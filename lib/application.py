# application.py

import asyncio
import atexit
import logging
import os
import platform
import shlex
import signal
import subprocess
import threading
from pathlib import Path
from subprocess import Popen
from typing import Optional

import psutil
from selenium.common import JavascriptException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

import lib.globals
import lib.helper as helper
from lib.configuration import Configuration
from lib.driver import SpectronDriver
from lib.exception import POpenError, InvalidArgument, UnsupportedOS, NotInitialized, ClientError

logger = logging.getLogger(__name__)


class Application:

    def __init__(self, app_path: str, chromedriver_version: str, config=None):
        """
        Creates a new instance of Application.

        :Args:
         - app_path : Path to the Electron application.
         - chromedriver_version : Specify the exact chromedriver version. https://chromedriver.chromium.org/downloads
         - config : List of optional configurations for webdriver, chromedriver, and electron. Refer to Configuration class for details.
         """
        if config is None:
            config = {}

        config.update({'chromedriver_version': chromedriver_version})
        config.update({'app_path': app_path})
        self.config = Configuration(**config)

        self.os = platform.system()
        self.return_code = None
        self.running = False
        self.results = None
        self._client: Optional[SpectronDriver] = None
        self._app: Optional[Popen] = None
        self._thread_wait: threading.Event = None

    @property
    def client(self) -> SpectronDriver:
        if self._client is None:
            msg = "Client not started yet."
            logger.error(msg)
            raise ClientError(msg)

        return self._client

    def start(self) -> None:
        """Start App and Client."""
        lib.globals.initialize()
        self.start_app()

        lib.globals.driver = asyncio.run(self.start_client())

        wait_time = helper.to_seconds(self.config.wait_timeout)
        self.client.update_wait(wait_time)

        self._register_close_events()
        self.running = True

    def stop(self) -> None:
        """Close App and Client."""
        if not self.is_running():
            return

        if self._app.stdout:
            logger.info(f'Closed log file.')
            self._app.stdout.close()

        self.switch_to_main_window()
        self.client.close()
        self.client.quit()

        self.terminate()

        logger.info("Application closed.")
        self._cleanup()

    def terminate(self) -> None:
        """Close Electron process tree using OS-specific functions."""
        if not self._app:
            return

        timeout_seconds = helper.to_seconds(self.config.stop_timeout)
        process = psutil.Process(self._app.pid)
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

        logger.info("WebDriver started.")
        logger.info(f"Application Electron version: {self._electron_version()}")

        return self.client

    def start_app(self) -> Popen:
        """Open Electron app."""
        if self.is_running():
            return self._app

        if self.os == "Darwin":
            cmd = shlex.split(f'{self.config.app_path}')
        elif self.os == "Windows":
            raise NotImplementedError
        elif self.os == "Linux":
            raise NotImplementedError
        else:
            raise UnsupportedOS(f"Unsupported OS - {self.os}")

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
            self._app = Popen(cmd + args, **kwargs)
            self.return_code = self._app.returncode
        except OSError as e:
            logger.exception(f"Error opening App! {e}")
            raise POpenError

        logger.info("Application started.")

        return self._app

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

    def devtools_url(self) -> str:
        return f"http://{self._debugger_address()}"

    def pause(self, timeout=None) -> None:
        if timeout is None:
            timeout = self.config.debug_timeout

        timeout = helper.to_seconds(timeout)

        signal.signal(signal.SIGINT, self.unpause)

        logger.info('Pause initiated.')
        print(f'Enter Ctrl+C to continue (timeout of {timeout} seconds):')

        self._thread_wait = threading.Event()
        self._thread_wait.wait(timeout=timeout)

    def unpause(self) -> None:
        logger.info('Pause cancelled.')
        if self._thread_wait:
            self._thread_wait.set()

    def default_selector(self, by: By) -> None:
        """Sets the default selector for all(), first(), element() finders"""
        lib.globals.default_selector = by

    def start_debug_mode(self, timeout=None) -> None:
        logger.info("Starting debugger mode.")
        msg = f"Devtools URL: {self.devtools_url()}"
        logger.info(msg)
        print(msg)
        self.pause(timeout)

    # private

    def _chrome_version(self) -> str:
        if not self.client:
            raise NotInitialized("Client not initialized yet")

        return self.client.capabilities['browserVersion']

    def _debugger_address(self) -> str:
        return f"localhost:{self.config.app_port}"

    def _cleanup(self) -> None:
        self.running = False
        self._app = None
        self._client = None

    def _electron_version(self) -> str:
        try:
            return self.client.execute_script("return process.versions.electron;")
        except JavascriptException as e:
            logger.warning(e.msg)
            return "Not available"

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

    def _register_close_events(self):
        atexit.register(self.stop)
