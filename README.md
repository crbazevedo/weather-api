
# Weather API

This repository contains the code for a FastAPI application that generates weather reports for cities around the world. The application uses data from the OpenWeatherMap API and the OpenAI GPT-4 model to generate the reports.

## Purpose

The purpose of this application is to generate short weather reports for a given city in the style of a local news reporter. The reports are based on real-time weather data from the OpenWeatherMap API. The language of the report is determined by the primary language spoken in the city.

The application uses the OpenAI GPT-4 model to generate the reports. The model is given a prompt that includes the city name and the weather data, and it generates a report that includes inside jokes about the city and sounds like it was written by a local news rporter from the city.

Here's an example of a prompt that the application might give to the GPT-4 model:

`Write a short Weather Report for {city} in the style of a local news reporter based on the following data: {weather_data}. Use the language spoken in that city for the report. Add inside jokes about the city and make it sound like a real weather report. Write in the style of a local news reporter who is from {city}.`


In this prompt, `{city}` is replaced with the name of the city and `{weather_data}` is replaced with the weather data from the OpenWeatherMap API.

## How to Use

To use this application, you need to have Docker installed on your machine. You can then build and run the Docker image using the following commands:

```bash
docker build -t weather-api .
docker run -p 80:80 weather-api
```


Once the application is running, you can access it at `http://localhost:80`. The application provides two endpoints:

- `/weather/{city}`: Returns the current weather data for the city from the OpenWeatherMap API.
- `/weather-report/{city}`: Returns a weather report for the city generated by the GPT-4 model.

Replace `{city}` with the name of the city you want data for.

## License

This project is licensed under the terms of the MIT license.

This content includes headers, inline code, and code blocks, which are all standard features of Markdown. You can add this to your `README.md` file in your GitHub repository.
