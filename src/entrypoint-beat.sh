#!/bin/bash
echo [TIMING `date +"%F %R:%S"`] Starting celery beat
celery --app="app_dir.celery_app.app" beat &
