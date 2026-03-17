package main

import (
	"fmt"
	"log"

	"github.com/salamoonder/salamoonder-go"
)

// Keep in mind not using the same USER-AGENT as displayed as our docs will result in bad responses.
// https://apidocs.salamoonder.com/tasks/kasada/payload

const (
	URL        = "https://example.com/149e9513-01fa-4fb0-aad4-566afd725d1b/2d206a39-8ed7-437e-a3be-862e0f06eea3/fp?x-kpsdk-v=j-1.2.170"
	USER_AGENT = `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36`
	PROXY      = "http://user:pass@ip:port"
	API_KEY    = "sr-YOUR-KEY"
)

func main() {
	client := salamoonder.New(API_KEY)

	data, err := client.Kasada.ParseKasadaScript(URL, USER_AGENT, PROXY)
	if err != nil {
		log.Fatalf("Failed to parse Kasada script: %v", err)
	}

	taskID, err := client.Task.CreateTask("KasadaPayloadSolver", map[string]interface{}{
		"url":            "https://example.com",
		"script_url":     data["script_url"],
		"script_content": data["script_content"],
	})
	if err != nil {
		log.Fatalf("Failed to create task: %v", err)
	}

	result, err := client.Task.GetTaskResult(taskID)
	if err != nil {
		log.Fatalf("Failed to get task result: %v", err)
	}

	postSolution, err := client.Kasada.PostPayload(
		"https://example.com",
		result,
		USER_AGENT,
		PROXY,
		false, // mfc
	)
	if err != nil {
		log.Fatalf("Failed to post payload: %v", err)
	}

	fmt.Printf("%+v\n", postSolution)
}