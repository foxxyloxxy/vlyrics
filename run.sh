#!/bin/bash

if [ ! -d "./songs" ]; then
  mkdir -p songs/text
  mkdir -p songs/html
fi

if [ ! -d "./.venv" ]; then
  python3 -m venv ./.venv
  ./.venv/bin/pip install -r requirements.txt
fi

./.venv/bin/python3 main.py