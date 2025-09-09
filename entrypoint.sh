#!/bin/bash
echo "Waiting for database to be ready..."
sleep 10
echo "Starting Flask application..."
python -m muler.app
