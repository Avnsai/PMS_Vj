#!/bin/bash

# Build script optimized for low memory environments (2GB RAM)
# This script builds the project with memory constraints

echo "🔧 Building with low-memory optimizations..."
echo "Available memory: $(free -h | awk '/^Mem:/ {print $7}')"

# Set Node.js memory limit to ~1.5GB (leaving room for OS)
export NODE_OPTIONS="--max-old-space-size=1536"

# Clear any existing build artifacts
echo "🧹 Cleaning previous build..."
rm -rf dist

# Run TypeScript compilation first (less memory intensive)
echo "📝 Compiling TypeScript..."
yarn tsc || { echo "❌ TypeScript compilation failed"; exit 1; }

# Run Vite build with memory limit
echo "📦 Building with Vite..."
yarn vite build || { echo "❌ Vite build failed"; exit 1; }

echo "✅ Build completed successfully!"
echo "Build size:"
du -sh dist
