#!/bin/bash
# Smart Parking System — Folder Structure Scaffolding
ROOT="/home/snake/Projects/Smart Parking System"

# ===== Python Services =====
for svc in detection-service slot-service anpr-service dynamic-slot-service crash-detection-service; do
  mkdir -p "$ROOT/services/$svc/src/utils"
  mkdir -p "$ROOT/services/$svc/tests"
  touch "$ROOT/services/$svc/src/__init__.py"
  touch "$ROOT/services/$svc/src/main.py"
  touch "$ROOT/services/$svc/src/config.py"
  touch "$ROOT/services/$svc/src/consumer.py"
  touch "$ROOT/services/$svc/src/publisher.py"
  touch "$ROOT/services/$svc/src/utils/__init__.py"
  touch "$ROOT/services/$svc/tests/__init__.py"
  touch "$ROOT/services/$svc/Dockerfile"
  touch "$ROOT/services/$svc/requirements.txt"
  touch "$ROOT/services/$svc/.env.example"
  touch "$ROOT/services/$svc/README.md"
done

# Detection service specific
touch "$ROOT/services/detection-service/src/detector.py"
touch "$ROOT/services/detection-service/src/tracker.py"
touch "$ROOT/services/detection-service/src/utils/bbox.py"
touch "$ROOT/services/detection-service/src/utils/preprocessing.py"

# Slot service specific
touch "$ROOT/services/slot-service/src/slot_manager.py"
touch "$ROOT/services/slot-service/src/iou.py"

# ANPR service specific
touch "$ROOT/services/anpr-service/src/plate_detector.py"
touch "$ROOT/services/anpr-service/src/ocr.py"
touch "$ROOT/services/anpr-service/src/preprocessor.py"

# Dynamic slot service specific
touch "$ROOT/services/dynamic-slot-service/src/gap_analyzer.py"
touch "$ROOT/services/dynamic-slot-service/src/classifier.py"

# Crash detection specific
touch "$ROOT/services/crash-detection-service/src/motion_analyzer.py"
touch "$ROOT/services/crash-detection-service/src/velocity_tracker.py"

# ===== Node.js Services =====
for svc in verification-service aggregator-service history-service api-gateway; do
  mkdir -p "$ROOT/services/$svc/src/config"
  mkdir -p "$ROOT/services/$svc/src/routes"
  mkdir -p "$ROOT/services/$svc/src/controllers"
  mkdir -p "$ROOT/services/$svc/src/services"
  mkdir -p "$ROOT/services/$svc/src/models"
  mkdir -p "$ROOT/services/$svc/src/messaging"
  mkdir -p "$ROOT/services/$svc/src/middleware"
  mkdir -p "$ROOT/services/$svc/src/utils"
  mkdir -p "$ROOT/services/$svc/tests"
  touch "$ROOT/services/$svc/src/index.js"
  touch "$ROOT/services/$svc/src/app.js"
  touch "$ROOT/services/$svc/src/config/index.js"
  touch "$ROOT/services/$svc/src/messaging/consumer.js"
  touch "$ROOT/services/$svc/src/messaging/publisher.js"
  touch "$ROOT/services/$svc/src/middleware/errorHandler.js"
  touch "$ROOT/services/$svc/src/utils/logger.js"
  touch "$ROOT/services/$svc/Dockerfile"
  touch "$ROOT/services/$svc/package.json"
  touch "$ROOT/services/$svc/.env.example"
  touch "$ROOT/services/$svc/README.md"
done

# Verification service specific
touch "$ROOT/services/verification-service/src/routes/vehicles.js"
touch "$ROOT/services/verification-service/src/controllers/vehicleController.js"
touch "$ROOT/services/verification-service/src/services/vehicleService.js"
touch "$ROOT/services/verification-service/src/models/Vehicle.js"

# History service specific
touch "$ROOT/services/history-service/src/routes/sessions.js"
touch "$ROOT/services/history-service/src/controllers/historyController.js"
touch "$ROOT/services/history-service/src/services/historyService.js"
touch "$ROOT/services/history-service/src/models/ParkingSession.js"
touch "$ROOT/services/history-service/src/models/Alert.js"

