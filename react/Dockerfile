FROM node:11.10

RUN mkdir /react
WORKDIR /react

ENV PATH /react/node_modules/.bin:$PATH

COPY package.json /react/package.json
RUN npm install --silent && \
    npm install react-scripts@2.1.5 -g --silent

CMD ["npm", "start"]