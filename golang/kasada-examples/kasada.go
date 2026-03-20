package main

import (
	"log"

	"github.com/Salamoonder-LLC/salamoonder-go"
)

// Configuration
const (
	URL      = "https://example.com/auth/v2/customer/login"
	API_KEY  = "sr-YOUR-KEY"
	USERNAME = "USERNAME"
	PASSWORD = "PASSWORD"
)

var headers = map[string]string{}

func main() {
	client := salamoonder.New(API_KEY)

	taskID, err := client.Task.CreateTask("KasadaCaptchaSolver", map[string]interface{}{
		"pjs_url": "https://example.com/149e9513-01fa-4fb0-aad4-566afd725d1b/2d206a39-8ed7-437e-a3be-862e0f06eea3/p.js",
		"cd_only": "false",
	})
	if err != nil {
		log.Fatalf("Failed to create task: %v", err)
	}

	result, err := client.Task.GetTaskResult(taskID)
	if err != nil {
		log.Fatalf("Failed to get task result: %v", err)
	}

	if _, ok := result["x-kpsdk-ct"]; !ok {
		log.Printf("ERROR: Failed to solve challenge: %+v", result)
		return
	}

	headers["accept"] = "application/json, text/plain, */*"
	headers["accept-language"] = "en-US,en;q=0.9"
	headers["cache-control"] = "no-cache"
	headers["content-type"] = "application/json"
	headers["ocp-apim-subscription-key"] = "b4d9f36380184a3788857063bce25d6a"
	headers["x-kpsdk-cd"] = result["x-kpsdk-cd"].(string)
	headers["x-kpsdk-ct"] = result["x-kpsdk-ct"].(string)
	headers["user-agent"] = result["user-agent"].(string)
	headers["Referer"] = "https://www.example.com/"

	payload := map[string]interface{}{
		"ShouldTimeout": false,
		"UserName":      USERNAME,
		"Password":      PASSWORD,
		"OriginRoute":   "home",
	}

	response, err := client.PostJSON(URL, payload, headers, "")
	if err != nil {
		log.Fatalf("Failed to post: %v", err)
	}

	if response.StatusCode != 429 {
		log.Printf("SUCCESS: Successfully solved Kasada. %s", string(response.Body))
	} else {
		log.Printf("ERROR: Failed to solve Kasada %s", string(response.Body))
	}
}