# Gateway specific
touch "$ROOT/services/api-gateway/src/middleware/auth.js"
touch "$ROOT/services/api-gateway/src/routes/proxy.js"

# ===== Frontend =====
mkdir -p "$ROOT/frontend/public"
mkdir -p "$ROOT/frontend/src/api"
mkdir -p "$ROOT/frontend/src/components/common"
mkdir -p "$ROOT/frontend/src/components/dashboard"
mkdir -p "$ROOT/frontend/src/components/parking"
mkdir -p "$ROOT/frontend/src/components/vehicles"
mkdir -p "$ROOT/frontend/src/pages"
mkdir -p "$ROOT/frontend/src/hooks"
mkdir -p "$ROOT/frontend/src/context"
mkdir -p "$ROOT/frontend/src/styles"
mkdir -p "$ROOT/frontend/src/utils"
touch "$ROOT/frontend/public/index.html"
touch "$ROOT/frontend/src/index.js"
touch "$ROOT/frontend/src/App.js"
touch "$ROOT/frontend/src/api/parkingApi.js"
touch "$ROOT/frontend/src/pages/AdminDashboard.jsx"
touch "$ROOT/frontend/src/pages/UserDashboard.jsx"
touch "$ROOT/frontend/src/pages/VehicleManagement.jsx"
touch "$ROOT/frontend/src/pages/History.jsx"
touch "$ROOT/frontend/src/hooks/useWebSocket.js"
touch "$ROOT/frontend/src/context/AuthContext.js"
touch "$ROOT/frontend/src/styles/global.css"
touch "$ROOT/frontend/src/styles/variables.css"
touch "$ROOT/frontend/src/utils/formatters.js"
touch "$ROOT/frontend/Dockerfile"
touch "$ROOT/frontend/package.json"
touch "$ROOT/frontend/README.md"

# ===== Shared Contracts =====
mkdir -p "$ROOT/shared/events"
mkdir -p "$ROOT/shared/constants"
touch "$ROOT/shared/events/vehicle.detected.v1.json"
touch "$ROOT/shared/events/slot.updated.v1.json"
touch "$ROOT/shared/events/plate.detected.v1.json"
touch "$ROOT/shared/events/vehicle.verified.v1.json"
touch "$ROOT/shared/events/dynamic.slot.detected.v1.json"
touch "$ROOT/shared/events/crash.detected.v1.json"
touch "$ROOT/shared/constants/event-names.js"
touch "$ROOT/shared/README.md"

# ===== Infrastructure =====
mkdir -p "$ROOT/infra/docker/rabbitmq"
mkdir -p "$ROOT/infra/docker/postgres"
mkdir -p "$ROOT/infra/docker/redis"
mkdir -p "$ROOT/infra/nginx"
mkdir -p "$ROOT/infra/scripts"
touch "$ROOT/infra/docker/rabbitmq/rabbitmq.conf"
touch "$ROOT/infra/docker/postgres/init.sql"
touch "$ROOT/infra/docker/redis/redis.conf"
touch "$ROOT/infra/nginx/nginx.conf"
touch "$ROOT/infra/scripts/seed-db.sh"
touch "$ROOT/infra/scripts/wait-for-it.sh"

# ===== Docs =====
mkdir -p "$ROOT/docs/diagrams"
mkdir -p "$ROOT/docs/api"
mkdir -p "$ROOT/docs/meeting-notes"
# Move existing report files
if [ -d "$ROOT/Docs" ]; then
  cp "$ROOT/Docs"/*.tex "$ROOT/docs/" 2>/dev/null
  cp "$ROOT/Docs"/*.pdf "$ROOT/docs/" 2>/dev/null
fi
touch "$ROOT/docs/api/openapi.yaml"

# ===== Models =====
mkdir -p "$ROOT/models"
touch "$ROOT/models/README.md"

# ===== Root files =====
touch "$ROOT/docker-compose.yml"
touch "$ROOT/docker-compose.dev.yml"
touch "$ROOT/.env.example"
touch "$ROOT/Makefile"

echo "✅ Folder structure created successfully!"
