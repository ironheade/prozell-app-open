# pull official base image
FROM node:16.14.0-alpine
#FROM node:17-alpine


# set working directory
WORKDIR /app

EXPOSE 3000

# add `/app/node_modules/.bin` to $PATH
#ENV PATH /app/node_modules/.bin:$PATH

# install app dependencies
COPY package.json ./
#COPY package-lock.json ./
RUN yarn install

# add app
COPY . ./

# start app
CMD ["npm", "start"]
