#!/bin/bash

echo [TIMING `date +"%F %R:%S"`] Starting celery workers
celery --app="app_dir.celery_app.app" worker --concurrency="${APP_WORKER_COUNT:-4}" -n "celery@$(hostname).${AMAZON_CURRENT_AZ}" &
