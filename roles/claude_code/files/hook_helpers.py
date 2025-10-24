#!/usr/bin/env python3
"""
Claude Code Hook Helpers

This module provides reusable functions for creating custom Claude Code hooks.
These helpers make it easy to parse tool input and create consistent hook behavior.

Usage:
    Import this module in your custom hooks or use the helper functions inline.

Example:
    python3 -c "$(cat hook_helpers.py); check_command_pattern('git commit', 'Block commits', exit_code=2)"
"""

import json
import sys
import re
from typing import Optional, List


def get_tool_input() -> dict:
    """
    Read and parse tool input from stdin.

    Returns:
        dict: Parsed tool input data
    """
    try:
        return json.load(sys.stdin)
    except json.JSONDecodeError:
        return {}


def get_command(data: Optional[dict] = None) -> str:
    """
    Extract the command from tool input data.

    Args:
        data: Tool input data (if None, reads from stdin)

    Returns:
        str: The command being executed
    """
    if data is None:
        data = get_tool_input()
    return data.get('tool_input', {}).get('command', '')


def matches_pattern(command: str, pattern: str, exclude: Optional[str] = None) -> bool:
    """
    Check if command matches a regex pattern.

    Args:
        command: The command to check
        pattern: Regex pattern to match
        exclude: Optional string that should NOT be in the command

    Returns:
        bool: True if matches pattern and doesn't contain exclude string
    """
    matches = bool(re.search(pattern, command))
    if matches and exclude:
        return exclude not in command
    return matches


def contains_string(command: str, search: str, exclude: Optional[str] = None) -> bool:
    """
    Check if command contains a specific string.

    Args:
        command: The command to check
        search: String to search for
        exclude: Optional string that should NOT be in the command

    Returns:
        bool: True if contains search string and doesn't contain exclude string
    """
    contains = search in command
    if contains and exclude:
        return exclude not in command
    return contains


def print_message(message: str, stderr: bool = True) -> None:
    """
    Print a message to stderr or stdout.

    Args:
        message: The message to print
        stderr: If True, print to stderr; otherwise stdout
    """
    output = sys.stderr if stderr else sys.stdout
    output.write(message)
    if not message.endswith('\n'):
        output.write('\n')


def exit_hook(code: int = 0) -> None:
    """
    Exit the hook with a specific code.

    Args:
        code: Exit code (0=success, 1=error, 2=blocked)
    """
    sys.exit(code)


def check_command_pattern(
    pattern: str,
    message: str,
    exclude: Optional[str] = None,
    exit_code: int = 2,
    data: Optional[dict] = None
) -> None:
    """
    Complete hook: Check command against pattern and block/notify if matched.

    Args:
        pattern: Regex pattern to match against command
        message: Message to display if matched
        exclude: Optional string that should NOT be in command
        exit_code: Exit code if matched (0=notify, 2=block)
        data: Tool input data (if None, reads from stdin)
    """
    command = get_command(data)
    if matches_pattern(command, pattern, exclude):
        print_message(message)
        exit_hook(exit_code)
    exit_hook(0)


def check_command_contains(
    search: str,
    message: str,
    exclude: Optional[str] = None,
    exit_code: int = 2,
    data: Optional[dict] = None
) -> None:
    """
    Complete hook: Check if command contains string and block/notify if matched.

    Args:
        search: String to search for in command
        message: Message to display if found
        exclude: Optional string that should NOT be in command
        exit_code: Exit code if matched (0=notify, 2=block)
        data: Tool input data (if None, reads from stdin)
    """
    command = get_command(data)
    if contains_string(command, search, exclude):
        print_message(message)
        exit_hook(exit_code)
    exit_hook(0)


def check_multiple_patterns(
    patterns: List[tuple],
    data: Optional[dict] = None
) -> None:
    """
    Check multiple patterns in order and exit on first match.

    Args:
        patterns: List of tuples (pattern, message, exclude, exit_code)
        data: Tool input data (if None, reads from stdin)

    Example:
        check_multiple_patterns([
            (r'git commit.*-m', 'Use fabric', 'fabric', 2),
            (r'rm -rf /', 'Dangerous command', None, 2),
        ])
    """
    command = get_command(data)

    for item in patterns:
        pattern = item[0]
        message = item[1]
        exclude = item[2] if len(item) > 2 else None
        exit_code = item[3] if len(item) > 3 else 2

        if matches_pattern(command, pattern, exclude):
            print_message(message)
            exit_hook(exit_code)

    exit_hook(0)


if __name__ == '__main__':
    # Example usage when run directly
    print("Claude Code Hook Helpers")
    print("This module provides helper functions for creating hooks.")
    print("\nExample hook using helpers:")
    print("""
    python3 -c "
    import json, sys, re

    # Read command
    data = json.load(sys.stdin)
    cmd = data.get('tool_input', {}).get('command', '')

    # Check pattern
    if re.search(r'git commit.*-m', cmd) and 'fabric' not in cmd:
        sys.stderr.write('Use fabric for commits\\n')
        sys.exit(2)
    "
    """)
