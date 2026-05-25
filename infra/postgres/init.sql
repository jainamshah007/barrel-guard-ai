-- BARREL-GUARD AI Database Init
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_detections_camera
  ON detections(camera_id);
CREATE INDEX IF NOT EXISTS idx_detections_created
  ON detections(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_detections_class
  ON detections(object_class);
CREATE INDEX IF NOT EXISTS idx_detections_acked
  ON detections(acknowledged);
