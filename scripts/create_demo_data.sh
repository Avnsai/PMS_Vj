#!/bin/bash

# Enhanced Demo Data Creation Script for Enterprise Portfolio Management

echo "🚀 Creating enhanced demo data for Enterprise Portfolio Management System..."

# Navigate to backend directory
cd /app/backend

# Run the demo data creation script
python3 run_demo_data.py

# Check if the script was successful
if [ $? -eq 0 ]; then
    echo "✅ Enhanced demo data created successfully!"
    echo "🌐 You can now access the system at: https://typescript-fix-8.preview.emergentagent.com"
    echo "🔑 Login credentials: demo@company.com / demo123456"
    echo "📊 The analytics dashboard now has meaningful data for visualization!"
else
    echo "❌ Failed to create demo data"
    exit 1
fi