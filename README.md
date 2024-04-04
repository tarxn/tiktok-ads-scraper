<<<<<<< HEAD
## Selenium & Chrome template

A template example built with Selenium and a headless Chrome browser to scrape a website and save the results to storage. The URL of the web page is passed in via input, which is defined by the [input schema](https://docs.apify.com/platform/actors/development/input-schema). The template uses the [Selenium WebDriver](https://www.selenium.dev/documentation/webdriver/) to load and process the page. Enqueued URLs are stored in the default [request queue](https://docs.apify.com/sdk/python/reference/class/RequestQueue). The data are then stored in the default [dataset](https://docs.apify.com/platform/storage/dataset) where you can easily access them.

## Included features

- **[Apify SDK](https://docs.apify.com/sdk/python/)** for Python - a toolkit for building Apify [Actors](https://apify.com/actors) and scrapers in Python
- **[Input schema](https://docs.apify.com/platform/actors/development/input-schema)** - define and easily validate a schema for your Actor's input
- **[Request queue](https://docs.apify.com/sdk/python/docs/concepts/storages#working-with-request-queues)** - queues into which you can put the URLs you want to scrape
- **[Dataset](https://docs.apify.com/sdk/python/docs/concepts/storages#working-with-datasets)** - store structured data where each object stored has the same attributes
- **[Selenium](https://pypi.org/project/selenium/)** - a browser automation library

## How it works

This code is a Python script that uses Selenium to scrape web pages and extract data from them. Here's a brief overview of how it works:

- The script reads the input data from the Actor instance, which is expected to contain a `start_urls` key with a list of URLs to scrape and a `max_depth` key with the maximum depth of nested links to follow.
- The script enqueues the starting URLs in the default request queue and sets their depth to 1.
- The script processes the requests in the queue one by one, fetching the URL using requests and parsing it using Selenium.
- If the depth of the current request is less than the maximum depth, the script looks for nested links in the page and enqueues their targets in the request queue with an incremented depth.
- The script extracts the desired data from the page (in this case, titles of each page) and pushes them to the default dataset using the `push_data` method of the Actor instance.
- The script catches any exceptions that occur during the [web scraping](https://apify.com/web-scraping) process and logs an error message using the `Actor.log.exception` method.

## Resources

- [Selenium controlled Chrome example](https://apify.com/apify/example-selenium)
- [Selenium Grid: what it is and how to set it up](https://blog.apify.com/selenium-grid-what-it-is-and-how-to-set-it-up/)
- [Web scraping with Selenium and Python](https://blog.apify.com/web-scraping-with-selenium-and-python/)
- [Cypress vs. Selenium for web testing](https://blog.apify.com/cypress-vs-selenium/)
- [Python tutorials in Academy](https://docs.apify.com/academy/python)
- [Video guide on getting scraped data using Apify API](https://www.youtube.com/watch?v=ViYYDHSBAKM)
- A short guide on how to build web scrapers using code templates:

[web scraper template](https://www.youtube.com/watch?v=u-i-Korzf8w)


## Getting started

For complete information [see this article](https://docs.apify.com/platform/actors/development#build-actor-at-apify-console). In short, you will:

1. Build the Actor
2. Run the Actor

## Pull the Actor for local development

If you would like to develop locally, you can pull the existing Actor from Apify console using Apify CLI:

1. Install `apify-cli`

    **Using Homebrew**

    ```bash
    brew install apify-cli
    ```

    **Using NPM**

    ```bash
    npm -g install apify-cli
    ```

2. Pull the Actor by its unique `<ActorId>`, which is one of the following:
    - unique name of the Actor to pull (e.g. "apify/hello-world")
    - or ID of the Actor to pull (e.g. "E2jjCZBezvAZnX8Rb")

    You can find both by clicking on the Actor title at the top of the page, which will open a modal containing both Actor unique name and Actor ID.

    This command will copy the Actor into the current directory on your local machine.

    ```bash
    apify pull <ActorId>
    ```

## Documentation reference

To learn more about Apify and Actors, take a look at the following resources:

- [Apify SDK for JavaScript documentation](https://docs.apify.com/sdk/js)
- [Apify SDK for Python documentation](https://docs.apify.com/sdk/python)
- [Apify Platform documentation](https://docs.apify.com/platform)
- [Join our developer community on Discord](https://discord.com/invite/jyEM2PRvMU)
=======
# tiktok_ads_scrapper

>>>>>>> 11c07dcc5306a2472f20fc53292b7e870d74c500
