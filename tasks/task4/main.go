package main

import (
	"bytes"
	"io"
	"log"
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
)

const targetBase = "https://dummy.restapiexample.com/api/v1"

func proxy(c *gin.Context) {
	path := c.Param("path")
	targetURL := targetBase + path

	body, _ := io.ReadAll(c.Request.Body)
	req, _ := http.NewRequest(c.Request.Method, targetURL, bytes.NewBuffer(body))

	req.Header.Set("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
	req.Header.Set("Content-Type", "application/json")

	client := &http.Client{Timeout: 10 * time.Second}
	resp, err := client.Do(req)
	if err != nil {
		log.Printf("ошибка запроса %v", err)
		c.JSON(502, gin.H{"error": "api not work"})
		return
	}
	defer resp.Body.Close()

	respBody, _ := io.ReadAll(resp.Body)
	log.Printf("ответ api: %d", resp.StatusCode)

	c.Data(resp.StatusCode, "application/json", respBody)
}

func main() {
	r := gin.Default()

	r.GET("/", func(c *gin.Context) {
		c.File("./index.html")
	})

	r.Any("/api/*path", proxy)

	log.Println("сервер запущен на http://localhost:8080")
	r.Run(":8080")
}
