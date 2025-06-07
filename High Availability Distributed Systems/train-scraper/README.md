# Train Scraper API

## 🚀 How to Run

To start the application using Docker Compose, run:

```sh
docker compose up
```

---

## How to Use

### **Send a Scraping Request**

**Endpoint:**
```http
POST http://localhost:8080/api/commands/scrap?from={kod90}&to={kod90}
```

**Example:**
```http
POST http://localhost:8080/api/commands/scrap?from=40&to=159
```

*Parameters `from` and `to` are `kod90` values, which you can find [here](https://pl.wikipedia.org/wiki/Wikipedysta:Upior_polnocy/Kurs90).*  
*After executing the request, you will receive a unique `scrapingId`.*

### **Check Scraping Status**

**Endpoint:**
```http
GET http://localhost:8080/api/queries/scraping/{scrapingId}
```

**Example:**
```http
GET http://localhost:8080/api/queries/scraping/a42b1487-e3ac-44a1-a184-1348fa4e5d9f
```

*Replace `{scrapingId}` with the actual ID received from the POST request.*

---

## Development

For faster development, it is recommended to run the Spring Boot application locally instead of using Docker.  
Just uncomment the relevant URLs in the service configuration.

---


