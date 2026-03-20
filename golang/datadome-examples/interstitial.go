package main

import (
	"log"
	"strings"

	"github.com/Salamoonder-LLC/salamoonder-go"
)

// Configuration
const (
	URL        = "https://example.com/"
	USER_AGENT = `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36`
	PROXY      = "http://user:pass@ip:port"
	API_KEY    = "sr-YOUR-KEY"
)

var HEADERS = map[string]string{
	"User-Agent":             USER_AGENT,
	"sec-ch-ua":              `"Google Chrome";v="139", "Not-A.Brand";v="8", "Chromium";v="139"`,
	"sec-ch-ua-mobile":       "?0",
	"sec-ch-ua-platform":     `"Windows"`,
	"accept-language":        "en-US,en;q=0.9",
}

func main() {
	client := salamoonder.New(API_KEY)

	response, err := client.Get(URL, HEADERS, PROXY)
	if err != nil {
		log.Fatalf("Failed to get initial page: %v", err)
	}

	cookies := response.Cookies["datadome"]
	if cookies == "" {
		log.Printf("ERROR: No DataDome cookie found")
		return
	}

	constructedURL, err := client.Datadome.ParseInterstitialURL(string(response.Body), cookies, URL)
	if err != nil {
		log.Fatalf("Failed to parse interstitial URL: %v", err)
	}

	taskID, err := client.Task.CreateTask("DataDomeInterstitialSolver", map[string]interface{}{
		"captcha_url":  constructedURL,
		"user_agent":   USER_AGENT,
		"country_code": "pl",
	})
	if err != nil {
		log.Fatalf("Failed to create task: %v", err)
	}

	result, err := client.Task.GetTaskResult(taskID)
	if err != nil {
		log.Fatalf("Failed to get task result: %v", err)
	}

	cookieStr, ok := result["cookie"].(string)
	if !ok {
		log.Printf("ERROR: Failed to solve challenge: %+v", result)
		return
	}

	var solvedCookie string
	if strings.Contains(cookieStr, "datadome=") {
		parts := strings.SplitN(cookieStr, "datadome=", 2)
		if len(parts) > 1 {
			solvedCookie = strings.SplitN(parts[1], ";", 2)[0]
		}
	} else {
		solvedCookie = strings.SplitN(cookieStr, ";", 2)[0]
	}

	client.SessionCookies.Set("datadome", solvedCookie, ".example.com")

	response, err = client.Get(URL, HEADERS, PROXY)
	if err != nil {
		log.Fatalf("Failed to validate bypass: %v", err)
	}

	if response.StatusCode == 200 {
		log.Printf("SUCCESS: %s", string(response.Body))
		log.Printf("SUCCESS: Successfully bypassed Interstitial!")
	} else {
		log.Printf("ERROR: Bypass failed (response: %s)", string(response.Body))
	}
}