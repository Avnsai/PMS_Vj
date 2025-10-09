# Low Memory Build Guide (2GB RAM Server)

## Problem
Building a React + TypeScript + Vite project on a 2GB RAM server can cause out-of-memory errors and kill the build process.

## Solutions (Choose One)

---

### ✅ Option 1: Build with Optimized Configuration (Recommended)

The Vite config has been optimized to reduce memory usage. Use the custom build script:

```bash
cd /var/www/pms/frontend

# First, reinstall dependencies to fix rollup issue
rm -rf node_modules yarn.lock
yarn install

# Use the low-memory build script
./build-low-memory.sh
```

**Memory optimizations applied:**
- Disabled source maps (saves ~40% memory)
- Manual chunk splitting (reduces peak memory)
- Disabled compressed size reporting
- Uses esbuild minifier (faster, less memory)
- Node.js heap limited to 1.5GB

---

### ✅ Option 2: Enable Swap Space (Temporary Memory)

Add temporary swap space to handle memory spikes:

```bash
# Create 2GB swap file
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# Verify swap is active
free -h

# Now build
cd /var/www/pms/frontend
NODE_OPTIONS="--max-old-space-size=1536" yarn build

# Optional: Remove swap after build
sudo swapoff /swapfile
sudo rm /swapfile
```

---

### ✅ Option 3: Build Locally and Deploy (Best for Production)

Build on your local machine or CI/CD pipeline, then deploy only the `dist` folder:

**On your local machine:**
```bash
# Clone and build
git clone <your-repo>
cd frontend
yarn install
yarn build

# Create a tarball
tar -czf dist.tar.gz dist
```

**On your server:**
```bash
cd /var/www/pms/frontend
# Upload dist.tar.gz to server, then:
tar -xzf dist.tar.gz
```

---

### ✅ Option 4: Use GitHub Actions / CI/CD

Create `.github/workflows/build.yml`:

```yaml
name: Build Frontend

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          
      - name: Install dependencies
        run: cd frontend && yarn install
        
      - name: Build
        run: cd frontend && yarn build
        
      - name: Upload artifact
        uses: actions/upload-artifact@v3
        with:
          name: dist
          path: frontend/dist
```

Then download and deploy the artifact to your server.

---

### ✅ Option 5: Build in Docker Container

Create `Dockerfile.build`:

```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package.json yarn.lock ./
RUN yarn install --frozen-lockfile

COPY . .
RUN yarn build

# Output will be in /app/dist
```

Build:
```bash
docker build -f Dockerfile.build -t frontend-builder .
docker run -v $(pwd)/dist:/app/dist frontend-builder
```

---

## Monitoring During Build

Watch memory usage:
```bash
# In another terminal
watch -n 1 'free -h'
```

---

## Current Build Configuration

**Optimizations in `vite.config.ts`:**
- ❌ Source maps disabled
- ✅ Code splitting enabled
- ✅ Vendor chunks separated
- ✅ CSS code splitting
- ✅ esbuild minification

**Expected build time:** 30-60 seconds
**Expected memory peak:** ~1.3-1.5GB

---

## If Build Still Fails

1. **Check available memory:**
   ```bash
   free -h
   df -h
   ```

2. **Kill other processes:**
   ```bash
   # Stop unnecessary services temporarily
   sudo systemctl stop nginx  # if running
   sudo systemctl stop apache2  # if running
   ```

3. **Upgrade server:**
   - Consider upgrading to 4GB RAM for comfortable builds
   - Or use CI/CD for building (Option 3/4)

---

## Production Deployment

After successful build:

```bash
# Your dist folder is ready
cd /var/www/pms/frontend/dist

# Serve with nginx or your web server
# nginx config example in /etc/nginx/sites-available/
```

---

## Need Help?

If none of these work, consider:
- Using a build server (separate from production)
- Upgrading RAM to 4GB
- Using serverless deployment (Vercel, Netlify) which handles builds automatically
