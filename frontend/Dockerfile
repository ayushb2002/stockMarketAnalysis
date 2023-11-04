# Pull latest official node image
FROM node:latest

# Expose ports
EXPOSE 3000
EXPOSE 35729

# Set working directory
WORKDIR /frontend

# Add /app/node_modules/.bin to environment variables
ENV PATH node_modules/.bin:$PATH

# Copy package files and install app dependencies
COPY package.json package.json
COPY yarn.lock yarn.lock
RUN yarn install

# Start the React app
CMD ["yarn", "start"]