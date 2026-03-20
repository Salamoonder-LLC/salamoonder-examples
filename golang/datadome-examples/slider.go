package main

import (
	"fmt"
	"log"
	"strings"

	"github.com/Salamoonder-LLC/salamoonder-go"
)

// Configuration
const (
	URL        = "https://example.com/"
	USER_AGENT = `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36`
	PROXY      = "http://user:pass@ip:port"
	API_KEY    = "sr-YOUR-KEY"
)

func main() {
	client := salamoonder.New(API_KEY)

	headers := map[string]string{"User-Agent": USER_AGENT}
	response, err := client.Get(URL, headers, PROXY)
	if err != nil {
		log.Fatalf("Failed to get initial page: %v", err)
	}

	cookies := response.Cookies["datadome"]
	if cookies == "" {
		fmt.Println("No DataDome cookie found")
		return
	}

	constructedURL, err := client.Datadome.ParseSliderURL(string(response.Body), cookies, URL)
	if err != nil {
		log.Fatalf("Failed to parse slider URL: %v", err)
	}

	taskID, err := client.Task.CreateTask("DataDomeSliderSolver", map[string]interface{}{
		"captcha_url":  constructedURL,
		"user_agent":   USER_AGENT,
		"country_code": "us",
	})
	if err != nil {
		log.Fatalf("Failed to create task: %v", err)
	}

	result, err := client.Task.GetTaskResult(taskID)
	if err != nil {
		log.Fatalf("Failed to get task result: %v", err)
	}

	var solvedCookie string
	if cookieStr, ok := result["cookie"].(string); ok {
		if strings.Contains(cookieStr, "datadome=") {
			parts := strings.Split(cookieStr, "datadome=")
			if len(parts) > 1 {
				solvedCookie = strings.Split(parts[1], ";")[0]
			}
		}
	} else {
		log.Printf("ERROR: Failed to solve %+v", result)
		return
	}

	client.SessionCookies.Set("datadome", solvedCookie, ".example.com")

	response, err = client.Get(URL, headers, "")
	if err != nil {
		log.Fatalf("Failed to validate bypass: %v", err)
	}

	if response.StatusCode == 200 {
		log.Printf("SUCCESS: [+] Successfully bypassed DD Slider.")
		log.Printf("SUCCESS: [+] Status Code: %d", response.StatusCode)
	} else {
		log.Printf("ERROR: Bypass failed")
	}
}