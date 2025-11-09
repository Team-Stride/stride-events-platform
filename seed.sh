#!/bin/bash
# Seed database with test data

echo "🌱 Seeding database..."

cd backend
python3.11 -m app.scripts.seed_data

echo "✅ Seeding complete!"
