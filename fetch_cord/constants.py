"""Constants used throughout FetchCord."""

# Timing constants (in seconds)
MIN_CYCLE_TIME_SECONDS = 15
DEFAULT_CYCLE_TIME_SECONDS = 30
WAIT_INTERVAL_SECONDS = 0.05

# Git branches
DEFAULT_BRANCH = "master"
TESTING_BRANCH = "testing"

# Discord's limits on Rich Presence buttons.
MAX_BUTTONS = 2
MAX_BUTTON_LABEL = 32

# Error / status messages
RESULT_NOT_FOUND = "Not Found"
CUSTOM_TIME_MESSAGE = "setting custom time {time} seconds"

# RPC connection
RPC_CONNECTION_REFUSED_MSG = (
    "RPC connection refused (is Discord open?); trying again in 30 seconds"
)

# Systemd commands
VALID_SYSTEMD_COMMANDS = {"start", "stop", "enable", "disable", "status"}

# Service file URL
SERVICE_FILE_URL_TEMPLATE = (
    "https://raw.githubusercontent.com/fetchcord/FetchCord/"
    "{branch}/systemd/fetchcord.service"
)

# Resource files for update
RESOURCE_FILES = [
    "cpus.json",
    "gpus.json",
    "os.json",
    "terminal.json",
    "shell.json",
    "motherboards.json",
    "system_types.json",
]
