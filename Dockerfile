# pull official base image
FROM node:16.14.0-alpine
#FROM node:17-alpine
#RUN npm install -g http-server

# set working directory
WORKDIR /app
EXPOSE 3000

# add `/app/node_modules/.bin` to $PATH
#ENV PATH /app/node_modules/.bin:$PATH

# install app dependencies
#COPY package.json ./
COPY package.json ./
#COPY package-lock.json ./
#RUN npm install
RUN yarn install

# add app
#COPY . .
COPY . ./
#RUN npm run build


# start app
#CMD ["http-server", "dist"]
CMD ["npm", "start"]
