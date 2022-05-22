#!/usr/bin/env python3

"""A times table quiz"""

import argparse
from datetime import datetime
import getpass
from random import randrange
import signal
import subprocess
import typing


SPEAK = True
VOICE = "m3"


class _AbortedError(Exception):
    pass


def _interrupt_handler(signum, frame):
    raise _AbortedError()


def _question_as_written(question: str) -> str:
    return question.replace("times", "x").replace("equals", "=")


def _display(message: str, newline=True) -> None:
    if newline:
        print(message, flush=True)
    else:
        print(message, flush=True, end="")


def _speak(message: str, display: bool = True,
           alt_message: typing.Optional[str] = None) -> None:
    if display:
        _display(alt_message or message)
    if SPEAK:
        subprocess.check_call(["espeak-ng", "-v", VOICE, message])


def _ask(message: str, alt_message: typing.Optional[str] = None) -> str:
    _display(alt_message or message, newline=False)
    if SPEAK:
        subprocess.check_call(["espeak-ng", "-v", VOICE, message])
    return input("")


def _speak_times_table(number: int) -> None:
    default__interrupt_handler = signal.signal(
        signal.SIGINT,
        _interrupt_handler
    )
    try:
        for i in range(1, 13):
            question = f"{i} times {number} equals {i * number}"
            _speak(question, alt_message=_question_as_written(question))
    except _AbortedError:
        pass
    finally:
        signal.signal(signal.SIGINT, default__interrupt_handler)


def _quiz_times_table(number: int) -> None:
    default__interrupt_handler = signal.signal(
        signal.SIGINT,
        _interrupt_handler
    )
    try:
        start = datetime.now()
        for i in range(1, 13):
            question = f"{i} times {number} equals "
            the_answer = str(i * number)
            while True:
                answer = _ask(
                    question,
                    alt_message=_question_as_written(question)
                )
                if answer == the_answer:
                    _speak(f"{the_answer}. Correct", alt_message="Correct")
                    break
                _speak(f"Sorry, {answer} is not correct, please try again")
        end = datetime.now()
        elapsed = round((end - start).total_seconds(), 1)
        _speak(f"Well done! 12 questions answered in {elapsed} seconds")
    except _AbortedError:
        pass
    finally:
        signal.signal(signal.SIGINT, default__interrupt_handler)


def _quiz_random_times_table(count: int) -> None:
    default__interrupt_handler = signal.signal(
        signal.SIGINT,
        _interrupt_handler
    )
    try:
        start = datetime.now()
        for _ in range(count):
            left = randrange(1, 12)
            right = randrange(1, 12)
            the_answer = str(left * right)
            question = f"{left} times {right} equals "
            while True:
                answer = _ask(
                    question,
                    alt_message=_question_as_written(question)
                )
                if answer == the_answer:
                    _speak(f"{the_answer}. Correct", alt_message="Correct")
                    break
                _speak(f"Sorry, {answer} is not correct, please try again")
        end = datetime.now()
        elapsed = round((end - start).total_seconds(), 1)
        _speak(f"Well done! {count} questions answered in {elapsed} seconds")
    except _AbortedError:
        pass
    finally:
        signal.signal(signal.SIGINT, default__interrupt_handler)


def _main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v",
        "--voice",
        choices=["male", "female"],
        default="male"
    )
    args = parser.parse_args()
    global VOICE
    if args.voice == "male":
        VOICE = "m3"
    else:
        VOICE = "f3"

    username = getpass.getuser()
    _speak(f"Hello {username}.")
    while True:
        _display(" 1. Listen to a times table")
        _display(" 2. A simple quiz")
        _display(" 3. A random quiz")
        _display(" 4. Finish")
        choice = _ask("Which number would you like to play? ")
        if choice in ["1", "2", "3", "4"]:
            if "1" == choice:
                table = _ask(
                    "Which times table?",
                    alt_message="Which times table? [1-12] "
                )
                if table in [str(i) for i in range(1, 13)]:
                    _speak_times_table(int(table))
                else:
                    _speak("Sorry, but you must choose a number from 1 to 12")
            elif "2" == choice:
                table = _ask(
                    "Which times table?",
                    alt_message="Which times table? [1-12] "
                )
                if table in [str(i) for i in range(1, 13)]:
                    _quiz_times_table(int(table))
                else:
                    _speak("Sorry, but you must choose a number from 1 to 12")
            elif "3" == choice:
                count = _ask("How many questions would you like? ")
                _quiz_random_times_table(int(count))
            elif "4" == choice:
                _speak("Thank you for playing. Goodbye.")
                return
        else:
            _speak("Sorry, but you must choose a number from 1 to 3")
        _display("")


if __name__ == "__main__":
    _main()
